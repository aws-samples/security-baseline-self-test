from lib import common
from lib import level_const as level
import botocore.exceptions
import logging

def check_multi_region_trail_enabled(session, translator) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['Trail', 'Multi-Region Logging']

    client = session.client('cloudtrail')

    try:
        trails = client.describe_trails()["trailList"]
    except (client.exceptions.UnsupportedOperationException,
            client.exceptions.OperationNotPermittedException,
            client.exceptions.NoManagementAccountSLRExistsException,
            botocore.exceptions.ClientError) as e:
        logging.error(f"Error describing trails: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("describe_trails_error")
        ret.result_rows.append(["ERR", "ERR"])
        ret.error_message = str(e)
        return ret

    if not trails:
        ret.level = level.danger
        ret.msg = translator.translate("no_trail")
        ret.result_rows.append(["-", "-"])
        return ret

    logging_disabled_counter = 0
    for trail in trails:
        trail_arn = trail["TrailARN"]
        try:
            is_multi_region = client.get_trail(Name=trail_arn)['Trail']["IsMultiRegionTrail"]
            ret.result_rows.append([trail_arn, str(is_multi_region)])
            if not is_multi_region:
                logging_disabled_counter += 1
        except botocore.exceptions.ClientError as e:
            logging.error(f"Error getting trail {trail_arn}: {str(e)}", exc_info=True)
            ret.result_rows.append([trail_arn, "ERR"])
            ret.level = level.error
            ret.msg = translator.translate("get_trail_error")
            ret.error_message = str(e)

    if ret.level != level.error:
        if logging_disabled_counter == len(trails):
            ret.level = level.danger
            ret.msg = translator.translate("danger")
        elif logging_disabled_counter > 0:
            ret.level = level.warning
            ret.msg = translator.translate("warning")
        else:
            ret.level = level.success
            ret.msg = translator.translate("success")

    return ret