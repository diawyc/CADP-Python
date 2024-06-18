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
s3_bucket_name='unit4-web'
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

## lambda function
```
name='login'
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
