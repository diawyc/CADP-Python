import flask
import boto3
import time
import random
import os

Class AudioClass:
""""remove readKeys()"""
                @staticmethod
                def convertToAudio(BID, language, contents):
                    audio=""
                    try:
                        if language=="chinese":
                            languageCode="cmn-CN"
                            voiceId="Zhiyu"
                        else:
                            languageCode="en-US"
                            voiceId="Amy"
                        #keys=AudioClass.readKeys()
                        region_name = 'cn-northwest-1' 
                        client=boto3.client("polly",region_name=region_name)
                        response = client.synthesize_speech(
                            LanguageCode=languageCode,
                            OutputFormat='mp3',
                            Text=contents,
                            TextType='text',
                            VoiceId=voiceId
                        )
                        data=response["AudioStream"].read()
                        audio=("%06d"%BID)+ ".mp3"
                        fobj=open("static/"+audio, "wb")
                        fobj.write(data)
                        fobj.close()
                    except Exception as err:
                        print(err)
                        audio=""
                    return audio
                    """ 2.2 代码

                def convertToAudio(BID,language,contents):
                    res=False
                    try:
                        if code=="cmn-CN":
                            id="Zhiyu"
                        else:
                            id="Amy"

                        region_name = 'cn-northwest-1' 
                        client=boto3.client('polly',region_name=region_name)
                        response = client.synthesize_speech(
                            LanguageCode=code,
                            OutputFormat='mp3',
                            Text=contents,
                            TextType='text',
                            VoiceId=id)
                        data=response["AudioStream"].read()
                        fobj=open("static/audio.mp3",'wb')
                        fobj.write(data)
                        fobj.close()
                        res=True
                    except Exception as err:
                        print(err)
                    return res

                @app.route("/",methods=["GET","POST"])
                def index():
                    code="cmn-CN"
                    fileName=""
                    msg=""
                    text="这是一个文字转语音的演示,输入要朗读文字,提交后会生成音频!"
                    if flask.request.method=="POST":
                        code=flask.request.form.get("code")
                        text=flask.request.form.get("text","").strip()
                        if text!="":
                            if convertToAudio(code,text):
                                fileName="audio.mp3"
                        else:
                            msg="请输入文字"
                    return flask.render_template("polly.html",code=code,text=text,msg=msg,fileName=fileName,rnd=random.random())

                @app.route("/download",methods=["GET","POST"])
                def download():
                    fileName=flask.request.args.get("fileName","")
                    if fileName=="":
                        return b""
                    if os.path.exists("static/"+fileName):
                        fobj=open("static/"+fileName,'rb') #windows和unix的符号不一样
                        data=fobj.read()
                        fobj.close()
                        response=flask.make_response(data)
                        response.headers["Content-Disposition"] = "attachment;filename="+fileName
                        response.headers["ContentType"] = "application/octet-stream"
                        response.headers["Encoding"] = "utf8"
                        return response
                    else:
                        return b""
                app.secret_key = '12345'
                app.debug=True
                if __name__ == '__main__':
                    app.run(host='0.0.0.0', port=5000, debug=True)
                       """
