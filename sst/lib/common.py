import botocore.exceptions
from enum import Enum
import logging, traceback

class Ret:
    def __init__(self) -> None:
        self.status_code = 200
        self.body = "success"
        self.headers = {'Content-Type': 'text/html;charset=UTF-8'}

    def to_dict(self) -> dict:
        return {
            'statusCode':self.status_code,
            'body':self.body,
            'headers':self.headers
        }

class CheckResult:
    def __init__(self) -> None:
        self.title = "UNKNOWN"
        self.level = "UNKNOWN"
        self.msg = "UNKNOWN"
        self.result_rows = []
        self.result_cols = []

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'level' : self.level,
            'msg' : self.msg,
            'result_rows' : self.result_rows,
            'result_cols' : self.result_cols
        }

    def get_table(self) -> dict:
        return {
            'cols' : self.result_cols,
            'rows' : self.result_rows
        }

def get_iam_credential_report(credential_report) -> list:
    first_iam_user_row_index = 2
    if len(credential_report) < first_iam_user_row_index+1:
        return []
    else :
        return list(map(lambda x: x.split(","), credential_report[2:]))

def get_root_credential_report(credential_report) -> list:
    root_row_index = 1
    return credential_report[root_row_index].split(",")

def generate_credential_report(client) -> list:
    try:
        return client.get_credential_report()["Content"].decode('ascii').split()
    except client.exceptions.CredentialReportNotPresentException:
        logging.warning('CredentialReportNotPresent')
        state = client.generate_credential_report()["State"]
        if state == "COMPLETE":
            return client.get_credential_report()["Content"].decode('ascii').split()
        else:
            logging.error(traceback.format_exc())
    except client.exceptions.CredentialReportExpiredException:
        logging.warning('CredentialReportExpiredException')
        client.generate_credential_report()
        state = client.generate_credential_report()
        if state == "COMPLETE":
            return client.get_credential_report()["Content"].decode('ascii').split()
        else:
            logging.error(traceback.format_exc())
    except client.exceptions.CredentialReportNotReadyException:
        logging.error(traceback.format_exc())
    except client.exceptions.ServiceFailureException:
        logging.error(traceback.format_exc())
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())

    return []

def get_account_id(client) -> str:
    try:
        return str(client.get_caller_identity()["Account"])
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())

    return "ERR"

def get_opted_in_regions(ec2_client) -> list:
    try:
        response = ec2_client.describe_regions(Filters=[
            {
                "Name":"opt-in-status",
                "Values":[
                    "opted-in", "opt-in-not-required"
                ]
            }
        ])
    except botocore.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        raise botocore.exceptions.ClientError
    else :
        region_name_list = []
        
        for region in response["Regions"]:
            region_name_list.append(region['RegionName'])
        
        return region_name_list

class CREDENTIAL_REPORT_COLS(Enum):
    USER=0
    ARN=1
    USER_CREATION_TIME=2
    PASSWORD_ENABLED=3
    PASSWORD_LAST_USED=4
    PASSWORD_LAST_CHANGED=5
    PASSWORD_NEXT_ROTATION=6
    MFA_ACTIVE=7
    ACCESS_KEY_1_ACTIVE=8
    ACCESS_KEY_1_LAST_ROTATED=9
    ACCESS_KEY_1_LAST_USED_DATE=10
    ACCESS_KEY_1_LAST_USED_REGION=11
    ACCESS_KEY_1_LAST_USED_SERVICE=12
    ACCESS_KEY_2_ACTIVE=13
    ACCESS_KEY_2_LAST_ROTATED=14
    ACCESS_KEY_2_LAST_USED_DATE=15
    ACCESS_KEY_2_LAST_USED_REGION=16
    ACCESS_KEY_2_LAST_USED_SERVICE=17
    CERT_1_ACTIVE=18
    CERT_1_LAST_ROTATED=19
    CERT_2_ACTIVE=20
    CERT_2_LAST_ROTATED=21

class CHECKLIST_INDEX_CONST(Enum):
    ROOT_MFA_SETTING_CHECK=0
    ROOT_USAGE_CHECK=1
    ROOT_CREDENTIAL_CHECK=2
    IAM_MFA_SETTING_CHECK=3
    IAM_PASSWORD_POLICY_CHECK=4
    NON_GROUP_POLICY_CHECK=5
    ALTERNATE_CONTACT_CHECK=6
    TRAIL_ENABLED_CHECK=7
    MULTIREGION_TRAIL_CHECK=8
    ACCOUNT_LEVEL_BUCKET_PUBLIC_ACCESS_CHECK=9
    BUCKET_LEVEL_PUBLIC_ACCESS_CHECK=10
    CLOUDWATCH_ALARM_CONFIGURATION_CHECK=11
    MULTIREGION_INSTANCE_USAGE_CHECK=12
    GUARD_DUTY_ENABLED_CHECK=13
    TRUST_ADVISOR_CHECK=14