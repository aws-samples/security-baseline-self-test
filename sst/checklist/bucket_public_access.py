from lib import common
from lib import level_const as level
import botocore.exceptions
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

MAXIMUM_NUMBER_OF_BUCKET_LIMIT = 1000

def get_bucket_info(client, bucket_name) -> tuple:
    try:
        bucket_info = client.get_public_access_block(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            return level.danger, [bucket_name, "All Allowed"]
        else:
            logging.error(f"Error getting public access block for bucket {bucket_name}: {str(e)}", exc_info=True)
            return level.error, [bucket_name, "ERR"]
    
    public_access_block_policy_counter = sum(
        1 for policy_status in bucket_info["PublicAccessBlockConfiguration"].values()
        if policy_status
    )
    nums_of_public_access_block_policies = len(bucket_info["PublicAccessBlockConfiguration"])
    
    if public_access_block_policy_counter == 0:
        return level.danger, [bucket_name, "All Allowed"]
    elif 0 < public_access_block_policy_counter < nums_of_public_access_block_policies:
        return level.warning, [bucket_name, "Partially Allowed"]
    elif public_access_block_policy_counter == nums_of_public_access_block_policies:
        return level.success, [bucket_name, "All Blocked"]
    else:
        return level.error, [bucket_name, "Unexpected Exception"]

def check_bucket_public_access(session, translator) -> common.CheckResult:
    logging.info(translator.translate("checking"))
    
    ret = common.CheckResult()
    ret.title = translator.translate("title")
    ret.result_cols = ['Bucket Name', 'Public Access Setting']
    
    s3_client = session.client('s3')
    
    try:
        bucket_list = s3_client.list_buckets()["Buckets"]
    except botocore.exceptions.ClientError as e:
        logging.error(f"Error listing buckets: {str(e)}", exc_info=True)
        ret.level = level.error
        ret.msg = translator.translate("unexpected_error")
        ret.result_rows.append(['ERR', 'ERR'])
        ret.error_message = str(e)
        return ret

    with ThreadPoolExecutor() as thread_executor:
        futures = []
        if len(bucket_list) > MAXIMUM_NUMBER_OF_BUCKET_LIMIT:
            ret.level = level.error
            ret.msg = translator.translate("bucket_limit_warning").format(MAXIMUM_NUMBER_OF_BUCKET_LIMIT)
            bucket_list = bucket_list[:MAXIMUM_NUMBER_OF_BUCKET_LIMIT]
        
        for bucket in bucket_list:
            futures.append(thread_executor.submit(get_bucket_info, s3_client, bucket['Name']))

        level_flag = level.success
        for future in as_completed(futures):
            result_level, result = future.result()
            if result_level > level_flag:
                level_flag = result_level
            ret.result_rows.append(result)

    if level_flag == level.success:
        ret.msg = translator.translate("success")
    elif level_flag == level.warning:
        ret.msg = translator.translate("warning")
    elif level_flag == level.danger:
        ret.msg = translator.translate("danger")
    elif ret.level != level.error:  # Don't overwrite bucket limit warning
        ret.msg = translator.translate("error")

    ret.level = level_flag
    return ret