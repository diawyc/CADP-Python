import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    user = dynamodb.Table('User')
    
    try:
        contents = user.scan()
        
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
