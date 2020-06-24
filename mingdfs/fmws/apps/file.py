from flask import Blueprint, request

FILE_BP = Blueprint('file_bp', __name__)


@FILE_BP.route('/upload', methods=['POST'])
def upload():
    """上传文件

    POST 请求form表单 {"api_key": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    pass


@FILE_BP.route('/download', methods=['GET'])
def download():
    """下载文件

    GET 请求url参数 {"api_key": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx}
        返回 成功 二进制数据
            失败 json {"data": [], "status": 0}
    """
    pass


@FILE_BP.route('/delete', methods=['POST'])
def delete():
    """删除文件

    POST 请求form表单 {"api_key": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx}
        返回json 成功 {"data": [], "status": 0}
                失败 {"data": [], "status": 1}
    """
    pass


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
                    }
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    pass


@FILE_BP.route('/edit_file_content', methods=['POST'])
def edit_file_content():
    """编辑文件内容

    POST 请求form表单 {"api_key": xxx, "third_user_id": xxx, "title": xxx, "category_id": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    pass