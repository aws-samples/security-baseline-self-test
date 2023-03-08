from lib import common, language
from lib import level_const as level
import botocore.exceptions
from concurrent.futures import ThreadPoolExecutor
import logging, traceback
import concurrent.futures

def get_bucket_info(client, bucket_name) -> tuple:

    try:
        bucket_info = client.get_public_access_block(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            return level.danger, [bucket_name, "All Allowed"]
        else:
            logging.error(logging.error(traceback.format_exc()))
            return level.error, [bucket_name, "ERR"]
    else:
        public_access_block_policy_counter = 0
        nums_of_public_access_block_policies = len(bucket_info["PublicAccessBlockConfiguration"].items())

        for _, public_access_block_policy_status in bucket_info["PublicAccessBlockConfiguration"].items():
            if public_access_block_policy_status == True:
                public_access_block_policy_counter += 1
            else :
                continue

        if public_access_block_policy_counter == 0:
            return level.danger, [bucket_name, "All Allowed"]
        elif public_access_block_policy_counter > 0 and public_access_block_policy_counter < nums_of_public_access_block_policies:
            return level.warning, [bucket_name, "Partially Allowed"]
        elif public_access_block_policy_counter == nums_of_public_access_block_policies:
            return level.success, [bucket_name, "All Blocked"]
        else :
            return level.error, [bucket_name, "UnExpected Exception"]

def check_bucket_public_access(session, selected_language) -> common.CheckResult:

    translator = language.translation("bucket_public_access", selected_language)

    print(translator.checking())

    ret = common.CheckResult()

    ret.title = translator.title()
    ret.result_cols = ['Bucket Name', 'Public Access Setting']

    s3_client = session.client('s3')

    bucket_list = []
    try:
        bucket_list = s3_client.list_buckets()["Buckets"]
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "Unexpected Error"
        ret.result_rows.append(['ERR', 'ERR'])
        return ret
    else:
        thread_executor = ThreadPoolExecutor()

        futures = []

        MAXIMUM_NUMBER_OF_BUCKET_LIMIT = 1000
        level_flag = level.success

        if len(bucket_list) > MAXIMUM_NUMBER_OF_BUCKET_LIMIT:
            level_flag = level.error
            for x in range(MAXIMUM_NUMBER_OF_BUCKET_LIMIT):
                bucket = bucket_list[x]
                futures.append(thread_executor.submit(get_bucket_info, s3_client, bucket['Name']))
        else:
            for bucket in bucket_list:
                futures.append(thread_executor.submit(get_bucket_info, s3_client, bucket['Name']))
    
        for future in concurrent.futures.as_completed(futures):
            result_level, result = future.result()

            if result_level != level.success:
                if result_level != level.warning:
                    if result_level != level.danger:
                        level_flag = level.error
                    else:
                        level_flag = level.danger
                else :
                    level_flag = level.warning

            ret.result_rows.append(result)

        if level_flag == level.success:
            ret.msg = translator.success()
        elif level_flag == level.warning:
            ret.msg = translator.warning()
        elif level_flag == level.danger:
            ret.msg = translator.danger()
        else:
            if len(bucket_list) > 1000:
                ret.msg = translator.bucket_limit_warning(MAXIMUM_NUMBER_OF_BUCKET_LIMIT)
            else:
                ret.msg = "Invalid Request"

        ret.level = level_flag

    return ret