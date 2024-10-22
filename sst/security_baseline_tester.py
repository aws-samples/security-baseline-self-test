import boto3
import botocore
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from checklist import *
from lib import common, level_const
from lib.language import get_translator
import report_generator
import logging
import datetime
import os

class SecurityBaselineTester:
    def __init__(self, profile, language):
        self.profile = profile
        self.language = language
        self.session = self._create_session()
        self.config = self._load_config()
        self.translator = get_translator("main", language)

    def _create_session(self):
        if self.profile == "default":
            return boto3.Session()
        return boto3.Session(profile_name=self.profile)

    def _load_config(self):
        try:
            with open('config.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error("config.json file not found. Please ensure it exists in the same directory as this script.")
            raise
        except json.JSONDecodeError:
            logging.error("Error parsing config.json. Please ensure it is a valid JSON file.")
            raise

    def run(self):
        try:
            self._validate_session()
            caller_identity = self._get_caller_identity()
            self._print_auditor_info(caller_identity)
            
            logging.info(self.translator.translate("start_test"))
            
            account_id, results = self._execute_tests()
            self._generate_report(account_id, results)
            
            logging.info(self.translator.translate("test_completed"))
        except Exception as e:
            logging.error(f"An error occurred during the security baseline test: {str(e)}", exc_info=True)

    def _validate_session(self):
        if self.session.region_name is None:
            raise ValueError('AWS region is not specified. Run "aws configure" to set it.')

    def _get_caller_identity(self):
        try:
            return self.session.client('sts').get_caller_identity()
        except botocore.exceptions.ClientError as e:
            logging.error(f"Failed to get caller identity: {str(e)}")
            raise

    def _print_auditor_info(self, caller_identity):
        logging.info("==================== AUDITOR INFO ====================")
        logging.info(f"USER ID : {caller_identity['UserId']}")
        logging.info(f"ACCOUNT : {caller_identity['Account']}")
        logging.info(f"ARN     : {caller_identity['Arn']}")
        logging.info("=====================================================")

    def _execute_tests(self):
        iam_client = self.session.client('iam')
        sts_client = self.session.client('sts')
        
        account_id = common.get_account_id(sts_client)
        logging.info(self.translator.translate("request_credential_report"))
        credential_report = common.generate_credential_report(iam_client)
        
        with ThreadPoolExecutor(max_workers=self.config.get('max_workers', 5)) as executor:
            futures = {
                executor.submit(self._run_check, check_name, credential_report): check_name
                for check_name in self.config.get('checks', [])
            }
            
            results = {level: [] for level in ["Success", "Warning", "Danger", "Error", "Info"] if isinstance(level, str)}
            for future in as_completed(futures):
                result = future.result()
                results[result.level].append(result)
        
        return account_id, results

    def _run_check(self, check_name, credential_report):
        check_module = __import__(f"checklist.{check_name}", fromlist=[check_name])
        check_method = getattr(check_module, self.config['checks'][check_name])
        translator = get_translator(check_name, self.language)

        if check_name in ['alternate_contacts', 'account_level_bucket_public_access', 'bucket_public_access',
                          'cloudwatch_alarm_configuration', 'direct_attached_policy', 'guardduty_enabled',
                          'multi_region_instance_usage', 'multi_region_trail', 'trail_enabled', 'iam_password_policy']:
            return check_method(self.session, translator)
        elif check_name in ['root_mfa', 'root_usage', 'root_access_key', 'iam_user_mfa']:
            return check_method(self.session, translator, credential_report)
        elif check_name == 'trusted_advisor':
            return check_method(translator)
        else:
            raise ValueError(f"Unknown check method: {check_name}")
        
    def _check_result_directory(self):
        directory_name = "results"

        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            logging.info(self.translator.translate("results_folder_created"))
        else:
            logging.info(self.translator.translate("results_folder_already_exists"))
    
    def _generate_report(self, account_id, results):
        html_report = report_generator.generate_html_report(account_id, results, self.language)
        
        current_time = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        short_account_id = account_id[-4:]

        self._check_result_directory()
        
        report_filename = f"./results/sst-report-{short_account_id}-{current_time}.html"
        
        with open(report_filename, "w") as f:
            f.write(html_report)
        
        logging.info(self.translator.translate("generate_result_report"))