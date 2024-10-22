from lib import common
from lib import level_const as level
import botocore.exceptions
import logging

def get_user_policies(client, user_name):
    try:
        direct_attached = len(client.list_attached_user_policies(UserName=user_name)["AttachedPolicies"])
        inline = len(client.list_user_policies(UserName=user_name)["PolicyNames"])
        return str(direct_attached), str(inline)
    except botocore.exceptions.ClientError as e:
        logging.error(f"Error getting policies for user {user_name}: {str(e)}", exc_info=True)
        return "ERR", "ERR"

def check_iam_direct_attached_policy(session, translator) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    client = session.client('iam')
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ["IAM User", "Direct Attached Managed Policy", "Inline Policy"]

    try:
        user_list = client.list_users()["Users"]
    except client.exceptions.NoSuchEntityException:
        ret.level = level.warning
        ret.msg = translator.translate("no_user")
        ret.result_rows.append(["-", "-", "-"])
        return ret
    except client.exceptions.ServiceFailureException as e:
        ret.level = level.error
        ret.msg = translator.translate("service_failure")
        ret.result_rows.append(["ERR", "ERR", "ERR"])
        ret.error_message = str(e)
        logging.error(f"Service Failure: {str(e)}", exc_info=True)
        return ret
    except botocore.exceptions.ClientError as e:
        ret.level = level.error
        ret.msg = translator.translate("unexpected_error")
        ret.result_rows.append(["ERR", "ERR", "ERR"])
        ret.error_message = str(e)
        logging.error(f"Unexpected Error: {str(e)}", exc_info=True)
        return ret

    if not user_list:
        ret.level = level.warning
        ret.msg = translator.translate("no_user")
        return ret

    ret.level = level.success
    ret.msg = translator.translate("success")

    for user in user_list:
        user_name = user["UserName"]
        direct_attached, inline = get_user_policies(client, user_name)
        
        if direct_attached == "ERR" or inline == "ERR":
            ret.level = level.error
            ret.msg = translator.translate("unexpected_error")
        else:
            ret.result_rows.append([user_name, direct_attached, inline])
            if int(direct_attached) > 0 or int(inline) > 0:
                ret.level = level.warning
                ret.msg = translator.translate("warning")

    return ret