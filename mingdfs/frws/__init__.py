from gevent.pywsgi import WSGIServer

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


def register_frws(host_name, ip, port, fmws_key, fmws_host_name, fmws_port, save_dirs, frws_key):
    form_data = {
        "host_name": host_name,
        "ip": ip,
        "port": port,
        "save_dirs": save_dirs,
        "frws_key": frws_key,
        "fmws_key": fmws_key
    }
    try:
        api = 'http://%s:%d/frws_manager/register_frws' % (fmws_host_name, fmws_port)

        r = requests.get(api, data=form_data)
        r.raise_for_status()
        print(r.json()['data'])
        return r.json()['status']
    except:
        logging.error(traceback.format_exc())
        return 0