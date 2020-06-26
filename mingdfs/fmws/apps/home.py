from flask import Blueprint, request, render_template, abort
from mingdfs.utils import pc_or_mobile, PC, MOBILE

HOME_BP = Blueprint('home_bp', __name__)


@HOME_BP.route('/', methods=['GET'])
@HOME_BP.route('/home', methods=['GET'])
def home():
    if pc_or_mobile(request.headers['User-Agent']) == PC:
        return render_template('pc/home.html')
    elif pc_or_mobile(request.headers['User-Agent']) == MOBILE:
        return render_template('mobile/home.html')
    else:
        abort(403, '不支持的客户端')