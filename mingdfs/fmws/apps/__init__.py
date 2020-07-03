from gevent.pywsgi import WSGIServer

import logging
import traceback
from datetime import timedelta

from flask import Flask, request, abort
# 设置APP和SESSION
from flask_session import Session
from redis import StrictRedis

from mingdfs.db_mysql import MySQLPool
from mingdfs.fmws import settings
from mingdfs.utils import pc_or_mobile, PC, MOBILE

REDIS_CLI: StrictRedis = None
MYSQL_POOL: MySQLPool = None

def check_rm():
    global MYSQL_POOL, REDIS_CLI
    if MYSQL_POOL is None:
        raise Exception("MySQL初始化失败")

    if REDIS_CLI is None:
        raise Exception("Redis初始化失败")


def init_mr():
    global MYSQL_POOL, REDIS_CLI
    # 设置MySQL和Redis
    REDIS_CLI = StrictRedis(host=settings.REDIS_CONFIG['host'],
                            port=settings.REDIS_CONFIG['port'],
                            db=settings.REDIS_CONFIG['db'],
                            password=settings.REDIS_CONFIG['passwd'],
                            socket_timeout=60,
                            socket_connect_timeout=60,
                            socket_keepalive=True)

    MYSQL_POOL = MySQLPool(host=settings.MYSQL_CONFIG['host'],
                           user=settings.MYSQL_CONFIG['user'],
                           passwd=settings.MYSQL_CONFIG['passwd'],
                           db=settings.MYSQL_CONFIG['db'],
                           size=settings.MYSQL_CONFIG['size'])



# 设置FLASK
APP = Flask(__name__, static_folder=settings.STATIC_FOLDER,
            template_folder=settings.TEMPLATES_FOLDER)

def init_app():
    global APP, REDIS_CLI
    APP.config.from_mapping(
        SECRET_KEY=settings.SECRET_KEY,
        SEND_FILE_MAX_AGE_DEFAULT=timedelta(seconds=1),
        SESSION_TYPE="redis",
        SESSION_REDIS=REDIS_CLI,
        SESSION_KEY_PREFIX="SESSION:",
        # session超时时间
        PERMANENT_SESSION_LIFETIME=timedelta(seconds=60 * 60),
        # MAX_CONTENT_LENGTH=16 * 1024 * 1024
    )

    Session(APP)

def _init_bp():
    global APP
    # 蓝图
    from mingdfs.fmws.apps.file import FILE_BP
    from mingdfs.fmws.apps.user import USER_BP
    from mingdfs.fmws.apps.frws_manager import FRWS_MANAGER_BP
    from mingdfs.fmws.apps.home import HOME_BP
    #
    # 注册蓝图
    APP.register_blueprint(FILE_BP, url_prefix="/file")
    APP.register_blueprint(USER_BP, url_prefix="/user")
    APP.register_blueprint(FRWS_MANAGER_BP, url_prefix="/frws_manager")
    APP.register_blueprint(HOME_BP, url_prefix='')

    def _not_support_mobile():
        if not request.headers.has_key('User-Agent'):
            abort(403, '错误的请求头。')

        if request.headers.has_key("User-Agent"):
            ua = request.headers['User-Agent']
            if pc_or_mobile(ua) == MOBILE:
                abort(403, '移动端网站正在建设中。')

    APP.before_request(_not_support_mobile)


def start_fmws(host, port):
    global APP
    http_server = None
    try:
        _init_bp()

        http_server = WSGIServer((host, port), APP)
        http_server.serve_forever()
    except Exception as e:
        logging.error(e)
    finally:
        try:
            REDIS_CLI.close()
        except:
            logging.error(traceback.format_exc())
        try:
            MYSQL_POOL.release()
        except:
            logging.error(traceback.format_exc())

        try:
            if http_server: http_server.close()
        except:
            logging.error(traceback.format_exc())


def debug(host, port):
    global APP
    _init_bp()

    APP.run(host=host, port=port, threaded=True)


if __name__ == '__main__':
    debug('0.0.0.0', 15675)