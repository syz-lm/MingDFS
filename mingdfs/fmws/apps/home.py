from flask import Blueprint, request, render_template, abort, session, redirect, url_for
from mingdfs.utils import pc_or_mobile, PC, MOBILE
from mingdfs.fmws.settings import IS_LOGIN
from mingdfs.fmws.db import User
from mingdfs.fmws import apps


HOME_BP = Blueprint('home_bp', __name__)


@HOME_BP.route('/', methods=['GET'])
@HOME_BP.route('/home', methods=['GET'])
def home():
    user_id = session.get(IS_LOGIN, None)
    if user_id is None:
        return redirect(url_for('user_bp.login'))

    user = User(apps.MYSQL_POOL)
    user_name = user.get_user_name_by_user_id(user_id)
    if user_name is None:
        print('user_id存在，但user_name为none', user_id)
        session.pop(IS_LOGIN) # XXX: 这究竟是flask的bug还是flask团队留下的后门？
        return redirect(url_for('user_bp.login'))

    api_key = user.get_api_key_by_user_id(user_id)
    if api_key is None:
        print('user_id存在，但api_key为none', api_key)
        return redirect(url_for('user_bp.login'))

    context = {
        'user_name': user_name,
        'api_key': api_key
    }
    if pc_or_mobile(request.headers['User-Agent']) == PC:
        return render_template('pc/home.html', **context)
    elif pc_or_mobile(request.headers['User-Agent']) == MOBILE:
        return render_template('mobile/home.html', **context)
    else:
        abort(403, '不支持的客户端')