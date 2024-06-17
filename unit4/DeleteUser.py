import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    user = dynamodb.Table('User')
    
    try:
        ID = 0
        login_info = {}
        contents = user.scan(FilterExpression=Attr("ID").eq(event["id"]))
        msg = user.delete_item(Key={
            "ID": contents["Items"][0]["ID"],
            "Name": contents["Items"][0]["Name"]
        })
        
        return {
            'statusCode': 200,
            'body': msg
        }
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': str(e)
        }
