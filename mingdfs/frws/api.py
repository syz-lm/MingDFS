import base64
import os
import time

import psutil
from flask import request, Blueprint, send_from_directory

from mingdfs.frws import settings
from mingdfs.frws import APP
from mingdfs.utils import decrypt
import json
from mingdfs import frws


FILE_BP = Blueprint('file_bp', __name__)

@APP.route('/hello', methods=['GET'])
def hello():
    """fmws发送校验
    GET 请求form表单 {"frws_key": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    if request.method == 'GET':
        frws_key = request.form['frws_key']
        if frws_key != settings.FRWS_KEY:
            return {"data": [], "status": 0}
        else:
            return {"data": [], "status": 1}


@FILE_BP.route('/upload', methods=['POST'])
def upload():
    """上传文件

    POST 请求加密后的form表单 {"user_id": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx, "file_extension": xxx, "file_size": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}

        XXX: file_size的单位为字节，1G = 1024 * 1024 * 1024(字节)
    """
    if request.method == "POST":
        playload = request.form['playload']

        q = 0
        fk_l = len(settings.FMWS_KEY)
        if fk_l < 16:
            q = 16 - fk_l
        else:
            q = fk_l % 16
        key = settings.FMWS_KEY
        if q != 0:
            key += '0' * q
        form_data = json.loads(decrypt(key, playload))

        user_id = form_data['user_id']
        third_user_id = form_data['third_user_id']
        title = form_data['title']
        category_id = form_data['category_id']
        file_extension = form_data['file_extension']
        file_size = int(form_data['file_size'])

        save_file_name = str(user_id) + '_' + str(third_user_id) + '_' + title + \
                         '_' + str(category_id)
        save_file_name = base64.standard_b64encode(save_file_name.encode()).decode()
        save_file_name = base64.standard_b64encode(save_file_name.encode()).decode()

        file = request.files['upload_file_name']
        upload_file_name = file.filename
        try:
            file_extension_name = upload_file_name.rsplit('.', 1)[1]
            if file_extension_name != file_extension:
                raise
            if file_extension != '':
                save_file_name += '.' + file_extension_name
        except:
            return {"data": [], "status": 0}

        can_save_dirs = []
        for save_dir in settings.SAVE_DIRS:
            sdiskusage = psutil.disk_usage(save_dir)

            if sdiskusage.free >= file_size:
                save_path = save_dir + os.path.sep + save_file_name
                if not os.path.exists(save_path):
                    can_save_dirs.append(save_dir)
                else:
                    return {"data": [], "status": 1}

        for can_save_dir in can_save_dirs:
            save_path = can_save_dir + os.path.sep + save_file_name
            try:
                file.save(save_path)
                return {"data": [], "status": 1}
            except Exception as e:
                print(save_path, '文件保存失败', str(e))
                return {"data": [], "status": 0}

        return {"data": [], "status": 0}


@FILE_BP.route('/download', methods=['GET', 'POST'])
def download():
    """下载文件

    POST 请求经过加密过的payload {"user_id": xxx, "third_user_id": xxx,
                               "title": xxx, "category_id": xxx,
                               "file_extension": xxx, "timestamp": xxx}
        返回 成功 json {"data": [], "status": 1}
            失败 json {"data": [], "status": 0}

    GET 请求url参数 { "payload": xxx}
        成功 返回 二进制数据
        失败 返回 json {"data": [], "status": 0}
    """
    if request.method == 'POST':
        req_body = request.get_data().decode()

        q = 0
        fk_l = len(settings.FMWS_KEY)
        if fk_l < 16:
            q = 16 - fk_l
        else:
            q = fk_l % 16
        key = settings.FMWS_KEY
        if q != 0:
            key += '0' * q
        form_data = json.loads(decrypt(key, req_body))

        user_id = form_data.get('user_id')
        third_user_id = form_data.get("third_user_id")
        title = form_data.get('title')
        category_id = form_data.get("category_id")
        file_extension = form_data.get('file_extension')
        file_name = str(user_id) + '_' + str(third_user_id) + '_' + title + \
                    '_' + str(category_id)
        file_name = base64.standard_b64encode(file_name.encode()).decode()
        file_name = base64.standard_b64encode(file_name.encode()).decode()
        if file_extension != '':
            file_name = file_name + "." + file_extension
        
        for save_dir in settings.SAVE_DIRS:
            file_path = save_dir + os.path.sep + file_name
            if os.path.exists(file_path):
                frws.REDIS_CLI.set(req_body, file_name)
                return {"data": [], "status": 1}
        return {"data": [], "status": 0}
    elif request.method == 'GET':
        proof = request.args.get('proof').encode()
        playload = base64.standard_b64decode(proof).decode()
        print('playload: %s' % playload)

        q = 0
        fk_l = len(settings.FMWS_KEY)
        if fk_l < 16:
            q = 16 - fk_l
        else:
            q = fk_l % 16
        key = settings.FMWS_KEY
        if q != 0:
            key += '0' * q

        form_data = json.loads(decrypt(key, playload.encode()))

        user_id = form_data.get('user_id')
        third_user_id = form_data.get("third_user_id")
        title = form_data.get('title')
        category_id = form_data.get("category_id")
        file_extension = form_data.get('file_extension')
        file_name = str(user_id) + '_' + str(third_user_id) + '_' + title + \
                    '_' + str(category_id)
        file_name = base64.standard_b64encode(file_name.encode()).decode()
        file_name = base64.standard_b64encode(file_name.encode()).decode()
        if file_extension != '':
            file_name = file_name + "." + file_extension

        if frws.REDIS_CLI.get(playload) != file_name.encode():
            return {"data": [], "status": 0}

        for save_dir in settings.SAVE_DIRS:
            file_path = save_dir + os.path.sep + file_name
            if os.path.exists(file_path):
                return send_from_directory(save_dir, file_name, attachment_filename=file_name)

        return {"data": [], "status": 0}


@FILE_BP.route('/edit', methods=['POST'])
def edit():
    """编辑文件，user_id, title, category_id, file_extension

       POST 请求加密的form表单 {
                        "user_id": xxx,
                        "src_third_user_id": xxx,
                        "new_third_user_id": xxx,
                        "src_title": xxx,
                        "new_title": xxx,
                        "src_category_id": xxx,
                        "new_category_id": xxx,
                        "src_file_extension": xxx,
                        "new_file_extension": xxx
                        }
           返回json 成功 {"data": [], "status": 1}
                   失败 {"data": [], "status": 0}
    """
    if request.method == "POST":
        req_body = request.get_data().decode()

        q = 0
        fk_l = len(settings.FMWS_KEY)
        if fk_l < 16:
            q = 16 - fk_l
        else:
            q = fk_l % 16
        key = settings.FMWS_KEY
        if q != 0:
            key += '0' * q
        form_data = json.loads(decrypt(key, req_body))

        user_id = form_data['user_id']

        src_third_user_id = form_data['src_third_user_id']
        src_title = form_data['src_title']
        src_category_id = form_data['src_category_id']
        src_file_extension = form_data['src_file_extension']
        new_title = form_data['new_title']
        new_category_id = form_data['new_category_id']
        new_file_extension = form_data['new_file_extension']
        new_third_user_id = form_data['new_third_user_id']

        for save_dir in settings.SAVE_DIRS:
            src_file_name = str(user_id) + '_' + str(src_third_user_id) + '_' + \
                                 src_title + \
                                 '_' + str(src_category_id)
            src_file_name = base64.standard_b64encode(src_file_name.encode()).decode()
            src_file_name = base64.standard_b64encode(src_file_name.encode()).decode()

            if src_file_extension != '':
                src_file_name = src_file_name + "." + src_file_extension

            src_save_file_name = save_dir + os.path.sep + src_file_name
            if not os.path.exists(src_save_file_name):
                continue

            new_file_name = str(user_id) + '_' + str(new_third_user_id) + '_' + \
                                 new_title + \
                                 '_' + str(new_category_id)
            new_file_name = base64.standard_b64encode(new_file_name.encode()).decode()
            new_file_name = base64.standard_b64encode(new_file_name.encode()).decode()

            if new_file_extension != '':
                new_file_name = new_file_name + "." + new_file_extension

            new_save_file_name = save_dir + os.path.sep + new_file_name
            if os.path.exists(new_save_file_name):
                return {"data": [], "status": 0}

            try:
                os.rename(src_save_file_name, new_save_file_name)
                return {"data": [], "status": 1}
            except Exception as e:
                print(e)
                return {"data": [], "status": 0}

        return {"data": [], "status": 0}


@FILE_BP.route('/delete', methods=['POST'])
def delete():
    """删除文件

    GET 请求加密的form表单 {"user_id": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx, "file_extension": xxx}
        返回json 成功 {"data": [], "status": 0}
                失败 {"data": [], "status": 1}
    """
    if request.method == 'POST':
        try:
            req_body = request.get_data().decode()

            q = 0
            fk_l = len(settings.FMWS_KEY)
            if fk_l < 16:
                q = 16 - fk_l
            else:
                q = fk_l % 16
            key = settings.FMWS_KEY
            if q != 0:
                key += '0' * q
            form_data = json.loads(decrypt(key, req_body))

            user_id = form_data['user_id']
            third_user_id = form_data['third_user_id']
            title = form_data['title']
            category_id = form_data['category_id']
            file_extension = form_data['file_extension']

            for save_dir in settings.SAVE_DIRS:
                file_name = str(user_id) + '_' + str(third_user_id) + '_' + title + \
                                 '_' + str(category_id)
                file_name = base64.standard_b64encode(file_name.encode()).decode()
                file_name = base64.standard_b64encode(file_name.encode()).decode()
                if file_extension != '':
                    file_name = file_name + "." + file_extension

                save_file_name = save_dir + os.path.sep + file_name
                if os.path.exists(save_file_name):
                    try:
                        os.remove(save_file_name)
                        return {"data": [], "status": 1}
                    except Exception as e:
                        print('删除文件失败', save_file_name, str(e))
                        return {"data": [],  'status': 0}

            return {"data": [], "status": 0}
        except:
            import traceback
            print(traceback.format_exc())


@FILE_BP.route('/stat', methods=['GET'])
def stat():
    """统计该服务器上的数据存储区的可用磁盘空间，CPU的使用百分比，内存使用百分比

    GET 请求
        返回json 成功 {"data":[{
                                "used_memory_percent": xxx,
                                "used_cpu_percent": xxx,
                                "disk_free": {
                                    "xxx": xxx,
                                    "aaa": xxx
                                }
                            }],
                    "status": 1}
                失败 {"data": [], "status": 0}
    """
    if request.method == 'GET':
        try:
            svmem = psutil.virtual_memory()
            used_memory_percent = svmem.percent

            used_cpu_percent = psutil.cpu_percent(interval=None, percpu=False)

            disk_free = {}
            for save_dir in settings.SAVE_DIRS:
                sdiskusage = psutil.disk_usage(save_dir)
                disk_free[save_dir] = sdiskusage.free

            return {"data": [{
                "used_memory_percent": used_memory_percent,
                "used_cpu_percent": used_cpu_percent,
                "disk_free": disk_free
                }],
                "status": 1
            }
        except Exception as e:
            print(e)
            return {"data": [], "status": 0}