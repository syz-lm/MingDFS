from gevent.pywsgi import WSGIServer
from gevent import monkey

import logging
import traceback

from flask import Flask

# 设置FLASK
APP = Flask(__name__)

# 蓝图
from mingdfs.fmws.apps.file import FILE_BP

# 注册蓝图
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
            http_server.close()
        except:
            logging.error(traceback.format_exc())


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8000, debug=True)