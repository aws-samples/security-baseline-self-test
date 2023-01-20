from lib import common
from lib import level_const as level
import botocore.exceptions
import logging, traceback

def check_account_level_bucket_public_access(session) -> common.CheckResult:

    ret = common.CheckResult()

    ret.title = "계정수준 S3 Bucket Public Access 설정 확인"
    ret.result_cols = ['Policy Name', 'Public Access Setting']

    sts_client = session.client('sts')
    s3control_client = session.client('s3control')

    account_id = None
    try :
        account_id = sts_client.get_caller_identity()["Account"]
        account_policy = s3control_client.get_public_access_block(AccountId=account_id)["PublicAccessBlockConfiguration"]
    except s3control_client.exceptions.NoSuchPublicAccessBlockConfiguration as e:
        ret.level = level.danger
        ret.msg = "계정의 기본 S3 Bucket Public Access 정책이 존재하지 않습니다."
        ret.result_rows.append(["ALL", "없음"])
    except botocore.exceptions.ClientError :
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "예기치 못한 에러가 발생했습니다."
        ret.result_rows.append(['ERR', 'ERR'])
        return ret
    else:
        public_allow_policy_counter = 0
        for policy_name, setting in account_policy.items():

            if setting == False:
                public_allow_policy_counter += 1
                ret.result_rows.append([policy_name, "허용"])
            else:
                ret.result_rows.append([policy_name, "차단"])

        nums_of_public_block_access_policies = len(account_policy.items())

        if public_allow_policy_counter == 0:
            ret.level = level.success
            ret.msg = "계정의 기본 S3 Bucket Public Access 정책이 모두 차단으로 설정되어 있습니다."
        elif public_allow_policy_counter > 0 and public_allow_policy_counter < nums_of_public_block_access_policies:
            ret.level = level.warning
            ret.msg = "계정의 기본 S3 Bucket Public Access 정책이 일부 허용으로 설정되어 있습니다. 차단하는 것이 보다 안전합니다."
        elif public_allow_policy_counter == nums_of_public_block_access_policies :
            ret.level = level.danger
            ret.msg = "계정의 기본 S3 Bucket Public Access 정책이 모두 허용으로 설정되어 있습니다. 차단하는 것이 보다 안전합니다."
        else:
            ret.level = level.error
            ret.msg = "예기치 못한 에러가 발생했습니다."
            ret.result_rows = ["ERR", "ERR"]

    return ret