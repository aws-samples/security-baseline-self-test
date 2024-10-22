from lib import common
from lib import level_const as level
import botocore.exceptions
import logging

def check_iam_password_policy(session, translator) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    client = session.client('iam')
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ["Password Policy"]

    try:
        client.get_account_password_policy()
        ret.level = level.success
        ret.msg = translator.translate("success")
    except client.exceptions.NoSuchEntityException:
        ret.level = level.warning
        ret.msg = translator.translate("warning")
        ret.result_rows.append(["Not Set"])
    except client.exceptions.ServiceFailureException as e:
        logging.error(f"Service Failure: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("service_failure")
        ret.result_rows.append(["ERR"])
        ret.error_message = str(e)
    except botocore.exceptions.ClientError as e:
        logging.error(f"Unexpected ClientError: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("unexpected_error")
        ret.result_rows.append(["ERR"])
        ret.error_message = str(e)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("unexpected_error")
        ret.result_rows.append(["ERR"])
        ret.error_message = str(e)

    return ret