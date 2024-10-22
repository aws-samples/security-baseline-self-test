from lib import common
from lib import level_const as level
import botocore.exceptions
import logging

def check_account_level_bucket_public_access(session, translator) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['Policy Name', 'Public Access Setting']

    sts_client = session.client('sts')
    s3control_client = session.client('s3control')

    try:
        account_id = sts_client.get_caller_identity()["Account"]
    except botocore.exceptions.ClientError as e:
        logging.error(f"Failed to get caller identity: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("failed_get_identity")
        ret.result_rows.append(['ERR', 'ERR'])
        ret.error_message = str(e)
        return ret

    try:
        account_policy = s3control_client.get_public_access_block(AccountId=account_id)["PublicAccessBlockConfiguration"]
    except s3control_client.exceptions.NoSuchPublicAccessBlockConfiguration:
        ret.level = level.danger
        ret.msg = translator.translate("no_such_public_access_block_config")
        ret.result_rows.append(["ALL", "Not Exist"])
        return ret
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logging.error(f"AWS API error: {error_code} - {error_message}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("aws_api_error")
        ret.result_rows.append(['ERR', 'ERR'])
        ret.error_message = f"{error_code}: {error_message}"
        return ret
    except botocore.exceptions.BotoCoreError as e:
        logging.error(f"Boto3 error occurred: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("boto3_error")
        ret.result_rows.append(['ERR', 'ERR'])
        ret.error_message = str(e)
        return ret
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("unexpected_error")
        ret.result_rows.append(['ERR', 'ERR'])
        ret.error_message = str(e)
        return ret

    public_allow_policy_counter = 0
    for policy_name, setting in account_policy.items():
        if setting == False:
            public_allow_policy_counter += 1
            ret.result_rows.append([policy_name, "Allow"])
        else:
            ret.result_rows.append([policy_name, "Block"])

    nums_of_public_block_access_policies = len(account_policy.items())
    
    if public_allow_policy_counter == 0:
        ret.level = level.success
        ret.msg = translator.translate("success")
    elif 0 < public_allow_policy_counter < nums_of_public_block_access_policies:
        ret.level = level.warning
        ret.msg = translator.translate("warning")
    elif public_allow_policy_counter == nums_of_public_block_access_policies:
        ret.level = level.danger
        ret.msg = translator.translate("danger")
    else:
        ret.level = level.error
        ret.msg = translator.translate("unexpected_error")
        ret.result_rows = ["ERR", "ERR"]

    return ret