from lib import common
from lib import level_const as level
import botocore.exceptions
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

def get_instance_usage_by_region(client, region):
    try:
        number_of_instances = sum(len(reservation['Instances']) for reservation in client.describe_instances()['Reservations'])
        return region, str(number_of_instances)
    except botocore.exceptions.ClientError as e:
        logging.error(f"Error getting instance usage for region {region}: {str(e)}", exc_info=True)
        return region, "ERR"

def check_multiregion_instance_usage(session, translator) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['Region', 'Instance Usage']

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
            executor.submit(get_instance_usage_by_region, session.client('ec2', region_name=region), region)
            for region in regions
        ]

        ret.level = level.info
        ret.msg = translator.translate("info_msg")
        
        for future in as_completed(futures):
            region, number_of_instances = future.result()
            if number_of_instances == "ERR":
                ret.level = level.error
                ret.msg = translator.translate("retrieval_error")
            ret.result_rows.append([region, number_of_instances])

    return ret