from gevent.pywsgi import WSGIServer
from gevent import monkey

import logging
import traceback
from datetime import timedelta

from flask import Flask
# 设置APP和SESSION
from flask_session import Session
from redis import StrictRedis

from mingdfs.common.db_mysql import MySQLPool
# 静态文件和模板
from mingdfs.fmws.settings import TEMPLATES_FOLDER, STATIC_FOLDER


# 数据库
from mingdfs.fmws.settings import MYSQL_CONFIG, REDIS_CONFIG, SECRET_KEY

# 设置MySQL和Redis
REDIS_CLI = StrictRedis(host=REDIS_CONFIG['host'],
                        port=REDIS_CONFIG['port'],
                        db=REDIS_CONFIG['db'],
                        password=REDIS_CONFIG['passwd'],
                        socket_timeout=60,
                        socket_connect_timeout=60,
                        socket_keepalive=True)

MYSQL_POOL = MySQLPool(host=MYSQL_CONFIG['host'],
                               user=MYSQL_CONFIG['user'],
                               passwd=MYSQL_CONFIG['passwd'],
                               db=MYSQL_CONFIG['db'],
                               size=MYSQL_CONFIG['size'])

# 设置FLASK
APP = Flask(__name__, static_folder=STATIC_FOLDER,
            template_folder=TEMPLATES_FOLDER)

APP.config.from_mapping(
    SECRET_KEY=SECRET_KEY,
    SEND_FILE_MAX_AGE_DEFAULT=timedelta(seconds=1),
    SESSION_TYPE="redis",
    SESSION_REDIS=REDIS_CLI,
    SESSION_KEY_PREFIX="SESSION:",
    # session超时时间
    PERMANENT_SESSION_LIFETIME=timedelta(seconds=60 * 60),
    # MAX_CONTENT_LENGTH=16 * 1024 * 1024
)

Session(APP)

# 蓝图
from mingdfs.fmws.apps.plat import PLAT_BP
from mingdfs.fmws.apps.file import FILE_BP

# 注册蓝图
APP.register_blueprint(PLAT_BP, url_prefix="/plat")
APP.register_blueprint(FILE_BP, url_prefix="/file")


# 设置日志
logging.basicConfig(level=logging.DEBUG)


def main():
    global APP
    try:
        monkey.patch_all()

        http_server = WSGIServer(('0.0.0.0', 8000), APP)
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


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8000, debug=True)