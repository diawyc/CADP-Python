# 安装Python开发程序

```
sudo yum install python3 python3-pip
pip3 install --upgrade pip
pip3 install --user flask
pip3 install --user pymysql
pip3 install --user boto3

```
# 升级到Python 11
```
sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel

sudo wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
```

## 创建配置文件
```
printf "host,user,password\nmydbinstance.cxtmwuenuqe2.rds.cn-northwest-1.amazonaws.com.cn,root,mypassword" > mySql.csv
```

## 将本地app目录上传至S3上
```
local_folder_name=AudioBook
s3_bucket_name=lessonbucket
```
```
aws s3 cp $local_folder_name s3://$s3_bucket_name/$local_folder_name/ --recursive
aws s3 ls $s3_bucket_name
```
## 在EC2上创建一个目录后,下载S3上的代码
```
region=cn-northwest-1
local_folder_name=AudioBook
s3_bucket_name=lessonbucket
```
```
sudo mkdir AudioBook
cd $local_folder_name
sudo aws s3 cp s3://$s3_bucket_name/$local_folder_name . --recursive --region=$region
```
## 启动Web程序
### 给写进文件夹的权限
```
sudo chown -R ssm-user:ssm-user static
```
```
python3 /usr/bin/mytest/$local_folder_name/server.py
```
