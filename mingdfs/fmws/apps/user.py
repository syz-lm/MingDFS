from flask import Blueprint, request, session, render_template, abort
from mingdfs.fmws.db import User
from mingdfs.fmws import apps
from mingdfs.utils import pc_or_mobile, PC, MOBILE
from mingdfs.fmws.settings import IS_LOGIN

import time
import hashlib

apps.check_rm()

USER_BP = Blueprint('user_bp', __name__)


@USER_BP.route('/register', methods=['POST', 'GET'])
def register():
    """注册

    POST 请求form表单 {"user_name": xxx, "passwd": xxx, "re_passwd": xxx, "email": xxx, "check_code": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}

    GET 返回注册页面
    """
    if request.method == 'POST':
        user_name = request.form['user_name']
        passwd = request.form['passwd']
        re_passwd = request.form['re_passwd']
        email = request.form['email']
        check_code = request.form['check_code']

        if passwd != re_passwd:
            return {"data": [], "status": 0}

        if session.get(email) != check_code:
            return {"data": [], "status": 0}

        user = User(apps.MYSQL_POOL)
        if user.exists(user_name, email) == False:
            register_time = int(time.time())
            md5 = hashlib.md5()
            md5.update((user_name + email + str(register_time)).encode('utf-8'))
            api_key = md5.hexdigest()
            if user.add_user(user_name, 0, api_key, register_time, email, passwd, 0):
                session.pop(email)
                return {"data": [], "status": 1}
            else:
                return {"data": [], "status": 0}
    elif request.method == 'GET':
        if pc_or_mobile(request.headers['User-Agent']) == PC:
            return render_template('pc/register.html')
        elif pc_or_mobile(request.headers['User-Agent']) == MOBILE:
            return render_template('mobile/register.html')
        else:
            abort(403, "不支持的客户端")


@USER_BP.route('/login', methods=['POST'])
def login():
    """登录

    POST 请求form表单 {"user_name": xxx, "passwd": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}

    GET 返回登录页面
    """
    if request.method == 'POST':
        user_name = request.form['user_name']
        passwd = request.form['passwd']
        user = User(apps.MYSQL_POOL)
        user_id = user.login(user_name, passwd)
        if user_id != None:
            session[IS_LOGIN] = user_id
            return {"data": [], "status": 1}
        else:
            return {"data": [], "status": 0}
    elif request.method == 'GET':
        if pc_or_mobile(request.headers['User-Agent']) == PC:
            return render_template('pc/login.html')
        elif pc_or_mobile(request.headers['User-Agent']) == MOBILE:
            return render_template('mobile/login.html')
        else:
            abort(403, '不支持的客户端')


@USER_BP.route('/change_passwd', methods=['POST'])
def change_passwd():
    """修改密码

    POST 请求form表单 {"user_name": xxx, "passwd": xxx", "re_passwd": xxx, "email": xxx, "check_code": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    if request.method == 'POST':
        user_name = request.form['user_name']
        passwd = request.form['passwd']
        re_passwd = request.form['re_passwd']
        email = request.form['email']
        check_code = request.form['check_code']

        if passwd != re_passwd:
            return {"data": [], "status": 0}
        if session.get(email) != check_code:
            return {"data": [], "status": 0}
        user = User(apps.MYSQL_POOL)
        if user.change_passwd(passwd, user_name, email):
            session.pop(email)
            return {"data": [], "status": 1}
        else:
            return {"data": [], "status": 0}
    elif request.method == 'GET':
        if pc_or_mobile(request.headers['User-Agent']) == PC:
            return render_template('pc/change_passwd.html.html')
        elif pc_or_mobile(request.headers['User-Agent']) == MOBILE:
            return render_template('mobile/change_passwd.html.html')
        else:
            abort(403, '不支持的客户端')


@USER_BP.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        if session.get(IS_LOGIN) != None:
            session.pop(IS_LOGIN)
            return {"data": [], "status": 1}
        else:
            return {"data": [], "status": 0}


@USER_BP.route('/pay', methods=['POST'])
def pay():
    """充值

    POST 请求form表单 {"money": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    pass