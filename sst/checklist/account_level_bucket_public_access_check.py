from lib import common, language
from lib import level_const as level
import botocore.exceptions
import logging, traceback

def check_account_level_bucket_public_access(session, selected_language) -> common.CheckResult:

    translator = language.translation("account_level_bucket_public_access", selected_language)

    print(translator.checking())

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['Policy Name', 'Public Access Setting']

    sts_client = session.client('sts')
    s3control_client = session.client('s3control')

    account_id = None
    try :
        account_id = sts_client.get_caller_identity()["Account"]
        account_policy = s3control_client.get_public_access_block(AccountId=account_id)["PublicAccessBlockConfiguration"]
    except s3control_client.exceptions.NoSuchPublicAccessBlockConfiguration as e:
        ret.level = level.danger
        ret.msg = translator.no_such_public_access_block_config()
        ret.result_rows.append(["ALL", "Not Exist"])
    except botocore.exceptions.ClientError :
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Unexpected Exception"
        ret.result_rows.append(['ERR', 'ERR'])
        return ret
    else:
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
            ret.msg = translator.success()
        elif public_allow_policy_counter > 0 and public_allow_policy_counter < nums_of_public_block_access_policies:
            ret.level = level.warning
            ret.msg = translator.warning()
        elif public_allow_policy_counter == nums_of_public_block_access_policies :
            ret.level = level.danger
            ret.msg = translator.danger()
        else:
            ret.level = level.error
            ret.msg = "Unexpected Exception"
            ret.result_rows = ["ERR", "ERR"]

    return ret