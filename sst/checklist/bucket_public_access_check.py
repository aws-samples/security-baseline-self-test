from lib import common
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
            return level.danger, [bucket_name, "모두 허용"]
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
            return level.danger, [bucket_name, "모두 허용"]
        elif public_access_block_policy_counter > 0 and public_access_block_policy_counter < nums_of_public_access_block_policies:
            return level.warning, [bucket_name, "일부 허용"]
        elif public_access_block_policy_counter == nums_of_public_access_block_policies:
            return level.success, [bucket_name, "모두 차단"]
        else :
            return level.error, [bucket_name, "예상치 못한 문제가 발생했습니다."]

def check_bucket_public_access(session) -> common.CheckResult:

    ret = common.CheckResult()

    ret.title = "개별 Bucket 수준 S3 Bucket Public Access 설정 확인"
    ret.result_cols = ['Bucket Name', 'Public Access Setting']

    s3_client = session.client('s3')

    bucket_list = []
    try:
        bucket_list = s3_client.list_buckets()["Buckets"]
    except botocore.exceptions.ClientError:
        logging.error(traceback.format_exc())
        ret.level = level.error
        ret.msg = "예기치 못한 에러가 발생했습니다."
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
            ret.msg = "S3 Bucket의 Public Access 정책이 모두 차단되어 있습니다."
        elif level_flag == level.warning:
            ret.msg = "S3 Bucket Public Access 정책이 일부 허용되어 있습니다. 차단하는 것이 보다 안전합니다."
        elif level_flag == level.danger:
            ret.msg = "S3 Bucket Public Access 정책이 모두 허용되어 있습니다. 차단하는 것이 보다 안전합니다."
        else:
            if len(bucket_list) > 1000:
                ret.msg = "최대 점검가능한 버킷 수({MAXIMUM_NUMBER_OF_BUCKET_LIMIT})을 초과했습니다. 점검이 되지 않은 버킷은 수동으로 점검하시거나 AWS Trusted Advisor를 이용해주세요.".format(MAXIMUM_NUMBER_OF_BUCKET_LIMIT=MAXIMUM_NUMBER_OF_BUCKET_LIMIT)
            else:
                ret.msg = "잘못된 요청입니다."

        ret.level = level_flag

    return ret