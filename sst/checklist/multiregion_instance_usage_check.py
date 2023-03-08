from lib import common, language
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

def check_multiregion_instance_usage(session, selected_language) -> common.CheckResult:

    translator = language.translation("multi_region_instance_usage", selected_language)

    print(translator.checking())

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['Region', 'instance usage']

    ec2_client = session.client('ec2')

    try:
        regions = common.get_opted_in_regions(ec2_client)
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Unexpected Error"
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
        ret.msg = translator.info_msg()
        for future in concurrent.futures.as_completed(futures):
            region, number_of_instance = future.result()

            if number_of_instance == "ERR":
                ret.level = level.error
                ret.msg = "Unexpected Error"
            else:
                pass
            
            ret.result_rows.append([region, number_of_instance])

    return ret