from lib import common
from lib import level_const as level
import botocore.exceptions
import logging, traceback

def check_multi_retion_trail_enabled(session) -> common.CheckResult:

    ret = common.CheckResult()

    ret.title = "Cloudtrail의 Multi-Region Logging 설정 확인"
    ret.result_cols = ['Trail', 'Multi-Region Logging']

    client = session.client('cloudtrail')

    trails = []
    try:
        trails = client.describe_trails()["trailList"]
    except client.exceptions.UnsupportedOperationException:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "지원하지 않는 작업입니다."
        ret.result_rows.append(["ERR", "ERR"])
    except client.exceptions.OperationNotPermittedException:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "수행할 수 없습니다."
        ret.result_rows.append(["ERR", "ERR"])
    except client.exceptions.NoManagementAccountSLRExistsException:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "관리계정의 Service Linked Role 이 존재하지 않습니다."
        ret.result_rows.append(["ERR", "ERR"])
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "예기치 못한 에러가 발생했습니다."
        ret.result_rows.append(["ERR", "ERR"])

    if len(trails) == 0:
        ret.level = level.danger
        ret.msg = '''생성된 Trail 이 없습니다.Trail을 생성해 해주세요.&nbsp(<a href="https://docs.aws.amazon.com/ko_kr/prescriptive-guidance/latest/aws-startup-security-baseline/acct-07.html" target="_blank" style="overflow:hidden;word-break:break-all;">Trail 생성방법</a>)'''
        ret.result_rows.append(["-", "-"])
    else :

        logging_disabled_counter = 0
        
        for trail in trails:
            trail_arn = trail["TrailARN"]

            is_multi_region = False

            try:
                is_multi_region = client.get_trail(Name=trail_arn)['Trail']["IsMultiRegionTrail"]
            except botocore.exceptions.ClientError as e:
                logging.error(traceback.format_exc())
                ret.level = level.error
                ret.msg = "예기치 못한 에러가 발생했습니다."
                ret.result_rows.append([trail_arn, "ERR"])
            else:
                if is_multi_region == False:
                    ret.level = level.warning
                    logging_disabled_counter += 1
                else:
                    pass
                ret.result_rows.append([trail_arn, str(is_multi_region)])
        
        if logging_disabled_counter == len(trails):
            ret.level = level.danger
            ret.msg = "모든 Trail 의 multi-region logging 설정이 비활성화 되어 있습니다."
        elif logging_disabled_counter > 0 and logging_disabled_counter < len(trails):
            ret.level = level.warning
            ret.msg = "일부 Trail 의 multi-region logging 설정이 비활성화 되어 있습니다."
        else:
            ret.level = level.success
            ret.msg = "모든 Trail 의 multi-region logging 설정이 활성화되어 있습니다."

    return ret