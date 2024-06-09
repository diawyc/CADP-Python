import pymysql
import os
import hashlib

class BookDatabase:
    @staticmethod
    def readMySql():
        mySql = {}
        try:
            with open("mySql.csv", "rt") as fobj:
                rows = fobj.readlines()
                row = rows[1].strip().split(",")
                mySql["host"] = row[0]
                mySql["user"] = row[1]
                mySql["password"] = row[2]
        except Exception as err:
            print(err)
        return mySql

    @staticmethod
    def initialize():
        res = {}
        try:
            mySql = BookDatabase.readMySql()
            print(mySql)
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
            fs = os.listdir("static")
            for f in fs:
                os.remove("static/" + f)

        except Exception as err:
            print(err)

        return res
"""page 106"""
@staticmethod
def login(user,pwd):
    res=False
    try:
        pwd=hashlib.md5(pwd.encode()).hexdigest()
        mySql=BookDatabase.readMySql()
        con=pymysql.connect(host=mySql["host"],user=mySql["user"],password=mySql["password"],charset="utf8",db="audiobooks")
        cursor=con.cursor(pymysql.cursors.DictCursor)
        sql="select * from users where user=%s and pwd=%s"
        cursor.execute(sql,[user,pwd])
        if cursor.fetchone():
            res=True
        con.close()
    except Exception as err:
        print(err)
    return res

@staticmethod
def insertBook(title,author,language,contents,data):
    result={"BID":0,"image":"","audio":""}
    try:
        mySql=BookDatabase.readMySql()
        con=pymysql.connect(host=mySql["host"],user=mySql["user"],password=mySql["password"],charset="utf8",db="audiobooks")
        cursor=con.cursor(pymysql.cursors.DictCursor)
        sql="insert into books (title,author,language,contents,image,audio) values (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,[title,author,language,contents,"",""])
        con.commit()
        cursor.execute("select BID from books order by BID desc limit 1")
        row=cursor.fetchone()
        BID=row["BID"]
        sBID="%06d" %BID
        image=""
        if len(data)>0:
            fobj=open("static\\"+sBID+".jpg","wb")
            fobj.write(data)
            fobj.close()
            image=sBID+".jpg"
"""page 107"""
                audio=""
                if contents!="":
                    audio=AudioClass.convertToAudio(BID,language,contents)
                if audio!="" or image!="":
                    cursor.execute('update books set image=%s,audio=%s where BID=%s',(image,audio,BID))
                    con.commit()
                    con.close()
                    result={"BID":BID,"image":image,"audio":audio}
                except Exception as err:
                    print(err)
                return result

                @staticmethod
                def updateBook(BID,title,author,language,contents,data):
                    result={"BID":0,"image":"","audio":""}
                    try:
                        mySql=BookDatabase.readMySql()
                        con=pymysql.connect(host=mySql["host"],user=mySql["user"],password=mySql["password"],charset="utf8",db="audiobooks")
                        cursor=con.cursor(pymysql.cursors.DictCursor)
                        sBID="%06d"%BID
                        image=""
                        if len(data)>0:
                            fobj=open("static\\"+sBID+".jpg","wb")
                            fobj.write(data)
                            fobj.close()
                            image=sBID+".jpg"
                        audio=""
                        if contents!="":
                            audio=AudioClass.convertToAudio(BID,language,contents)
                        else:
                            if os.path.exists("static\\"+sBID+".mp3"):
                                os.remove("static\\"+sBID+".mp3")
                        if image:
                            sql="update books set title=%s,author=%s,language=%s,contents=%s,image=%s,audio=%s where BID="+str(BID)
                            cursor.execute(sql,[title,author,language,contents,image,audio])
                        else:
                            #如果没有图像就更新除了图像外的所有
                            sql="update books set title=%s,author=%s,language=%s,contents=%s,audio=%s where BID="+str(BID)
                            cursor.execute(sql,[title,author,language,contents,audio])
                        con.commit()
                        con.close()
                        result={"BID":BID,"image":image,"audio":audio}
"""page 108"""
