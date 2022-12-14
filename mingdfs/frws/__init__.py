import logging
import traceback

import requests
from flask import Flask
from gevent.pywsgi import WSGIServer
from redis import StrictRedis

from mingdfs.frws import settings

REDIS_CLI: StrictRedis = None

# 设置FLASK
APP = Flask(__name__)

# 蓝图
from mingdfs.frws.api import FILE_BP

# 注册蓝图
APP.register_blueprint(FILE_BP, url_prefix="/file")


# 设置日志
logging.basicConfig(level=logging.DEBUG)

def init_redis_cli():
    global REDIS_CLI
    REDIS_CLI = StrictRedis(host=settings.REDIS_CONFIG['host'],
                            port=settings.REDIS_CONFIG['port'],
                            db=settings.REDIS_CONFIG['db'],
                            password=settings.REDIS_CONFIG['passwd'],
                            socket_timeout=60,
                            socket_connect_timeout=60,
                            socket_keepalive=True)

def start_frws(host, port):
    global APP
    try:
        init_redis_cli()
        http_server = WSGIServer((host, port), APP, keyfile=settings.SSL_KEYFILE, certfile=settings.SSL_CERTFILE)
        http_server.serve_forever()
    except Exception as e:
        logging.error(e)
    finally:
        try:
            http_server.close()
        except:
            logging.error(traceback.format_exc())

def debug_frws(host, port):
    global APP
    init_redis_cli()
    APP.run(host, port, threaded=True, ssl_context=(settings.SSL_CERTFILE, settings.SSL_KEYFILE))


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
        api = 'https://%s:%d/frws_manager/register_frws' % (fmws_host_name, fmws_port)

        r = requests.get(api, data=form_data, verify=False)
        r.raise_for_status()
        print(r.json()['data'])
        return r.json()['status']
    except:
        logging.error(traceback.format_exc())
        return 0