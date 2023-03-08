from lib import common, language
from lib import level_const as level
import botocore.exceptions
import logging, traceback

def check_iam_password_policy(session, selected_language) -> common.CheckResult:

    translator = language.translation("iam_password_policy", selected_language)

    print(translator.checking())
    client = session.client('iam')

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ["Password Policy"]

    try:
        client.get_account_password_policy()
    except client.exceptions.NoSuchEntityException:
        ret.level = level.warning
        ret.msg = translator.warning()
        ret.result_rows.append(["Not Set"])
        return ret
    except client.exceptions.ServiceFailureException:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Service Failure"
        ret.result_rows.append(["ERR"])
        return ret
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Unexpected Error"
        ret.result_rows.append(["ERR"])
        return ret
    else:
        ret.level = level.success
        ret.msg = translator.success()

    return ret
