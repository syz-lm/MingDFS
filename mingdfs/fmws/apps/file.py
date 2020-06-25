from flask import Blueprint, request, send_file
from mingdfs.fmws import settings
from mingdfs.fmws.apps import MYSQL_POOL, REDIS_CLI
from mingdfs.fmws.db import User, File, RediOP
import requests
import os
import traceback
import logging
import io
import time


FILE_BP = Blueprint('file_bp', __name__)


@FILE_BP.route('/upload', methods=['POST'])
def upload():
    """上传文件

    POST 请求form表单 {"api_key": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    if request.method == 'POST':
        api_key = request.form['api_key']
        third_user_id = request.form['third_user_id']
        title = request.form['title']
        category_id = request.form['category_id']

        user = User(MYSQL_POOL)
        user_id = user.get_user_id_by_api_key(api_key)
        if user_id is None:
            return {"data": [], "status": 0}

        my_file = request.files['upload_file_name']
        file_extension = my_file.filename.rsplit('.', 1)
        if len(file_extension) != 2:
            file_extension = ''
        else:
            file_extension = file_extension[1]

        file = File(MYSQL_POOL)
        if file.exists(user_id, third_user_id, title, category_id):
            return {"data": [], "status": 0}
        else:
            redis_op = RediOP(REDIS_CLI)
            host_name, port = redis_op.get_best_frws_host_name_port()
            if host_name is None or port is None:
                return {"data": [], "status": 0}

            save_path = settings.FMWS_CACHE + os.path + file.filename
            try:
                file.save(save_path)
            except:
                logging.error(traceback.format_exc())
                print('文件存储失败', save_path)
                return {"data": [], 'status': 0}

            u = settings.FRWS_API_TEMPLATE['upload']
            method = u['method￿']
            try:
                f = open(save_path, 'rb')
                url = u['url'] % (host_name, port)
                files = {'upload_file_name': f}
                r = requests.request(method, url, files=files)
                r.raise_for_status()
                if r.json()['status'] != 0:
                    return {"data": [], "status": 1}
                else:
                    return {"data": [], "status": 0}
            except:
                logging.error(traceback.format_exc())
                print('转存文件失败', url, method)
                return {"data": [], "status": 0}
            finally:
                try:
                    if f: f.close()
                except:
                    logging.error(traceback.format_exc())
                    print('关闭文件失败', save_path)

                try:
                    os.remove(save_path)
                except:
                    logging.error(traceback.format_exc())
                    print('清除文件失败', save_path)
                    # TODO


@FILE_BP.route('/download', methods=['GET'])
def download():
    """下载文件

    GET 请求url参数 {"api_key": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx}
        返回 成功 二进制数据
            失败 json {"data": [], "status": 0}
    """
    if request.method == 'GET':
        api_key = request.form['api_key']
        third_user_id = request.form['third_user_id']
        title = request.form['title']
        category_id = request.form['category_id']

        user = User(MYSQL_POOL)
        user_id = user.get_user_id_by_api_key(api_key)
        if user_id is None:
            return {"data": [], "status": 0}

        file = File(MYSQL_POOL)
        file_extension = file.get_file_extension(user_id, third_user_id, title, category_id)
        if file_extension is None:
            return {"data": [], "status": 0}

        redis_op = RediOP(REDIS_CLI)
        host_name, port = redis_op.get_best_frws_host_name_port()
        if host_name is None and port is None:
            return {"data": [], "status": 0}
        u = settings.FRWS_API_TEMPLATE['download']
        method = u['method￿']
        url = u['url'] % (host_name, port)
        params = {
            "user_id": user_id,
            "third_user_id": third_user_id,
            "title": title,
            "category_id": category_id,
            "file_extension": file_extension
        }
        r = requests.request(method, url, params=params, headers={'Connection': 'close'})
        r.raise_for_status()
        file_name = str(time.time())
        if file_extension != '':
            file_name = file_name + '.' + file_extension
        return send_file(io.BytesIO(r.content), attachment_filename=file_name)


@FILE_BP.route('/delete', methods=['POST'])
def delete():
    """删除文件

    POST 请求form表单 {"api_key": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx}
        返回json 成功 {"data": [], "status": 0}
                失败 {"data": [], "status": 1}
    """
    if request.method == 'POST':
        api_key = request.form['api_key']
        third_user_id = request.form['third_user_id']
        title = request.form['title']
        category_id = request.form['category_id']

        user = User(MYSQL_POOL)
        user_id = user.get_user_id_by_api_key(api_key)
        if user_id is None:
            return {"data": [], "status": 0}

        file = File(MYSQL_POOL)
        file_extension = file.get_file_extension(user_id, third_user_id, title, category_id)
        if file_extension is None:
            return {"data": [], "status": 0}

        redis_op = RediOP(REDIS_CLI)
        host_name, port = redis_op.get_best_frws_host_name_port()
        if host_name is None and port is None:
            return {"data": [], "status": 0}

        u = settings.FRWS_API_TEMPLATE['delete']
        method = u['method￿']
        url = u['url'] % (host_name, port)
        form_data = {
            "user_id": user_id,
            "third_user_id": third_user_id,
            "title": title,
            "category_id": category_id,
            "file_extension": file_extension
        }
        r = requests.request(method, url, data=form_data, headers={'Connection': 'close'})
        r.raise_for_status()
        if r.json()['status'] != 0:
            return {"data": [], "status": 1}
        else:
            return {"data": [], "status": 0}


@FILE_BP.route('/edit', methods=['POST'])
def edit():
    """编辑文件，user_id, title, category_id, file_extension

    POST 请求form表单 {
                    "api_key": xxx,
                    "src_third_user_id": xxx,
                    "new_third_user_id": xxx,
                    "src_title": xxx,
                    "new_title": xxx,
                    "src_category_id": xxx,
                    "new_category_id": xxx,
                    "new_file_extension": xxx
                    }
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    if request.method == 'POST':
        api_key = request.form['api_key']
        src_third_user_id = request.form['src_third_user_id']
        new_third_user_id = request.form['new_third_user_id']
        src_title = request.form['src_title']
        new_title = request.form['new_title']
        src_category_id = request.form['src_category_id']
        new_category_id = request.form['new_category_id']

        new_file_extension = request.form['new_file_extension']
        user = User(MYSQL_POOL)
        user_id = user.get_user_id_by_api_key(api_key)
        if user_id is None:
            return {"data": [], "status": 0}

        file = File(MYSQL_POOL)
        src_file_extension = file.get_file_extension(user_id, src_third_user_id, src_title, src_category_id)

        redis_op = RediOP(REDIS_CLI)
        host_name, port = redis_op.get_best_frws_host_name_port()
        if host_name is None and port is None:
            return {"data": [], "status": 0}

        u = settings.FRWS_API_TEMPLATE['edit']
        method = u['method￿']
        url = u['url'] % (host_name, port)
        form_data = {
            "user_id": user_id,
            "src_third_user_id": src_third_user_id,
            "new_third_user_id": new_third_user_id,
            "src_title": src_title,
            "new_title": new_title,
            "src_category_id": src_category_id,
            "new_category_id": new_category_id,
            "src_file_extension": src_file_extension,
            "new_file_extension": new_file_extension
        }
        r = requests.request(method, url, data=form_data, headers={'Connection': 'close'})
        r.raise_for_status()
        if r.json()['status'] != 0:
            return {"data": [], "status": 1}
        else:
            return {"data": [], "status": 0}