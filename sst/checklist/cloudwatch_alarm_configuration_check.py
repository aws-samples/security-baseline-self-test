from lib import common
from lib import level_const as level
import botocore.exceptions
from concurrent.futures import ThreadPoolExecutor
import logging, traceback

def get_cloudwatch_alarms(client, region) -> tuple:
    try:
        alarms = client.describe_alarms()["MetricAlarms"]
    except client.exceptions.InvalidNextToken:
        logging.error(traceback.format_exc())
        return region, "ERR"
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())
        return region, "ERR"
    else:
        return region, alarms

def check_cloudwatch_alarm_configuration(session) -> common.CheckResult:
    ret = common.CheckResult()

    ret.title = "CloudWatch에 중요 이벤트 알림 설정 확인"
    ret.result_cols = ['Region', 'Name']

    ec2_client = session.client('ec2')
    
    try:
        regions = common.get_opted_in_regions(ec2_client)
    except botocore.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "예기치 못한 에러가 발생했습니다."
        ret.result_rows.append(['ERR', 'ERR'])
        return ret
    else:

        thread_executor = ThreadPoolExecutor()
        futures = []
        for region in regions:
            cloudwatch_client = session.client('cloudwatch', region_name=region)

            futures.append(thread_executor.submit(get_cloudwatch_alarms, cloudwatch_client, region))

        is_alarm_exist = False
        ret.result_rows = []
        for future in futures:
            region, alarms = future.result()

            if alarms == "ERR":
                logging.error(traceback.format_exc())
                ret.level = level.error
                ret.msg = "일부 또는 전체 리전의 알림 구성조회에 실패했습니다."
                ret.result_rows.append([region, 'ERR'])
                continue
            else:
                if len(alarms) > 0:
                    is_alarm_exist = True
                    for alarm in alarms:
                        ret.result_rows.append([region, alarm['AlarmName']])
                else:
                    pass
        
        if is_alarm_exist == True:
            ret.level = level.success
            ret.msg = "CloudWatch 알림이 구성되어 있습니다. 비용 알림, 루트 계정 활동 알림이 있는지 확인해주세요."
        else:
            ret.level = level.warning
            ret.msg = '''CloudWatch 알림이 구성되어 있지 않습니다. &nbsp<a href="https://catalog.workshops.aws/startup-security-baseline/en-US/b-securing-your-account/7-configurealarms" target="_blank" style="overflow:hidden;word-break:break-all;">워크샵</a>을 통해 비용 알림, 루트 계정 활동 알림을 설정해보세요.'''

    return ret