## 配置S3
```
aws s3
```
## 创建Lambda function
### 创建lambda使用的Role
参数指定
```
aws s3
```
## lambda function
```
name='lvli-event-dev'
runtime='python3.11'
filename='login.zip'
rolearn='arn:aws-cn:iam::'$accountid':role/service-role/'$rolename
region='cn-northwest-1'

```

```
lambdaarn=$(aws lambda create-function \
    --function-name $name \
    --runtime $runtime \
    --zip-file fileb://$filename \
    --handler index.lambda_handler \
    --role $rolearn --region=$region --no-cli-pager --query 'FunctionArn' --output text)
echo $lambdaarn
```
