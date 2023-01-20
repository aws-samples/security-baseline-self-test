import boto3
import datetime
import os
import logging
import botocore.exceptions

API_CALL_COOLTIME = 5

class Ret:
    def __init__(self) -> None:
        self.status_code = 200
        self.body = "success"
        self.headers = {'Content-Type': 'text/html;charset=UTF-8'}

    def to_dict(self) -> dict:
        return {
            'statusCode':self.status_code,
            'body':self.body,
            'headers':self.headers
        }

def is_too_many_requests(s3_client, bucket_name) -> tuple:
    
    last_modified = ''
    try:
        last_modified = s3_client.get_object(Bucket=bucket_name, Key="temp")['LastModified']
        if datetime.datetime.now(datetime.timezone.utc) - last_modified < datetime.timedelta(minutes=API_CALL_COOLTIME):
            return last_modified, True
        else:
            return last_modified, False
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            # This error is raised at the first test executing.
            return last_modified, False
        else:
            raise e

def lambda_handler(event, context):

    logging.info('Invoked')

    ret = Ret()

    bucket_name = os.environ["Bucket"][13:]
    lambda_client = boto3.client('lambda')
    sns_client = boto3.client('sns')
    sns_topic = os.environ['Topic']
    s3_client = boto3.client('s3')
    
    try:
        subscriptions = sns_client.list_subscriptions_by_topic(TopicArn = sns_topic)["Subscriptions"]
    except sns_client.exceptions.NotFoundException:
        ret.status_code = 400
        ret.body = 'AWS SNS Topic 을 찾을 수 없습니다.'
        return ret.to_dict()
    except sns_client.exceptions.AuthorizationErrorException:
        ret.status_code = 401
        ret.body = 'Unauthorized'
        return ret.to_dict()
    except sns_client.exceptions.InternalErrorException:
        ret.status_code = 500
        ret.body = 'Internal Error'
        return ret.to_dict()
    else:
        sns_endpoint = list(map(lambda x: x["Endpoint"], subscriptions))

        for subscription in subscriptions:
            # This logic suppose to a new and a unique subscription in a sns topic which created by this sample code.
            if subscription["SubscriptionArn"] != "PendingConfirmation":
                break
            else:
                ret.status_code = 202
                ret.body = '이메일로 발송된 SNS Topic 구독에 대한 알림을 먼저 확인하신 뒤, 다시 진행해주세요.({sns_endpoint})'.format(sns_endpoint=sns_endpoint)
                return ret.to_dict()

        last_modified = ''
        flag = ''

        try:
            last_modified, flag = is_too_many_requests(s3_client, bucket_name)
        except Exception as e:
            ret.status_code = 500
            ret.body = "예기치 못한 에러가 발생했습니다.({e})".format(e=e)
            return ret.to_dict()

        if flag == True:
            rest_cooltime = datetime.timedelta(minutes=API_CALL_COOLTIME)-(datetime.datetime.now(datetime.timezone.utc) - last_modified)
            ret.status_code = 429
            ret.body = "마지막 점검 요청 후 {API_CALL_COOLTIME}분 이내에 다시 점검을 요청할 수 없습니다. {rest_cooltime} 뒤에 다시 시도해주세요.".format(API_CALL_COOLTIME=API_CALL_COOLTIME, rest_cooltime=rest_cooltime)

        else:
            s3_client.put_object(Bucket=bucket_name, Key="temp", Body="") # You can use last modified datetime of this object to block too many lambda function invoke.

            sst_function = os.environ["SST"].split(":")[-1]
            lambda_client.invoke(FunctionName=sst_function, InvocationType='Event')

            ret.body = '''점검중 입니다. 점검이 완료되면 등록한 이메일로 알려드리겠습니다. 감사합니다.'''

        logging.info('Successfully Finished')
        return ret.to_dict()