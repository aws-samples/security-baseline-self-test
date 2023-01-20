from lib import common
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

def check_guard_duty_enabled(session) -> common.CheckResult:
    ret = common.CheckResult()

    ret.title = "GuardDuty 를 사용하도록 설정했는지 확인"
    ret.result_cols = ['Region', 'GuardDuty 설정']

    ec2_client = session.client('ec2')

    try:
        regions = common.get_opted_in_regions(ec2_client)
    except botocore.exceptions.ClientError as e:
        ret.level = level.error
        ret.msg = "예기치 못한 에러가 발생했습니다."
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
                ret.msg = "일부 또는 전체 리전의 GuardDuty 상태정보를 가져오는데 실패했습니다."
                ret.result_rows.append([region, "ERR"])
            elif number_of_detectors > 0:
                nums_of_guardduty_enabled += 1
                ret.result_rows.append([region, "활성"])
            else:
                ret.result_rows.append([region, "비활성"])

        ret.level = level.info
        if nums_of_guardduty_enabled > 0:
            ret.msg = "한개 이상의 리전에 GuardDuty가 활성화 되어 있습니다."
        else:
            ret.msg = "GuardDuty가 활성화 된 리전이 없습니다."

        return ret