import boto3, botocore
from checklist import *
from lib import common, level_const, language
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import report_generator
import datetime
import logging, traceback
import argparse
import os

global translators

def execute_test(session) -> tuple:

    iam_client = session.client('iam')
    sts_client = session.client('sts')

    account_id_str = common.get_account_id(sts_client)

    selected_language = translator.language
    print(translator.request_credential_report())
    credential_report = common.generate_credential_report(iam_client)

    number_of_whole_test_case = 15

    thread_executor = ThreadPoolExecutor()
    futures = [0 for x in range(number_of_whole_test_case)]

    futures[common.CHECKLIST_INDEX_CONST.ROOT_MFA_SETTING_CHECK.value] = thread_executor.submit(root_mfa_setting_check.check_root_mfa_setting,credential_report, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.ROOT_USAGE_CHECK.value] = thread_executor.submit(root_usage_check.check_root_usage,credential_report, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.ROOT_CREDENTIAL_CHECK.value] = thread_executor.submit(root_user_accesskey_check.check_root_accesskey_usage,credential_report, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.IAM_MFA_SETTING_CHECK.value] = thread_executor.submit(iam_user_mfa_setting_check.check_iam_user_mfa_setting,credential_report, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.IAM_PASSWORD_POLICY_CHECK.value] = thread_executor.submit(iam_password_policy_check.check_iam_password_policy, session, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.NON_GROUP_POLICY_CHECK.value] = thread_executor.submit(direct_attached_policy_check.check_iam_direct_attached_policy, session, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.ALTERNATE_CONTACT_CHECK.value] = thread_executor.submit(alternate_contact_check.check_alternate_contact_filling, session, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.TRAIL_ENABLED_CHECK.value] = thread_executor.submit(trail_enabled_check.check_trail_enabled, session, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.MULTIREGION_TRAIL_CHECK.value] = thread_executor.submit(multiregion_trail_enabled_check.check_multi_retion_trail_enabled, session, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.ACCOUNT_LEVEL_BUCKET_PUBLIC_ACCESS_CHECK.value] = thread_executor.submit(account_level_bucket_public_access_check.check_account_level_bucket_public_access, session, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.BUCKET_LEVEL_PUBLIC_ACCESS_CHECK.value] = thread_executor.submit(bucket_public_access_check.check_bucket_public_access, session, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.CLOUDWATCH_ALARM_CONFIGURATION_CHECK.value] = thread_executor.submit(cloudwatch_alarm_configuration_check.check_cloudwatch_alarm_configuration, session, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.MULTIREGION_INSTANCE_USAGE_CHECK.value] = thread_executor.submit(multiregion_instance_usage_check.check_multiregion_instance_usage, session, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.GUARD_DUTY_ENABLED_CHECK.value] = thread_executor.submit(guard_duty_check.check_guard_duty_enabled, session, selected_language)
    futures[common.CHECKLIST_INDEX_CONST.TRUST_ADVISOR_CHECK.value] = thread_executor.submit(trust_advisor_check.check_trust_advisor_configuration, selected_language)

    result_sort_by_level = {
        level_const.danger:[],
        level_const.warning:[],
        level_const.success:[],
        level_const.error:[],
        level_const.info:[]
    }

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        result_sort_by_level[result.level].append(result)

    return account_id_str, result_sort_by_level

## Scrypt Start From Here

ret = common.Ret()

parser = argparse.ArgumentParser()
parser.add_argument("--profile", default="default", dest="profile", action="store", help="IAM user profile")

args = parser.parse_args()

session = ""

if args.profile == "default":
    print("AWS Credential : Default Profile")
    session = boto3.Session()
else:
    print("AWS Credentials : ${profile}".format(profile=args.profile))
    session = boto3.Session(profile_name=args.profile)

try:
    sts_client = session.client('sts')
    caller_identity = sts_client.get_caller_identity()
    
    user_id = caller_identity['UserId']
    account = caller_identity['Account']
    arn = caller_identity['Arn']

    if session.region_name == None:
        print('You must specify a region. You can also configure your region by running "aws configure".')
        exit()

    print("")
    print("##################### AUDITOR INFO #####################")
    print("##  USER ID : {user_id}".format(user_id=user_id))
    print("##  ACCOUNT : {account}".format(account=account))
    print("##  ARN : {arn}".format(arn=arn))
    print("########################################################")

except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'AccessDenied':
        print("Please Check IAM Permission. (sts:GetCallerIdentity is required)")
        logging.error(traceback.format_exc())
    else :
        print("UnexpectedException")
        logging.error(traceback.format_exc())
    exit()
except Exception as e:
    logging.error(traceback.format_exc())
    exit()

selected_language = ""

while True:
    print("==================================================")
    print("#### Select Language ####")
    print("1. English")
    print("2. Korean")
    print("0. EXIT")
    
    selected_language = input("Select Your Language : ")
    print("==================================================")

    if selected_language == '1':
        selected_language = language.LANGUAGE_CODE.ENGLISH.value
        break
    elif selected_language == '2':
        selected_language = language.LANGUAGE_CODE.KOREAN.value
        break
    elif selected_language == '0':
        exit()
    else:
        print("Invalid Input. Please Select Valid Number.")


translator = language.translation("main", selected_language)
print(translator.start_test())

try:
    account_id_str, result_sort_by_level = execute_test(session)

    print(translator.generate_result_report())
    html_report = report_generator.generate_html_report(account_id_str, result_sort_by_level, selected_language)
except Exception as e:
    logging.error(traceback.format_exc())

    ret.status_code = 500
    ret.body = '''InternalException'''
else:
    report_object_name = "security-self-testresult-{generated_date}.html".format(generated_date=datetime.datetime.now().strftime("%Y-%m-%d_h%Hm%Ms%S"))
    f = open(report_object_name, "wt")
    try:
        f.write(html_report)
    except IOError as e:
        logging.error(traceback.format_exc())

        ret.status_code=500
        ret.body = '''InternalException'''

    f.close()
    
    print("Result Path : {path}/{filename}".format(path=os.getcwd(), filename=report_object_name))
    
print("Finish")
logging.info('Successfully Finished')