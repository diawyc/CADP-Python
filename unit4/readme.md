## 配置存放HTML网站文件的S3
```
region=cn-northwest-1
s3_bucket_name='unit4-web'
```
```
aws s3api create-bucket \
    --bucket $s3_bucket_name \
    --region $region \
    --create-bucket-configuration LocationConstraint=$region
```
### cloudfront
```
s3url='unit4-web.s3.cn-northwest-1.amazonaws.com.cn'
```

```
aws cloudfront create-distribution \
    --origin-domain-name $s3url \
    --default-root-object index.html \
    --priced-class PriceClass_200 \
    --enabled \
    --default-cache-behavior-forwarded-values '{"QueryString": false}' \
    --viewer-protocol-policy allow-all \
    --origin-protocol-policy http-only
```

```
local_folder_name='html'
s3_bucket_name='unit4-web'
```
```
aws s3 cp $local_folder_name s3://$s3_bucket_name/ --recursive
aws s3 ls $s3_bucket_name
```


## 创建DynamoDB
```
region=cn-northwest-1
name='User'
```
```
aws dynamodb create-table \
    --table-name $name \
    --attribute-definitions \
        AttributeName=ID,AttributeType=N \
        AttributeName=Name,AttributeType=S \
    --key-schema \
        AttributeName=ID,KeyType=HASH \
        AttributeName=Name,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST
```
```
region=cn-northwest-1
name='CashBook'
```
```
aws dynamodb create-table \
    --table-name $name \
    --attribute-definitions \
        AttributeName=ID,AttributeType=N \
        AttributeName=User_ID,AttributeType=S \
    --key-schema \
        AttributeName=ID,KeyType=HASH \
        AttributeName=User_ID,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST
```

## create API gateway
```
name=MyAPI
api=$(aws apigateway create-rest-api --name $name --description "unit4 api gateawy for lambda" --endpoint-configuration '{"types":["REGIONAL"]}' --region $region --query 'id' --output text)
echo $api
resource=$(aws apigateway get-resources --rest-api-id $api --quer 'items[0].id' --output text)
echo $resource
```



## 创建Lambda function
### 创建lambda使用的两个Role

```
rolename='DynamoDBReadOnlyAccess_Role'
rolearn1=$(aws iam create-role --role-name $rolename --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' --query 'Role.Arn' --output text)
echo $rolearn1
aws iam attach-role-policy \
    --role-name $rolename \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

rolename='DynamoDBFullAccess_Role'
rolearn2=$(aws iam create-role --role-name $rolename --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' --query 'Role.Arn' --output text)
echo $rolearn2
aws iam attach-role-policy \
    --role-name $rolename \
    --policy-arn arn:aws-cn:iam::aws:policy/AmazonDynamoDBFullAccess \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

Output
```
arn:aws-cn:iam::693658368441:role/DynamoDBReadOnlyAccess_Role
arn:aws-cn:iam::693658368441:role/DynamoDBFullAccess_Role
```

## lambda function
```
name='login'
filename='login.py.zip'
rolearn='arn:aws-cn:iam::693658368441:role/DynamoDBReadOnlyAccess_Role'
```
```
name='QueryCashBook'
filename='QueryCashBook.py.zip'
rolearn='arn:aws-cn:iam::693658368441:role/DynamoDBReadOnlyAccess_Role'
```
```
name='QueryUser'
filename='QueryUser.py.zip'
rolearn='arn:aws-cn:iam::693658368441:role/DynamoDBReadOnlyAccess_Role'
```
```
name='InsertUser'
filename='InsertUser.py.zip'
rolearn='arn:aws-cn:iam::693658368441:role/DynamoDBFullAccess_Role'
```
```
name='DeleteUser'
filename='DeleteUser.py.zip'
rolearn='arn:aws-cn:iam::693658368441:role/DynamoDBFullAccess_Role'
```
```
name='UpdateUser'
filename='UpdateUser.py.zip'
rolearn='arn:aws-cn:iam::693658368441:role/DynamoDBFullAccess_Role'
```
```
name='InsertCashBook'
filename='InsertCashBook.py.zip'
rolearn='arn:aws-cn:iam::693658368441:role/DynamoDBFullAccess_Role'
```

```
runtime='python3.11'
region='cn-northwest-1'
lambdaarn=$(aws lambda create-function \
    --function-name $name \
    --runtime $runtime \
    --zip-file fileb://$filename \
    --handler index.lambda_handler \
    --role $rolearn --region=$region --no-cli-pager --query 'FunctionArn' --output text)
echo $lambdaarn
```
```
resourceid=$(aws apigateway create-resource --rest-api-id $api --parent-id $resource --path-part $name --region $region --quer 'id' --output text)
echo $resourceid
uri='arn:aws-cn:apigateway:cn-northwest-1:lambda:path/2015-03-31/functions/'$lambdaarn'/invocations'
```
创建POST method并关联到lambda
```
aws apigateway put-method --rest-api-id $api --resource-id=$resourceid --http-method POST --authorization-type NONE --region cn-northwest-1

aws apigateway put-integration --rest-api-id $api --resource-id=$resourceid --http-method POST --type AWS --integration-http-method POST --uri $uri --region $region

```
enable CORS
```
aws apigateway put-method --rest-api-id $api --resource-id=$resourceid --http-method OPTIONS --authorization-type NONE --region $region
```
```
aws apigateway put-integration-response --rest-api-id $api --resource-id =$resourceid --http-method OPTIONS  \
--status-code 200  \
--response-parameters '{"method.response.header.Access-Control-Allow-Headers":"'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'","method.response.header.Access-Control-Allow-Methods":"'OPTIONS,GET,PUT,POST,DELETE'","method.response.header.Access-Control-Allow-Origin":"'*'"}'  \
region=$region

```