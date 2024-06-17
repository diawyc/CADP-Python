import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    
    user = dynamodb.Table('User')
    
    # TODO implement
    ID_Max = 0
    
    try:
        contents = user.scan()
        if len(contents["Items"]) > 0:
            for i in contents["Items"]:
                print(i["ID"])
                if i["ID"]>ID_Max:
                    ID_Max = i["ID"]
        event["ID"] = ID_Max + 1
        if "Name" not in event or "Sex" not in event or "Password" not in event:
            raise Exception("Invalid data!")
        if "Others" in event:
            if not event["Others"]=="":
                l = event["Others"].split(",")
                for i in l:
                    l2 = i.split(":")
                    event[l2[0]]= l2[1]
        del event["Others"]
        
        print(event)
        
        user.put_item(Item=event)
        
        return {
            'statusCode': 200,
            'id': ID_Max + 1,
            'body': "Sign in successfully!"
        }
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': str(e)
        }
