from lib import common
from lib import level_const as level
import botocore.exceptions
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

def get_guard_duty_configuration(client, region):
    try:
        detectors = client.list_detectors()["DetectorIds"]
        return region, len(detectors)
    except (client.exceptions.BadRequestException,
            client.exceptions.InternalServerErrorException,
            botocore.exceptions.ClientError) as e:
        logging.error(f"Error getting GuardDuty configuration for region {region}: {str(e)}", exc_info=True)
        return region, "ERR"

def check_guard_duty_enabled(session, translator) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['Region', 'GuardDuty Setting']

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

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(get_guard_duty_configuration, session.client('guardduty', region_name=region), region)
            for region in regions
        ]

        nums_of_guardduty_enabled = 0
        error_occurred = False

        for future in as_completed(futures):
            region, number_of_detectors = future.result()
            if number_of_detectors == "ERR":
                error_occurred = True
                ret.result_rows.append([region, "ERR"])
            elif number_of_detectors > 0:
                nums_of_guardduty_enabled += 1
                ret.result_rows.append([region, "Activated"])
            else:
                ret.result_rows.append([region, "Inactivated"])

    if error_occurred:
        ret.level = level.error
        ret.msg = translator.translate("retrieval_error")
    else:
        ret.level = level.info
        if nums_of_guardduty_enabled > 0:
            ret.msg = translator.translate("is_activated")
        else:
            ret.msg = translator.translate("is_not_activated")

    return ret