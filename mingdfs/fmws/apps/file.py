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
from decimal import Decimal
import base64


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
        third_user_id = request.form.get('third_user_id', '0');
        title = request.form['title']
        category_id = request.form.get('category_id', '0');

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

            save_path = settings.FMWS_CACHE + os.path.sep + my_file.filename
            try:
                my_file.save(save_path)
            except:
                logging.error(traceback.format_exc())
                print('文件存储失败', save_path)
                return {"data": [], 'status': 0}

            u = settings.FRWS_API_TEMPLATE['upload']
            f = None
            method = None
            url = None
            try:
                file_size = os.path.getsize(save_path)

                method = u['method']
                f = open(save_path, 'rb')
                url = u['url'] % (host_name, port)
                files = {'upload_file_name': f}
                form_data = {
                    'user_id': user_id,
                    'third_user_id': third_user_id,
                    'title': title,
                    'category_id': category_id,
                    'file_extension': file_extension,
                    'file_size': file_size
                }
                r = requests.request(method, url, data=form_data, files=files)
                r.raise_for_status()
                if r.json()['status'] != 0:
                    add_time = int(time.time())
                    last_edit_time = add_time
                    last_access_time = 0
                    if not file.upload_file(user_id, title, category_id, add_time, last_edit_time,
                                            last_access_time, file_size, file_extension, third_user_id):
                        return {"data": [], "status": 0}
                    else:
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
        method = u['method']
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

        method = u['method']
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
            if file.delete_file(user_id, third_user_id, title, category_id) is not True:
                print(1)

                return {"data": [], "status": 0}
            else:
                return {"data": [], "status": 1}
        else:
            print(1)
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

        method = u['method']
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
            file = File(MYSQL_POOL)
            if not file.edit_file(user_id, src_third_user_id, new_third_user_id,
                                  src_title, new_title, src_category_id, new_category_id,
                                  int(time.time()), src_file_extension, new_file_extension):
                print("frws文件已经修改成功，但是数据库中修改失败", user_id, src_third_user_id, new_third_user_id,
                                  src_title, new_title, src_category_id, new_category_id,
                                  int(time.time()), src_file_extension, new_file_extension)
                return {"data": [], "status": 0}
            else:
                return {"data": [], "status": 1}
        else:
            return {"data": [], "status": 0}


@FILE_BP.route('/page_files', methods=['POST'])
def page_files():
    """分页获取文件

    POST 请求form表单 {"api_key": xxx, "page": xxx}
        返回json 成功 {"data": [{
                        "third_user_id": xxx,
                        "title": xxx,
                        "category_id": xxx,
                        "add_time": xxx,
                        "last_edit_time": xxx,
                        "last_access_time": xxx,
                        "file_size": xxx,
                        "file_extension": xxx,
                        "file_name": xxx
                    }], "status": 1}
                失败 {"data": [], "status": 0}

    XXX: 就这直接返回数据有点不太好，这相当于暴露了数据库的设计方案，但是前端那里又能根据页面和数据字段
    猜出，所以，隐藏也是不可能的，除非前端那里做闭源。所以，这是多虑了。
    """
    if request.method == 'POST':
        api_key = request.form['api_key']
        page = int(request.form['page'])

        user = User(MYSQL_POOL)
        user_id = user.get_user_id_by_api_key(api_key)
        if user_id is None:
            return {"data": [], "status": 0}

        file = File(MYSQL_POOL)
        files = file.page_files(user_id, page)
        for f in files:
            f['file_name'] = str(user_id) + '_' + f['third_user_id'] + '_' + base64.standard_b64encode(f['title'].encode()).decode() + \
                         '_' + f['category_id'] + "." + f['file_extension']

        return {"data": files, "status": 1}


@FILE_BP.route("/all_file_size", methods=['POST'])
def all_file_size():
    """统计该用户所有的文件总大小

    POST 请求form表单 {"api_key": xxx}
        返回json 成功 {"data": [{"all_file_size": xxx}], "status": 1}
                失败 {"data": [], "status": 0}
    """
    if request.method == 'POST':
        try:
            api_key = request.form['api_key']

            user = User(MYSQL_POOL)
            user_id = user.get_user_id_by_api_key(api_key)
            if user_id is None:
                return {"data": [], "status": 0}

            file = File(MYSQL_POOL)
            all_file_size: Decimal = file.all_file_size(user_id)

            if all_file_size is not None:
                return {"data": [{"all_file_size": int(all_file_size)}], "status": 1}
            else:
                return {"data": [], "status": 0}
        except:
            print(traceback.format_exc())


@FILE_BP.route("/get_total_pages", methods=['POST'])
def get_total_pages():
    """统计该用户总页数

    POST 请求form表单 {"api_key": xxx}
        返回json 成功 {"data": [{"total_pages": xxx}], "status": 1}
                失败 {"data": [], "status": 0}
    """
    if request.method == 'POST':
        try:
            api_key = request.form['api_key']

            user = User(MYSQL_POOL)
            user_id = user.get_user_id_by_api_key(api_key)
            if user_id is None:
                return {"data": [], "status": 0}

            file = File(MYSQL_POOL)
            total_pages = file.get_total_pages_by_user_id(user_id)

            if total_pages is not None:
                return {"data": [{"total_pages": total_pages}], "status": 1}
            else:
                return {"data": [], "status": 0}
        except:
            print(traceback.format_exc())