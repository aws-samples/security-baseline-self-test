import boto3
from checklist import *
from lib import common, level_const
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import report_generator
import os, datetime, json
import logging, traceback

def execute_test(session) -> tuple:

    iam_client = session.client('iam')
    sts_client = session.client('sts')

    account_id_str = common.get_account_id(sts_client)

    credential_report = common.generate_credential_report(iam_client)

    number_of_whole_test_case = 15

    thread_executor = ThreadPoolExecutor()
    futures = [0 for x in range(number_of_whole_test_case)]

    futures[common.CHECKLIST_INDEX_CONST.ROOT_MFA_SETTING_CHECK.value] = thread_executor.submit(root_mfa_setting_check.check_root_mfa_setting,credential_report)
    futures[common.CHECKLIST_INDEX_CONST.ROOT_USAGE_CHECK.value] = thread_executor.submit(root_usage_check.check_root_usage,credential_report)
    futures[common.CHECKLIST_INDEX_CONST.ROOT_CREDENTIAL_CHECK.value] = thread_executor.submit(root_user_accesskey_check.check_root_accesskey_usage,credential_report)
    futures[common.CHECKLIST_INDEX_CONST.IAM_MFA_SETTING_CHECK.value] = thread_executor.submit(iam_user_mfa_setting_check.check_iam_user_mfa_setting,credential_report)
    futures[common.CHECKLIST_INDEX_CONST.IAM_PASSWORD_POLICY_CHECK.value] = thread_executor.submit(iam_password_policy_check.check_iam_password_policy, session)
    futures[common.CHECKLIST_INDEX_CONST.NON_GROUP_POLICY_CHECK.value] = thread_executor.submit(direct_attached_policy_check.check_iam_direct_attached_policy, session)
    futures[common.CHECKLIST_INDEX_CONST.ALTERNATE_CONTACT_CHECK.value] = thread_executor.submit(alternate_contact_check.check_alternate_contact_filling, session)
    futures[common.CHECKLIST_INDEX_CONST.TRAIL_ENABLED_CHECK.value] = thread_executor.submit(trail_enabled_check.check_trail_enabled, session)
    futures[common.CHECKLIST_INDEX_CONST.MULTIREGION_TRAIL_CHECK.value] = thread_executor.submit(multiregion_trail_enabled_check.check_multi_retion_trail_enabled, session)
    futures[common.CHECKLIST_INDEX_CONST.ACCOUNT_LEVEL_BUCKET_PUBLIC_ACCESS_CHECK.value] = thread_executor.submit(account_level_bucket_public_access_check.check_account_level_bucket_public_access, session)
    futures[common.CHECKLIST_INDEX_CONST.BUCKET_LEVEL_PUBLIC_ACCESS_CHECK.value] = thread_executor.submit(bucket_public_access_check.check_bucket_public_access, session)
    futures[common.CHECKLIST_INDEX_CONST.CLOUDWATCH_ALARM_CONFIGURATION_CHECK.value] = thread_executor.submit(cloudwatch_alarm_configuration_check.check_cloudwatch_alarm_configuration, session)
    futures[common.CHECKLIST_INDEX_CONST.MULTIREGION_INSTANCE_USAGE_CHECK.value] = thread_executor.submit(multiregion_instance_usage_check.check_multiregion_instance_usage, session)
    futures[common.CHECKLIST_INDEX_CONST.GUARD_DUTY_ENABLED_CHECK.value] = thread_executor.submit(guard_duty_check.check_guard_duty_enabled, session)
    futures[common.CHECKLIST_INDEX_CONST.TRUST_ADVISOR_CHECK.value] = thread_executor.submit(trust_advisor_check.check_trust_advisor_configuration)

    result_sort_by_level = {
        level_const.danger:[],
        level_const.warning:[],
        level_const.success:[],
        level_const.error:[],
        level_const.info:[]
    }

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        result_sort_by_level[result.level].append(result)

    return account_id_str, result_sort_by_level

def put_report_to_bucket(bucket_name, html_report, sns_topic) -> common.Ret:

    ret = common.Ret()

    send_email_function = os.environ["EmailReport"].split(":")[-1]
    
    s3_client = boto3.client('s3')
    report_object_name = "security-self-testresult-{generated_date}.html".format(generated_date=datetime.datetime.now().strftime("%Y-%m-%d_h%Hm%Ms%S"))
    encoded = bytes(html_report.encode('UTF-8'))

    lambda_client = boto3.client('lambda')

    try:
        s3_client.put_object(Bucket=bucket_name, Key=report_object_name, Body=encoded)
    except Exception as e:
        logging.error(traceback.format_exc())

        sns_client = boto3.client('sns')
        sns_client.publish(TopicArn=sns_topic, Message='''S3 Bucket 에 리포트를 업로드하던 중 예기치 못한 에러가 발생했습니다.({error})'''.format(error=e))

        ret.status_code = 500
        ret.body = '''InternalException'''
    else:
        try:
            payload = {"ObjectName":report_object_name}
            lambda_client.invoke(FunctionName=send_email_function, InvocationType='Event', Payload=json.dumps(payload))
        except Exception as e:
            logging.error(traceback.format_exc())

            sns_client = boto3.client('sns')
            sns_client.publish(TopicArn=sns_topic, Message='''점검 결과 발신 함수를 실행하는 도중 예기치 못한 에러가 발생했습니다.({error})'''.format(error=e))

            ret.status_code = 500
            ret.body = '''InternalException'''

    return ret

def lambda_handler(event, context) -> common.Ret:

    logging.info('Invoked')

    ret = common.Ret()

    session = boto3.Session()
    sns_topic = os.environ["Topic"]
    bucket_name = os.environ["Bucket"][13:]

    try:
        account_id_str, result_sort_by_level = execute_test(session)
        html_report = report_generator.generate_html_report(account_id_str, result_sort_by_level)
    except Exception as e:
        logging.error(traceback.format_exc())

        sns_client = boto3.client('sns')
        sns_client.publish(TopicArn=sns_topic, Message='''Security Self-Test 진행 중 예기치 못한 에러가 발생했습니다.({error})'''.format(error=e))

        ret.status_code = 500
        ret.body = '''InternalException'''
    else:
        ret = put_report_to_bucket(bucket_name, html_report, sns_topic)

    logging.info('Successfully Finished')

    return ret.to_dict()