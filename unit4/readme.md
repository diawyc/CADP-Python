## 配置S3
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


```
local_folder_name='html'
s3_bucket_name='unit4-web'
```
```
aws s3 cp $local_folder_name s3://$s3_bucket_name/ --recursive
aws s3 ls $s3_bucket_name
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
