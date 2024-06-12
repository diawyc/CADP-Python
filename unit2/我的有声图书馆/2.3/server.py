import flask
import sys
import json
from database import BookDatabase
from audio import AudioClass
import datetime
import random
import time
import os
import urllib.request
app=flask.Flask("web") # main
"""
@app.route("/initialize")
def initialize():
    msg=""
    try:
        msg=BookDatabase.initialize()
    except Exception as err:
        msg=str(err)
    return json.dumps({"msg":msg})
"""
@app.route("/",methods=["GET","POST"])
def index():
    flask.session["login"]=""
    try:
        books=[]
        pageIndex=int(flask.request.values.get("pageIndex","1"))
        key=flask.request.values.get("key","")
        pageSize=10
        pageCount=0
        rows=BookDatabase.listBook(key)
        if rows:
            pageCount=len(rows)//pageSize
            if len(rows) % pageSize!=0:
                pageCount+=1
            if pageIndex>pageCount:
                pageIndex=pageCount
            rows=rows[(pageIndex-1)*pageSize:pageIndex*pageSize]
            for row in rows:
                book={"BID":row["BID"],"title":row["title"],"image":row["image"],"rnd":str(random.random()),"author":row["author"]}
                book["image"]=row["image"]+"?rnd="+str(random.random())
                books.append(book)
        return flask.render_template("index.html",books=books,pageCount=pageCount,pageIndex=pageIndex,key=key)
    except Exception as error:
        return str(error)
@app.route("/insertBook",methods=["GET","POST"])
def insertBook():
    if flask.session.get("login","")!="OK":
        return flask.redirect("/")
    try:
        msg=""
        title=""
        author=""
        language="chinese"
        contents=""
        image=""
        audio=""
        method=flask.request.method
        if method=="POST":
            title=flask.request.values.get("title","")
            author=flask.request.values.get("author","")
            language=flask.request.values.get("yList","")
            contents=flask.request.values.get("contents","")
            imgFile=flask.request.files["imgFile"]
            data=b""
            if imgFile:
                data=imgFile.read()
                result=BookDatabase.insertBook(title,author,language,contents,data)
            if result["BID"]>0:
                msg="增加图书成功"
                image=result["image"]
                audio=result["audio"]
            else:
                msg="增加图书失败: 该图书已经存在"
        key=title
        return flask.render_template("insertBook.html",title=title,author=author,language=language,contents=contents,image=image,audio=audio,key=key,msg=msg)
    except Exception as error:
        return str(error)
@app.route("/updateBook",methods=["GET","POST"])
def updateBook():
    if flask.session.get("login","")!="OK":
        return flask.redirect("/")
    try:
        msg=""
        BID=int(flask.request.values.get("BID","0"))
        pageIndex=int(flask.request.values.get("pageIndex","1"))
        key=flask.request.values.get("key","")
        book=BookDatabase.selectBook(BID)
        title=book["title"]
        author=book["author"]
        language=book["language"]
        contents=book["contents"]
        image=book["image"]
        audio=book["audio"]
        method=flask.request.method
        if method=="POST":
            title=flask.request.values.get("title","")
            author=flask.request.values.get("author","")
            language=flask.request.values.get("language","")
            contents=flask.request.values.get("contents","")
            imgFile=flask.request.files["imgFile"]
            data=b""
            if imgFile:
                data=imgFile.read()
            result=BookDatabase.updateBook(BID,title,author,language,contents,data)
            if result["BID"]>0:
                msg="更新图书成功"
                if result["image"]!="":
                    image=result["image"]
                audio=result["audio"]
            else:
                msg="更新图书失败: 该图书已经存在"
            return flask.render_template("updateBook.html",BID=BID,pageIndex=pageIndex,key=key,title=title,author=author,language=language,contents=contents,image=image,audio=audio,msg=msg,rnd=random.random())
    except Exception as error:
        return str(error)
@app.route("/readBook",methods=["GET","POST"])
def readBook():
    try:
        BID=int(flask.request.values.get("BID","0"))
        pageIndex=int(flask.request.values.get("pageIndex","1"))
        key=flask.request.values.get("key","")
        book=BookDatabase.selectBook(BID)
        title=book["title"]
        contents=book["contents"]
        audio=book["audio"]
        #chinese blanks
        contents=" ".join(contents.replace("\n","<br> ")) #有修改
        return flask.render_template("readBook.html",BID=BID,pageIndex=pageIndex,key=key,title=title,contents=contents,audio=audio,rnd=random.random())
    except Exception as error:
        return str(error)
@app.route("/selectBook",methods=["GET","POST"])
def selectBook():
    if flask.session.get("login","")!="OK":
        return flask.redirect("/")
    try:
        books=[]
        pageIndex=int(flask.request.values.get("pageIndex","1"))
        key=flask.request.values.get("key","")
        pageSize=10
        pageCount=0
        cmd=flask.request.values.get("cmd","")
        if cmd=="delete":
            BID=int(flask.request.values.get("BID","0"))
            BookDatabase.deleteBook(BID)
        rows=BookDatabase.listBook(key)
        if rows:
            pageCount=len(rows)//pageSize
            if len(rows) % pageSize!=0:
                pageCount+=1
            if pageIndex>pageCount:
                pageIndex=pageCount
            rows=rows[(pageIndex-1)*pageSize:pageIndex*pageSize]
            for row in rows:
                book={"BID":row["BID"],"title":row["title"],"author":row["author"]}
                book["image"]=row["image"]+"?rnd="+str(random.random())
                books.append(book)
        return flask.render_template("selectBook.html",books=books,pageCount=pageCount,pageIndex=pageIndex,key=key)
    except Exception as error:
        return str(error)
@app.route("/download",methods=["GET","POST"])
def download():
    BID=int(flask.request.values.get("BID","0"))
    audio=flask.request.values.get("audio","")
    if BID>0 and audio!="":
        if os.path.exists("static/"+audio): # change to unix path format
            fobj=open("static/"+audio,'rb') # change to unix path format
            data=fobj.read()
            fobj.close()
            response=flask.make_response(data)
            title=BookDatabase.selectBook(BID)["title"]
            fileName=urllib.parse.quote(title+".mp3")
            response.headers["Content-Disposition"]="attachment; filename="+fileName
            response.headers["Content-Type"] = "application/octet-stream"
            response.headers["Encoding"] = "utf8"
            return response
    return flask.redirect("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        msg = ""
        user = ""
        pwd = ""
        flask.session["login"] = ""
        if flask.request.method == "POST":
            user = flask.request.values.get('user', "")
            pwd = flask.request.values.get("pwd", "")
            if BookDatabase.login(user, pwd):
                flask.session["login"] = "OK"
                return flask.redirect("/selectBook")
            else:
                msg = "登录失败"
        return flask.render_template("login.html", user=user, pwd=pwd, msg=msg)
    except Exception as error:
        return str(error)
app.secret_key = "123"
app.debug = True
app.run()         
  

