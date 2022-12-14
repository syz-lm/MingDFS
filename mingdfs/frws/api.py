import base64
import json
import os
import shutil
import time
import traceback

import psutil
from flask import request, Blueprint, send_from_directory, send_file

from mingdfs import frws
from mingdfs.frws import APP
from mingdfs.frws import settings
from mingdfs.utils import decrypt, decrypt_number, encrypt, crypt_number, get_video_num_image

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
                               "file_extension": xxx, "timestamp": xxx, "expire": xxx}
        返回 成功 json {"data": [{"proof": xxx}], "status": 1}
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
        timestamp = form_data.get('timestamp')
        # TODO
        expire = float(form_data.get('expire'))

        file_name = str(user_id) + '_' + str(third_user_id) + '_' + title + \
                    '_' + str(category_id)
        file_name = base64.standard_b64encode(file_name.encode()).decode()
        file_name = base64.standard_b64encode(file_name.encode()).decode()
        if file_extension != '':
            file_name = file_name + "." + file_extension

        for save_dir in settings.SAVE_DIRS:
            file_path = save_dir + os.path.sep + file_name
            if os.path.exists(file_path):
                # frws.REDIS_CLI.set(req_body, file_name, 60)
                q = 0
                fk_l = len(settings.OPERA_KEY)
                if fk_l < 16:
                    q = 16 - fk_l
                else:
                    q = fk_l % 16
                key = settings.OPERA_KEY
                if q != 0:
                    key += '0' * q
                now = time.time()
                form_data['expire'] = crypt_number(now + expire)
                form_data['timestamp'] = crypt_number(now)
                payload = encrypt(key, json.dumps(form_data))
                proof = base64.standard_b64encode(payload).decode()

                return {"data": [{'proof': proof}], "status": 1}
        return {"data": [], "status": 0}
    elif request.method == 'GET':
        proof = request.args.get('proof').encode()
        playload = base64.standard_b64decode(proof).decode()

        q = 0
        fk_l = len(settings.OPERA_KEY)
        if fk_l < 16:
            q = 16 - fk_l
        else:
            q = fk_l % 16
        key = settings.OPERA_KEY
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
        expire = decrypt_number(form_data.get('expire'))

        if file_extension != '':
            file_name = file_name + "." + file_extension

        # if frws.REDIS_CLI.get(playload) != file_name.encode():
        #     return {"data": [], "status": 0}
        now = time.time()
        if expire - now <= 0:
            return {"data": [], "status": 0}

        for save_dir in settings.SAVE_DIRS:
            file_path = save_dir + os.path.sep + file_name
            if os.path.exists(file_path):
                return send_from_directory(save_dir, file_name, attachment_filename=file_name)

        raise


