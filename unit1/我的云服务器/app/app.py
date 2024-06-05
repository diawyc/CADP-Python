# coding: utf-8
import hashlib
from flask import Flask, request, session, render_template, jsonify
import pymysql

app = Flask(__name__)
app.secret_key = '12345'

def con_db():
    return pymysql.connect(host='mydbinstance.cxtmwuenuqe2.rds.cn-northwest-1.amazonaws.com.cn', port=3306, user='root', passwd='mypassword', db='usermanage', charset='utf8mb4')
"""

#其中 mydbinstance.xxxxxxxxxxxx.rds.cn-north-1.amazonaws・com・cn为 MySQL的
#endpoint.此处应替换为之前创建的RDS的endpoint

"""


@app.route('/')
def index(): #用户登录界面
    return render_template('index.html')

@app.route('/user_reg/', methods=['POST', 'GET'])
def user_reg():#用户注册界面
    return render_template('userreg.html')

@app.route('/user_update/')
def user_update():#用户信息更新界面
    return render_template('userupdate.html')

@app.route('/login/', methods=['POST'])
def login():
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    con = con_db()
    cu = con.cursor()
    cu.execute("select id from user where user=%s and pwd=%s", (user, sha256_crypt(pwd)))
    if cu.fetchall():
        session['user'] = user
        if user == 'admin':
            return jsonify({'code': 2, 'msg': '登录成功'})
        return jsonify({'code': 0, 'msg': '登录成功'})
    return jsonify({'code': 1, 'msg': '账号或密码错误，请求失败'})

@app.route('/admin_index/')
def admin_index():#管理首页
    user = session.get('user')
    con = con_db()
    cu = con.cursor(pymysql.cursors.DictCursor)
    return render_template('admin.html', **{})

@app.route('/user_index/')
def user_index():
    user = session.get('user')
    con = con_db()
    cu = con.cursor(pymysql.cursors.DictCursor)
    cu.execute("select user, email from user where user=%s", (user,))
    data = cu.fetchall()
    if data:
        data = data[0]
    return render_template('user.html', **data)

@app.route('/reg/', methods=['POST'])
def reg():#用户注册
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    email = request.form.get('email')
    con = con_db()
    cu = con.cursor()
    cu.execute("select id from user where user=%s", (user,))
    if cu.fetchall():
        return jsonify({'code': 1, 'msg': '用户已存在'})
    cu.execute("insert into user(user, pwd, email) values (%s, %s, %s)", (user, sha256_crypt(pwd), email))
    con.commit()
    return jsonify({'code': 0, 'msg': '注册成功'})

@app.route('/put/', methods=['POST', 'GET'])
def put():
    con = con_db()
    cu = con.cursor(pymysql.cursors.DictCursor)
    user = session.get('user')
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    #print(user, pwd)
    if pwd:
        cu.execute("update user set pwd=%s where user=%s", (sha256_crypt(pwd), user))
    if email:
        cu.execute("update user set email=%s where user=%s", (email, user))
    con.commit()
    return jsonify({'code': 0, 'msg': '修改成功'})

@app.route('/get_list/', methods=['GET'])
def auser():
    user = session.get('user')
    sc = request.args.get('sc', None)
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    # print(sc)
    con = con_db()
    cu = con.cursor(pymysql.cursors.DictCursor)
    sql = 'select count(*)ct from user where 1=1'
    sql1= 'select * from user where 1=1'
    if sc:
        sql += " and user like '%{}%'".format(sc)
        sql1 += " and user like '%{}%'".format(sc)
    sql1 += ' group by id'
    sql1 += ' limit {}, {}'.format((page - 1) * limit, limit)
    #print(sql,sql1)
    cu.execute(sql)
    ct = cu.fetchall()[0].get('ct')
    cu.execute(sql1)
    data = cu.fetchall()
    return jsonify({'code': 0, 'msg': '获取成功', 'data': data, 'count': ct})

@app.route('/adel/', methods=['POST'])
def adel():#删除用户
    pid = request.form.get('pid')
    con = con_db()
    cu = con.cursor(pymysql.cursors.DictCursor)
    cu.execute("delete from user where id=%s", (pid,))
    con.commit()
    return jsonify({'code': 0, 'msg': '删除成功'})

@app.route('/aput/', methods=['POST'])
def aput():
    pid = request.form.get('pid')
    pwd = request.form.get('pwd')
    con = con_db()
    cu = con.cursor(pymysql.cursors.DictCursor)
    cu.execute("update user set pwd=%s where id=%s", (sha256_crypt(pwd), pid))
    con.commit()
    return jsonify({'code': 0, 'msg': '修改成功'})
def sha256_crypt(s):
    m = hashlib.sha256()
    b = s.encode(encoding='utf-8')
    m.update(b)
    sm = m.hexdigest()
    return sm

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

#This change will make the Flask app listen on all available network interfaces (`host='0.0.0.0'`) and run on port 5000. The `debug=True` parameter will enable the debug mode, which provides a more descriptive error message and automatic reloading of the server when the code changes.
