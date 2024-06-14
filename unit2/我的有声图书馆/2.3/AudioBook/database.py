import pymysql
import os
import hashlib
from audio import AudioClass
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
            print(err,':BookDatabase line17')
        return mySql
    @staticmethod
    def initialize():
        res = {}
        try:
            mySql = BookDatabase.readMySql()
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
            print(err,':BookDatabase line63')
        return res
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
            print(err,':BookDatabase line79')
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
                fobj=open("static/"+sBID+".jpg","wb") #change path to unix
                fobj.write(data)
                fobj.close()
                image=sBID+".jpg"
            audio="" #page 107
            if contents!="":
                audio=AudioClass.convertToAudio(BID,language,contents)
            if audio!="" or image!="":
                cursor.execute('update books set image=%s,audio=%s where BID=%s',(image,audio,BID))
                con.commit()
                con.close()
                result={"BID":BID,"image":image,"audio":audio}
        except Exception as err:
             print(err,':BookDatabase line 110')
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
                fobj=open("static/"+sBID+".jpg","wb")
                fobj.write(data)
                fobj.close()
                image=sBID+".jpg"
                audio=""
            if contents!="":
                audio=AudioClass.convertToAudio(BID,language,contents)
            else:
                if os.path.exists("static/"+sBID+".mp3"):
                    os.remove("static/"+sBID+".mp3")
            if image:
                sql="update books set title=%s,author=%s,language=%s,contents=%s,image=%s,audio=%s where BID="+str(BID)
                cursor.execute(sql,[title,author,language,contents,image,audio])
            else:
            #如果没有图像就维持原来的图像
                sql="update books set title=%s,author=%s,language=%s,contents=%s,audio=%s where BID="+str(BID)
                cursor.execute(sql,[title,author,language,contents,audio])
                con.commit()
                con.close()
                result={"BID":BID,"image":image,"audio":audio} 
        except Exception as err:#page 108"""
            print(err,':BookDatabase line143')
        return result
    @staticmethod
    def deleteBook(BID):
        res=False
        try:
            mySql=BookDatabase.readMySql()
            con=pymysql.connect(host=mySql["host"],user=mySql["user"],password=mySql["password"],charset="utf8",db="audiobooks")
            cursor=con.cursor(pymysql.cursors.DictCursor)
            #Removing the associated image and audio
            sBID="%06d"%BID
            image="static/"+sBID+".jpg"
            if os.path.exists(image):
                os.remove(image)
            audio="static/"+sBID+".mp3"
            if os.path.exists(audio):
                os.remove(audio)
            cursor.execute("delete from books where BID="+str(BID))
            con.commit()
            con.close()
            res=True
        except Exception as err:
            print(err,':BookDatabase line 165')
        return res
    @staticmethod
    def selectBook(BID):
        book=None
        try:
            mySql=BookDatabase.readMySql()
            con=pymysql.connect(host=mySql["host"],user=mySql["user"],password=mySql["password"],charset="utf8",db="audiobooks")
            cursor=con.cursor(pymysql.cursors.DictCursor)
            sql="select * from books where BID="+str(BID)
            cursor.execute(sql)
            book=cursor.fetchone()
            con.close()
        except Exception as err:
            print(err,':BookDatabase line179')
        return book
    @staticmethod
    def listBook(key):
        books=[]#p109"""
        try:
            mySql=BookDatabase.readMySql()
            con=pymysql.connect(host=mySql["host"],user=mySql["user"],password=mySql["password"],charset="utf8",db="audiobooks")
            cursor=con.cursor(pymysql.cursors.DictCursor)
            sql="select BID,title,author,language,image,audio from books order by title"
            if key!="":
                sql="select BID,title,author,language,image,audio from books where title like '%"+key+"%' order by title"
            cursor.execute(sql)
            books=cursor.fetchall()
            con.close()
        except Exception as err:
            print(err,':BookDatabase line195')
        return books