@FILE_BP.route('/get_video_first_photo', methods=['GET', 'POST'])
def get_video_first_photo():
    """获取视频文件的第一帧

    POST 请求经过加密过的payload {"user_id": xxx, "third_user_id": xxx,
                               "title": xxx, "category_id": xxx,
                               "file_extension": xxx, "timestamp": xxx,
                               "expire": xxx}
        返回 成功 json {"data": [{"proof": xxx}], "status": 1}
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
        timestamp = form_data.get('timestamp')
        # TODO
        expire = float(form_data.get('expire'))

        file_name = str(user_id) + '_' + str(third_user_id) + '_' + title + \
                    '_' + str(category_id)
        file_name = base64.standard_b64encode(file_name.encode()).decode()
        file_name = base64.standard_b64encode(file_name.encode()).decode()
        if file_extension != '':
            file_name = file_name + "." + file_extension

        for save_dir in settings.SAVE_DIRS:
            file_path = save_dir + os.path.sep + file_name
            if os.path.exists(file_path):
                # frws.REDIS_CLI.set(req_body, file_name, 60)
                q = 0
                fk_l = len(settings.OPERA_KEY)
                if fk_l < 16:
                    q = 16 - fk_l
                else:
                    q = fk_l % 16
                key = settings.OPERA_KEY
                if q != 0:
                    key += '0' * q
                now = time.time()
                form_data['expire'] = crypt_number(now + expire)
                form_data['timestamp'] = crypt_number(now)
                payload = encrypt(key, json.dumps(form_data))
                proof = base64.standard_b64encode(payload).decode()

                return {"data": [{'proof': proof}], "status": 1}
        return {"data": [], "status": 0}
    elif request.method == 'GET':
        proof = request.args.get('proof').encode()
        playload = base64.standard_b64decode(proof).decode()

        q = 0
        fk_l = len(settings.OPERA_KEY)
        if fk_l < 16:
            q = 16 - fk_l
        else:
            q = fk_l % 16
        key = settings.OPERA_KEY
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
        expire = decrypt_number(form_data.get('expire'))

        if file_extension != '':
            file_name = file_name + "." + file_extension

        # if frws.REDIS_CLI.get(playload) != file_name.encode():
        #     return {"data": [], "status": 0}
        now = time.time()
        if expire - now <= 0:
            return {"data": [], "status": 0}

        for save_dir in settings.SAVE_DIRS:
            file_path = save_dir + os.path.sep + file_name
            if os.path.exists(file_path):
                return send_file(
                    get_video_num_image(file_path, num=50),
                    mimetype='image/png'
                )

        raise


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

        src_file_name = str(user_id) + '_' + str(src_third_user_id) + '_' + \
                        src_title + \
                        '_' + str(src_category_id)
        src_file_name = base64.standard_b64encode(src_file_name.encode()).decode()
        src_file_name = base64.standard_b64encode(src_file_name.encode()).decode()

        if src_file_extension != '':
            src_file_name = src_file_name + "." + src_file_extension

        new_file_name = str(user_id) + '_' + str(new_third_user_id) + '_' + \
                        new_title + \
                        '_' + str(new_category_id)
        new_file_name = base64.standard_b64encode(new_file_name.encode()).decode()
        new_file_name = base64.standard_b64encode(new_file_name.encode()).decode()

        if new_file_extension != '':
            new_file_name = new_file_name + "." + new_file_extension

        if src_file_name == new_file_name:
            return {"data": [], "status": 0}

        for save_dir in settings.SAVE_DIRS:
            src_save_file_name = save_dir + os.path.sep + src_file_name
            if not os.path.exists(src_save_file_name):
                continue

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
    """删除文件, post用于移动文件到备份区

    POST 请求加密的form表单 {"user_id": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx, "file_extension": xxx, "is_routine": xxx}
        返回json 成功 {"data": [], "status": 0}
                失败 {"data": [], "status": 1}

    XXX: 如果 is_routine 为1 则代表使用事务，0则代表不使用事务。使用事务的可以进行删除回滚，以及删除确认。
    """
    q = 0
    fk_l = len(settings.FMWS_KEY)
    if fk_l < 16:
        q = 16 - fk_l
    else:
        q = fk_l % 16
    key = settings.FMWS_KEY
    if q != 0:
        key += '0' * q

    if request.method == 'POST':
        try:
            req_body = request.get_data().decode()

            form_data = json.loads(decrypt(key, req_body))

            user_id = form_data['user_id']
            third_user_id = form_data['third_user_id']
            title = form_data['title']
            category_id = form_data['category_id']
            file_extension = form_data['file_extension']
            is_routine = form_data['is_routine']

            for save_dir in settings.SAVE_DIRS:
                file_name = str(user_id) + '_' + str(third_user_id) + '_' + title + \
                                 '_' + str(category_id)
                file_name = base64.standard_b64encode(file_name.encode()).decode()
                file_name = base64.standard_b64encode(file_name.encode()).decode()
                if file_extension != '':
                    file_name = file_name + "." + file_extension

                save_file_name = save_dir + os.path.sep + file_name
                if os.path.exists(save_file_name):
                    if is_routine == 1:
                        try:
                            backup_path = os.path.sep.join([settings.BACKUP_DIR, file_name])
                            shutil.move(save_file_name, backup_path)
                            frws.REDIS_CLI.set(file_name, save_file_name)  # 等待删除确认，用于回滚删除事务
                            return {"data": [], "status": 1}
                        except:
                            print(traceback.format_exc())
                            print('移动文件失败', save_file_name)
                            return {"data": [], 'status': 0}
                    elif is_routine == 0:
                        try:
                            os.remove(save_file_name)
                            return {"data": [], "status": 1}
                        except:
                            print(traceback.format_exc())
                            print('删除文件失败', save_file_name)
                            return {"data": [], "status": 0}
                    raise

            return {"data": [], "status": 0}
        except:
            print(traceback.format_exc())


@FILE_BP.route('/delete_rollback', methods=['GET'])
def delete_rollback():
    """，get用于删除确认，一旦确认成功，就将备份区的文件永久删除，
    若确认失败，就将备份区的文件还原到原先的位置。

    GET 请求加密的form表单 {"user_id": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx,
                          "file_extension": xxx, "ack_status": xxx}
        返回json 成功 {"data": [], "status": 0}
                失败 {"data": [], "status": 1}

    XXX: ack_status 为1 代表确认成功，0为确认失败
    """
    q = 0
    fk_l = len(settings.FMWS_KEY)
    if fk_l < 16:
        q = 16 - fk_l
    else:
        q = fk_l % 16
    key = settings.FMWS_KEY
    if q != 0:
        key += '0' * q

    if request.method == 'GET':
        try:
            req_body = request.get_data().decode()

            form_data = json.loads(decrypt(key, req_body))
            user_id = form_data['user_id']
            third_user_id = form_data['third_user_id']
            title = form_data['title']
            category_id = form_data['category_id']
            file_extension = form_data['file_extension']
            ack_status = form_data['ack_status']

            file_name = str(user_id) + '_' + str(third_user_id) + '_' + title + \
                        '_' + str(category_id)
            file_name = base64.standard_b64encode(file_name.encode()).decode()
            file_name = base64.standard_b64encode(file_name.encode()).decode()

            if file_extension != '':
                file_name = file_name + "." + file_extension

            backup_path = os.path.sep.join([settings.BACKUP_DIR, file_name])
            try:
                if ack_status == 1:
                    os.remove(backup_path)
                elif ack_status == 0:
                    save_file_path = frws.REDIS_CLI.get(file_name).decode()
                    shutil.move(backup_path, save_file_path)
                else:
                    raise

                frws.REDIS_CLI.delete(file_name)
            except:
                print(traceback.format_exc())
                return {"data": [], "status": 0}

            return {"data": [], "status": 1}
        except:
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