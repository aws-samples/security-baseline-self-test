from lib import common, language
from lib import level_const as level
import botocore.exceptions
import logging, traceback

def check_trail_enabled(session, selected_language) -> common.CheckResult:

    translator = language.translation("trail_enabled", selected_language)

    print(translator.checking())

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['Trail', 'Is Logging']

    client = session.client('cloudtrail')

    ret.level = level.success

    trails = []
    try:
        trails = client.describe_trails()["trailList"]
    except client.exceptions.UnsupportedOperationException:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Unsupported Operation Error"
        ret.result_rows.append(["ERR", "ERR"])
    except client.exceptions.OperationNotPermittedException:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Operation Not Permitted"
        ret.result_rows.append(["ERR", "ERR"])
    except client.exceptions.NoManagementAccountSLRExistsException:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "No Management Account Service Linked Role Exists"
        ret.result_rows.append(["ERR", "ERR"])
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Unexpected Error"
        ret.result_rows.append(["ERR", "ERR"])

    if len(trails) == 0:
        ret.level = level.danger
        ret.msg = translator.danger()
        ret.result_rows.append(["-", "-"])
    else :

        logging_disabled_counter = 0
        
        for trail in trails:
            trail_arn = trail["TrailARN"]

            is_logging = False
            
            try:
                is_logging = client.get_trail_status(Name=trail_arn)["IsLogging"]
            except botocore.exceptions.ClientError:
                logging.error(traceback.format_exc())
                ret.level = level.error
                ret.msg = "Unexpected Error"
                ret.result_rows.append([trail_arn, "ERR"])
            else:
                if is_logging == False:
                    ret.result_rows.append([trail_arn, str(is_logging)])
                    logging_disabled_counter += 1
        
        if logging_disabled_counter == len(trails):
            ret.level = level.danger
            ret.msg = translator.danger()
        elif logging_disabled_counter > 0 and logging_disabled_counter < len(trails):
            ret.level = level.warning
            ret.msg = translator.warning()
        else:
            ret.level = level.success
            ret.msg = translator.success()

    return ret