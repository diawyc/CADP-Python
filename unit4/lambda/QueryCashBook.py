import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    user = dynamodb.Table('CashBook')
    
    try:
        ID = 0
        login_info = {}
        contents = user.scan(FilterExpression=Attr("Uggser_ID").eq(event["id"]))
        
        return {
            'statusCode': 200,
            'body': contents["Items"]
        }
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': str(e)
        }
