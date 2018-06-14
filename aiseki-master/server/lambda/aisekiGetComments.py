import boto3
from boto3.dynamodb.conditions import Key, Attr
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table    = dynamodb.Table('aiseki_comments')
    response = table.query(
        KeyConditionExpression=Key('aiseki_id').eq(event['params']['path']['aiseki_id']) & Key('created').gt(0),
        Limit=100,
        # ExclusiveStartKey=response['LastEvaluatedKey']),
        ScanIndexForward=False
    )

    return response['Items']
