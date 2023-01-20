from lib import common
from lib import level_const as level
import botocore.exceptions
from concurrent.futures import ThreadPoolExecutor
import logging, traceback
import concurrent.futures

def get_instance_usage_by_region(client, region) -> tuple:

    number_of_instances = 0
    try:
        reservation_list = client.describe_instances()['Reservations']
        for reservation in reservation_list:
            number_of_instances += len(reservation['Instances'])
    except botocore.exceptions.ClientError as e:
        logging.error(traceback.format_exc())
        return region, "ERR"
    else:
        return region, str(number_of_instances)

def check_multiregion_instance_usage(session) -> common.CheckResult:

    ret = common.CheckResult()

    ret.title = "리전 별 사용중인 인스턴스 수"
    ret.result_cols = ['Region', '사용중인 인스턴스 수']

    ec2_client = session.client('ec2')

    try:
        regions = common.get_opted_in_regions(ec2_client)
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "예기치 못한 에러가 발생했습니다."
        ret.result_rows.append(['ERR', 'ERR'])
        return ret
    else:
        futures = []
        for region in regions:
            ec2_client_by_region = session.client('ec2', region_name=region)

            thread_executor = ThreadPoolExecutor()

            futures.append(thread_executor.submit(get_instance_usage_by_region, ec2_client_by_region, region))

        ret.result_rows = []
        ret.level = level.info
        ret.msg = '''리전별 인스턴스 사용현황을 확인해주세요.&nbsp<a href="https://us-east-1.console.aws.amazon.com/ec2globalview/home" target="_blank" style="overflow:hidden;word-break:break-all;">EC2 Global View</a> 를 이용하여 확인할 수 있습니다.'''
        for future in concurrent.futures.as_completed(futures):
            region, number_of_instance = future.result()

            if number_of_instance == "ERR":
                ret.level = level.error
                ret.msg = "리전별 인스턴스 정보를 조회하는 중 예기치못한 에러가 발생했습니다."
            else:
                pass
            
            ret.result_rows.append([region, number_of_instance])

    return ret