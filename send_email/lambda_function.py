import boto3
import datetime
import os
import logging

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

def lambda_handler(event, context):

    logging.info('Invoked')

    ret = Ret()

    sns_client= boto3.client("sns")

    topic = os.environ["Topic"]
    bucket_name = os.environ["Bucket"][13:]
    object_name = event["ObjectName"]
    report_url = "https://s3.console.aws.amazon.com/s3/object/{bucket_name}?region=ap-northeast-2&prefix={object_name}".format(bucket_name=bucket_name, object_name=object_name)

    try:
        sns_client.publish(TopicArn=topic, Message='''
        AWS Security Self-Test 결과 리포트가 생성되었습니다. 아래 Link 를 눌러 결과를 다운받으실 수 있습니다.
        (Report Link : {report_url})
        '''.format(report_url=report_url))

        logging.info('Successfully Finished')
        return ret.to_dict()

    except Exception as e:
        logging.error(e)
        ret.status_code = 500
        ret.body = 'SNS publish failed'
        return ret.to_dict()