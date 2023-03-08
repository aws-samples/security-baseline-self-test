from lib import common, language
from lib import level_const as level
import botocore.exceptions
import logging, traceback

def check_iam_direct_attached_policy(session, selected_language) -> common.CheckResult:

    translator = language.translation("direct_attached_policy", selected_language)

    print(translator.checking())
    client = session.client('iam')

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ["IAM User", "Direct Attached Managed Policy", "Inline Policy"]

    try:
        user_list = client.list_users()["Users"]
    except client.exceptions.NoSuchEntityException:
        ret.level = level.warning
        ret.msg = translator.no_user()
        ret.result_rows.append(["-", "-", "-"])
        return ret
    except client.exceptions.ServiceFailureException:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Service Failure"
        ret.result_rows.append(["ERR", "ERR", "ERR"])
        return ret
    except botocore.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Unexpected Error"
        ret.result_rows.append(["ERR", "ERR", "ERR"])
        return ret
    
    if len(user_list) == 0:
        ret.level = level.warning
        ret.msg = translator.no_user()
    else:
        ret.level = level.success
        ret.msg = translator.success()

        for user in user_list:
            user_name = user["UserName"]
            
            nums_direct_attached_policies = None
            nums_inline_policies = None
            
            try:
                nums_direct_attached_policies = str(len(client.list_attached_user_policies(UserName=user_name)["AttachedPolicies"]))
            except botocore.exceptions.ClientError:
                logging.error(traceback.format_exc())
                ret.level = level.error
                ret.msg = "Unexpected Error"
                nums_direct_attached_policies = "ERR"

            try:
                nums_inline_policies = str(len(client.list_user_policies(UserName=user_name)["PolicyNames"]))
            except botocore.exceptions.ClientError:
                logging.error(traceback.format_exc())
                ret.level = level.error
                ret.msg = "Unexpected Error"
                nums_inline_policies = "ERR"

            if ret.level == level.error:
                continue
            else:
                ret.result_rows.append([user_name, nums_direct_attached_policies, nums_inline_policies])
            
                if nums_direct_attached_policies > "0" or nums_inline_policies > "0":
                    ret.level = level.warning
                    ret.msg = translator.warning()
                else:
                    pass

    return ret
