from flask import Blueprint, request

USER_BP = Blueprint('user_bp', __name__)


@USER_BP.route('/register', methods=['GET'])
def register():
    """注册

    GET 请求form表单 {"user_name": xxx, "passwd": xxx, "re_passwd": xxx, "email": xxx, "check_code": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    pass


@USER_BP.route('/login', methods=['GET'])
def login():
    """登录

    GET 请求form表单 {"user_name": xxx, "passwd": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    pass


@USER_BP.route('/change_passwd', methods=['GET'])
def change_passwd():
    """修改密码

    GET 请求form表单 {"user_name": xxx, "passwd": xxx", "re_passwd": xxx, "email": xxx, "check_code": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    pass


@USER_BP.route('/pay', methods=['GET'])
def pay():
    """充值

    GET 请求form表单 {"money": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    pass