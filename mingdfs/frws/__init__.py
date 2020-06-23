from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

import logging
import traceback
from flask import Flask
import requests

# 设置FLASK
APP = Flask(__name__)

# 蓝图
from mingdfs.frws.api import FILE_BP

# 注册蓝图
APP.register_blueprint(FILE_BP, url_prefix="/file")


# 设置日志
logging.basicConfig(level=logging.DEBUG)


def start_frws(host, port):
    """启动frws服务

    :param host: 运行地址
    :type host: str
    :param port: 运行端口
    :type port: int

    :return: None
    :rtype: None
    """
    global APP
    try:
        http_server = WSGIServer((host, port), APP)
        http_server.serve_forever()
    except Exception as e:
        logging.error(e)
    finally:
        try:
            http_server.close()
        except:
            logging.error(traceback.format_exc())


def register_frws(host_name, host, port, register_api):
    """注册frws服务

    :param host_name: fmws在hosts文件中对应的frws的名字
    :type host_name: str
    :param host: frws运行地址
    :type host: str
    :param port: frws运行端口
    :type port: int
    :param register_api: 服务器注册api
    :type register_api: str

    :return: 1 为成功，0 为失败
    :rtype: int
    """
    form_data = {
        "host_name": host_name,
        "host": host,
        "port": port
    }
    try:
        r = requests.get(register_api, data=form_data)
        r.raise_for_status()
        return r.json()['status']
    except:
        return 0