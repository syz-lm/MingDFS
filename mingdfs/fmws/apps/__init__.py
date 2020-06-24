from gevent.pywsgi import WSGIServer
from gevent import monkey

import logging
import traceback
from datetime import timedelta

from flask import Flask
# 设置APP和SESSION
from flask_session import Session
from redis import StrictRedis

from mingdfs.db_mysql import MySQLPool
from mingdfs.fmws import settings

REDIS_CLI= None
MYSQL_POOL = None

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
    global APP
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
    #
    # 注册蓝图
    APP.register_blueprint(FILE_BP, url_prefix="/file")
    APP.register_blueprint(USER_BP, url_prefix="/user")
    APP.register_blueprint(FRWS_MANAGER_BP, url_prefix="/frws_manager")


def start_fmws(host, port):
    global APP
    try:
        monkey.patch_all()
        _init_bp()

        print('fmws start.')
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
            http_server.close()
        except:
            logging.error(traceback.format_exc())


def debug(host, port):
    global APP
    _init_bp()

    APP.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    debug('0.0.0.0', 15675)