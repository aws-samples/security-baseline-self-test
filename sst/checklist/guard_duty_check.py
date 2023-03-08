from lib import common, language
from lib import level_const as level
import botocore.exceptions
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import logging, traceback

def get_guard_duty_configuration(client, region) -> tuple:
    try:
        detectors = client.list_detectors()["DetectorIds"]
    except client.exceptions.BadRequestException as e:
        logging.error(traceback.format_exc())
        return region, "ERR"
    except client.exceptions.InternalServerErrorException as e:
        logging.error(traceback.format_exc())
        return region, "ERR"
    except botocore.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        return region, "ERR"
    else:
        return region, len(detectors)

def check_guard_duty_enabled(session, selected_language) -> common.CheckResult:

    translator = language.translation("guardduty_enabled", selected_language)

    print(translator.checking())
    
    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['Region', 'GuardDuty Setting']

    ec2_client = session.client('ec2')

    try:
        regions = common.get_opted_in_regions(ec2_client)
    except botocore.exceptions.ClientError as e:
        ret.level = level.error
        ret.msg = "Unexpected Error"
        ret.result_rows.append(['ERR', 'ERR'])
        return ret
    else:

        thread_executor = ThreadPoolExecutor()

        futures = []
        for region in regions:

            guardduty_client = session.client('guardduty', region_name=region)

            futures.append(thread_executor.submit(get_guard_duty_configuration, guardduty_client, region))
        
        nums_of_guardduty_enabled = 0

        for future in concurrent.futures.as_completed(futures):
            region, number_of_detectors = future.result()

            if number_of_detectors == "ERR":
                ret.level = level.error
                ret.msg = "Failed to retrieve GuardDuty status from some regions."
                ret.result_rows.append([region, "ERR"])
            elif number_of_detectors > 0:
                nums_of_guardduty_enabled += 1
                ret.result_rows.append([region, "Activated"])
            else:
                ret.result_rows.append([region, "Inactivated"])

        ret.level = level.info
        if nums_of_guardduty_enabled > 0:
            ret.msg = translator.is_activated()
        else:
            ret.msg = translator.is_not_activated()

        return ret