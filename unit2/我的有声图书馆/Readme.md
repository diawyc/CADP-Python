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
## 安装mysql
```
sudo yum install mysql -y
```
## 连接RDS mysql
```
mysql -h mydbinstance.cxtmwuenuqe2.rds.cn-northwest-1.amazonaws.com.cn -P 3306 -u root -p
```
```
      CREATE DATABASE usermanage
      DEFAULT CHARACTER SET utf8mb4
      DEFAULT COLLATE utf8mb4_general_ci;
```
## 查看所有的数据库
```
SHOW DATABASES;
```

## 在usermanage数据库中创建数据表user
```
USE usermanage;
create table books (BID int auto_increment primary key, title varchar(256) unique, author varchar(64), language varchar(16), contents longtext, image varchar(16), audio varchar(16))
SHOW TABLES;    

```
##插入admin的信息,其中口令密码为1
```
INSERT INTO user (id, user, pwd, email)
VALUES (1, 'admin', '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', '123@admin.com');
select * from user;
```
## 将本地app目录上传至S3上
```
local_folder_name=polly
s3_bucket_name=lessonbucket
```
```
aws s3 cp $local_folder_name s3://$s3_bucket_name/$local_folder_name/ --recursive
aws s3 ls $s3_bucket_name
```
## 在EC2上创建一个目录后,下载S3上的代码
```
region=cn-northwest-1
local_folder_name=polly
s3_bucket_name=lessonbucket
```
```
sudo aws s3 cp s3://$s3_bucket_name/polly . --recursive --region=$region
```
## 启动Web程序
```
python3 /usr/bin/mytest/polly/server.py
```
