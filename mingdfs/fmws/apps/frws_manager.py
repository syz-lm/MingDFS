from flask import Blueprint, request
from mingdfs.fmws import settings
from mingdfs.utils import load_hosts, dump_hosts
import requests
from mingdfs.fmws import apps

FRWS_MANAGER_BP = Blueprint('frws_manager_bp', __name__)


@FRWS_MANAGER_BP.route('/register_frws', methods=['GET'])
def register_frws():
    """注册frws

    GET 请求form表单 form_data = {
                        "host_name": xxx,
                        "ip": xxx,
                        "port": xxx,
                        "fmws_key": xxx
                    }
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    if request.method == 'GET':
        host_name = request.form['host_name']
        ip = request.form['ip']
        port = request.form['port']
        fmws_key = request.form['fmws_key']

        if fmws_key != settings.FMWS_KEY:
            return {"data": [], "status": 0}

        if request.remote_addr != ip:
            return {"data": [], "status": 0}

        hello_api = 'http://%s:%s/hello' % (ip, port)
        try:
            r = requests.get(hello_api, data={"frws_key": settings.FRWS_KEY})
            r.raise_for_status()
            if r.json()['status'] != 1:
                return {"data": [], 'status': 0}
        except:
            return {"data": [], "status": 0}

        ih = load_hosts()
        ih[ip].add(host_name)
        dump_hosts(ih)

        apps.REDIS_CLI.hset(settings.CACHE_FRWS_COMPUTERS_KEY, host_name, port)
        return {"data": [], "status": 1}