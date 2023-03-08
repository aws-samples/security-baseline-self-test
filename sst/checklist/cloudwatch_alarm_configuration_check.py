from lib import common, language
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

def check_cloudwatch_alarm_configuration(session, selected_language) -> common.CheckResult:

    translator = language.translation("cloudwatch_alarm_configuation", selected_language)

    print(translator.checking())
    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['Region', 'Name']

    ec2_client = session.client('ec2')
    
    try:
        regions = common.get_opted_in_regions(ec2_client)
    except botocore.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Unexpected Error"
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
                ret.msg = "Failed to retrieve alarm configurations in some or all regions."
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
            ret.msg = translator.alarm_exist()
        else:
            ret.level = level.warning
            ret.msg = translator.alarm_not_exist()

    return ret