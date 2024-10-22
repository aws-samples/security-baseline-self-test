from lib import common
from lib import level_const as level
import botocore.exceptions
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

def get_cloudwatch_alarms(client, region):
    try:
        alarms = client.describe_alarms()["MetricAlarms"]
        return region, alarms
    except (client.exceptions.InvalidNextToken, botocore.exceptions.ClientError) as e:
        logging.error(f"Error getting CloudWatch alarms for region {region}: {str(e)}", exc_info=True)
        return region, "ERR"

def check_cloudwatch_alarm_configuration(session, translator) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['Region', 'Name']

    ec2_client = session.client('ec2')
    
    try:
        regions = common.get_opted_in_regions(ec2_client)
    except botocore.exceptions.ClientError as e:
        logging.error(f"Error getting opted-in regions: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("unexpected_error")
        ret.result_rows.append(['ERR', 'ERR'])
        ret.error_message = str(e)
        return ret

    with ThreadPoolExecutor() as thread_executor:
        futures = [
            thread_executor.submit(get_cloudwatch_alarms, session.client('cloudwatch', region_name=region), region)
            for region in regions
        ]

        is_alarm_exist = False
        ret.result_rows = []
        error_occurred = False

        for future in as_completed(futures):
            region, alarms = future.result()
            if alarms == "ERR":
                error_occurred = True
                ret.result_rows.append([region, 'ERR'])
            elif alarms:
                is_alarm_exist = True
                ret.result_rows.extend([region, alarm['AlarmName']] for alarm in alarms)

    if error_occurred:
        ret.level = level.error
        ret.msg = translator.translate("retrieval_error")
    elif is_alarm_exist:
        ret.level = level.success
        ret.msg = translator.translate("alarm_exist")
    else:
        ret.level = level.warning
        ret.msg = translator.translate("alarm_not_exist")

    return ret