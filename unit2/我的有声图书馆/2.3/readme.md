## 将本地AudioBook的上一层目录上传至S3上
```
local_folder_name=AudioBook
s3_bucket_name=lessonbucket
```
```
aws s3 cp $local_folder_name s3://$s3_bucket_name/$local_folder_name/ --recursive
aws s3 ls $s3_bucket_name
```
## 在EC2上创建一个AudioBook目录后,下载S3上的代码
```
region=cn-northwest-1
local_folder_name=AudioBook
s3_bucket_name=lessonbucket
```
```

sudo aws s3 cp s3://$s3_bucket_name/AudioBook . --recursive --region=$region
```
```
sudo chown -R ssm-user:ssm-user static
```
## 启动Web程序
```
python3 server.py
```
```
python3 initialize.py
```
```
http://52.82.100.56:5000/insertBook
```
```
pid=
sudo lsof -i :5000
sudo kill -9 $pid
```
