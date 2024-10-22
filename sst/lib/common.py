import botocore.exceptions
import logging
import json
import os
from .enums import CREDENTIAL_REPORT_COLS
import time

class Ret:
    def __init__(self) -> None:
        self.status_code = 200
        self.body = "success"
        self.headers = {'Content-Type': 'text/html;charset=UTF-8'}

    def to_dict(self) -> dict:
        return {
            'statusCode': self.status_code,
            'body': self.body,
            'headers': self.headers
        }

class CheckResult:
    def __init__(self) -> None:
        self.title = "UNKNOWN"
        self.level = "UNKNOWN"
        self.msg = "UNKNOWN"
        self.result_rows = []
        self.result_cols = []
        self.error_message = None  # 새로 추가된 필드

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'level': self.level,
            'msg': self.msg,
            'result_rows': self.result_rows,
            'result_cols': self.result_cols,
            'error_message': self.error_message
        }

    def get_table(self) -> dict:
        return {
            'cols': self.result_cols,
            'rows': self.result_rows
        }

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Config file not found: {config_path}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in config file: {config_path}")
        raise

config = load_config()

def get_iam_credential_report(credential_report) -> list:
    first_iam_user_row_index = config['credential_report']['first_iam_user_row_index']
    if len(credential_report) < first_iam_user_row_index + 1:
        return []
    else:
        return list(map(lambda x: x.split(","), credential_report[first_iam_user_row_index:]))

def get_root_credential_report(credential_report) -> list:
    root_row_index = config['credential_report']['root_row_index']
    return credential_report[root_row_index].split(",")

def generate_credential_report(client) -> list:
    try:
        for trial in range (1,5):
            response = client.generate_credential_report()
            logging.info(f"Generating credentials report for your account...({str(trial)}) Current state is {str(response['State'])}.")

            if response['State'] == "COMPLETE":
                return client.get_credential_report()["Content"].decode('ascii').split()
            
            time.sleep(5)
        
        raise TimeoutError("Time out")

    except (TimeoutError, botocore.exceptions.ClientError) as e:
        logging.error(f"Couldn't generate a credentials report for your account. (Error : {str(e)})")
        return []

def get_account_id(client) -> str:
    try:
        return str(client.get_caller_identity()["Account"])
    except botocore.exceptions.ClientError as e:
        logging.error(f"Error getting account ID: {str(e)}")
        return "ERR"

def get_opted_in_regions(ec2_client) -> list:
    try:
        response = ec2_client.describe_regions(Filters=[
            {
                "Name": "opt-in-status",
                "Values": ["opted-in", "opt-in-not-required"]
            }
        ])
        return [region['RegionName'] for region in response["Regions"]]
    except botocore.exceptions.ClientError as e:
        logging.error(f"Error getting opted-in regions: {str(e)}")
        raise