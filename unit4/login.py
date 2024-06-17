import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    user = dynamodb.Table('User')
    
    try:
        ID = 0
        login_info = {}
        contents = user.scan()
        if len(contents["Items"]) > 0:
            for i in contents["Items"]:
                if event["Name"] == i["Name"] and event["Password"] == i["Password"] and event["id"] == i["ID"]:
                    ID = i["ID"]
                    return {
                        'statusCode': 200,
                        'body': "Login successfully!",
                        "id": ID
                    }
        
        return {
            'statusCode': 200,
            'body': "Login failed!"
        }
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': str(e)
        }
