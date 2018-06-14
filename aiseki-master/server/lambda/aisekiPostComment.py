import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table    = dynamodb.Table('aiseki_comments')
    table.put_item(
        Item={
            "created": int(datetime.now().strftime('%s')),
            "comment": event['body-json']['comment'],
            "aiseki_id":event['body-json']['aiseki_id'],
            "user_name": event['body-json']['user_name'],
            "gender": event['body-json']['gender']
        }
    )
    return 'ok'
