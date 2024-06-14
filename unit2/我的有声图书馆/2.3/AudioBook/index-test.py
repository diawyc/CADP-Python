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
app=flask.Flask(__name__) # change from book

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
        return str(error)+':line45'

app.secret_key = "123"
app.debug = True
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)     
  

