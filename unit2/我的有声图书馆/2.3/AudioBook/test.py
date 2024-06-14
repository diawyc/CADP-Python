import pymysql
import os
import hashlib

def readMySql():
        mySql = {}
        try:
            with open("mySql.csv", "rt") as fobj:
                rows = fobj.readlines()
                row = rows[1].strip().split(",")
                mySql["host"] = row[0]
                mySql["user"] = row[1]
                mySql["casswor"] = row[6]
                print(mySql)
        except Exception as err:
            print(str(err),'16')
            return str(err)+'line16'
        
def initialize():
        res = {}
        try:
            mySql = readMySql()
            con = pymysql.connect(host=mySql["host"], user=mySql["user"], password=mySql["password"], charset="utf8")
            cursor = con.cursor(pymysql.cursors.DictCursor)
            try:
                sql = "DROP DATABASE IF EXISTS audiobooks"
                cursor.execute(sql)
                con.commit()
                res["drop_database"] = "success"
            except:
                res["drop_database"] = "failure"
            try:
                sql = "CREATE DATABASE audiobooks"
                cursor.execute(sql)
                con.commit()
                res["create_database"] = 'success'
            except:
                res["create_database"] = 'failure'
            con.select_db("audiobooks")
            try:
                sql = "CREATE TABLE books (BID INT auto_increment PRIMARY KEY, title VARCHAR(256) unique, author varchar(64),language VARCHAR(16), contents LONGTEXT, image VARCHAR(16), audio VARCHAR(16))"
                cursor.execute(sql)
                res["create_table_books"] = "success"
            except:
                res["create_table_books"] = "failure"
            try:
                sql = "CREATE TABLE users (user VARCHAR(16) PRIMARY KEY, pwd VARCHAR(256))"
                cursor.execute(sql)
                pwd = hashlib.md5(b"123").hexdigest()
                sql = "INSERT INTO users (user, pwd) VALUES ('admin', %s)"
                cursor.execute(sql, [pwd])
                res["create_table_users"] = "success"
            except:
                res["create_table_users"] = "failure"
            con.commit()
            con.close()
            # Removing all static files
            fs = os.listdir("static") #page 106
            for f in fs:
                os.remove("static/" + f)
        except Exception as err:
            print(err)
        return res
a=readMySql()
print(a)
    
