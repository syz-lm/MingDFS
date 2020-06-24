import base64
import os

import psutil
from flask import request, Blueprint, send_from_directory

from mingdfs.frws import settings
from mingdfs.frws import APP

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


@FILE_BP.route('/upload', methods=['GET'])
def upload():
    """上传文件

    GET 请求form表单 {"user_id": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx, "file_extension": xxx, "file_size": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}

        XXX: file_size的单位为字节，1G = 1024 * 1024 * 1024(字节)
    """
    if request.method == "GET":
        user_id = request.form['user_id']
        third_user_id = request.form['third_user_id']
        title = request.form['title']
        category_id = request.form['category_id']
        file_extension = request.form['file_extension']
        file_size = int(request.form['file_size'])

        save_file_name = str(user_id) + '_' + str(third_user_id) + '_' + base64.standard_b64encode(title.encode()).decode() + \
                         '_' + str(category_id)
        file = request.files['upload_file_name']
        upload_file_name = file.filename
        try:
            file_extension_name = upload_file_name.rsplit('.', 1)[1]
            if file_extension_name != file_extension:
                raise

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


@FILE_BP.route('/download', methods=['GET'])
def download():
    """下载文件

    GET 请求url参数 {"user_id": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx, "file_extension": xxx}
        返回 成功 二进制数据
            失败 json {"data": [], "status": 0}
    """
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        third_user_id = request.args.get("third_user_id")
        title = request.args.get('title')
        category_id = request.args.get("category_id")
        file_extension = request.args.get('file_extension')
        file_name = str(user_id) + '_' + str(third_user_id) + '_' + base64.standard_b64encode(title.encode()).decode() + \
                    '_' + str(category_id) + "." + file_extension

        for save_dir in settings.SAVE_DIRS:
            file_path = save_dir + os.path.sep + file_name
            if os.path.exists(file_path):
                return send_from_directory(save_dir, file_name)

        return {"data": [], "status": 0}


@FILE_BP.route('/edit', methods=['GET'])
def edit():
    """编辑文件，user_id, title, category_id, file_extension

       GET 请求form表单 {
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
    if request.method == "GET":
        user_id = request.form['user_id']

        src_third_user_id = request.form['src_third_user_id']
        src_title = request.form['src_title']
        src_category_id = request.form['src_category_id']
        src_file_extension = request.form['src_file_extension']
        new_title = request.form['new_title']
        new_category_id = request.form['new_category_id']
        new_file_extension = request.form['new_file_extension']
        new_third_user_id = request.form['new_third_user_id']

        for save_dir in settings.SAVE_DIRS:
            src_save_file_name = save_dir + os.path.sep + str(user_id) + '_' + str(src_third_user_id) + '_' + \
                                 base64.standard_b64encode(src_title.encode()).decode() + \
                                 '_' + str(src_category_id) + "." + src_file_extension
            if not os.path.exists(src_save_file_name):
                continue

            new_save_file_name = save_dir + os.path.sep + str(user_id) + '_' + str(new_third_user_id) + '_' + \
                                 base64.standard_b64encode(new_title.encode()).decode() + \
                                 '_' + str(new_category_id) + "." + new_file_extension

            if os.path.exists(new_save_file_name):
                return {"data": [], "status": 0}

            try:
                os.rename(src_save_file_name, new_save_file_name)
                return {"data": [], "status": 1}
            except Exception as e:
                print(e)
                return {"data": [], "status": 0}

        return {"data": [], "status": 0}


@FILE_BP.route('/delete', methods=['GET'])
def delete():
    """删除文件

    GET 请求form表单 {"user_id": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx, "file_extension": xxx}
        返回json 成功 {"data": [], "status": 0}
                失败 {"data": [], "status": 1}
    """
    if request.method == 'GET':
        user_id = request.form['user_id']
        third_user_id = request.form['third_user_id']
        title = request.form['title']
        category_id = request.form['category_id']
        file_extension = request.form['file_extension']

        for save_dir in settings.SAVE_DIRS:
            save_file_name = save_dir + os.path.sep + str(user_id) + '_' + str(third_user_id) + '_' + base64.standard_b64encode(title.encode()).decode() + \
                             '_' + str(category_id) + "." + file_extension
            if os.path.exists(save_file_name):
                try:
                    os.remove(save_file_name)
                    return {"data": [], "status": 1}
                except Exception as e:
                    print('删除文件失败', save_file_name, str(e))
                    return {"data": [],  'status': 0}

        return {"data": [], "status": 0}


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