# 安装Python开发程序
p019
```
sudo yum install python3 python3-pip
pip install --upgrade pip
sudo pip install flask
pip install --user pymysql

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
