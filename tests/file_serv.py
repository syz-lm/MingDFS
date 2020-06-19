from flask import Flask, request, send_from_directory
from os.path import sep

save_path = './file_serv_save'
app = Flask(__name__)


@app.route('/', methods=['GET'])
def upload_file():
    """上传文件

    GET 请求form表单 {"file_name": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    if request.method == 'GET':
        try:
            file_name = request.form['file_name']
            file = request.files['file_name']
            file.save(save_path + sep + file_name)

            return {"data": [], "status": 1}
        except Exception as e:
            print(e)
            return {"data": [], "status": 0}


@app.route('/view', methods=['GET'])
def view_file():
    """获取文件

    GET 请求url参数 {"file_name": xxx}
        返回json成功 {"data": [], "status": 1}
               失败 {"data": [], "status": 0}
    """
    if request.method == 'GET':
        file_name = request.args.get('file_name')
        return send_from_directory(save_path, file_name)


if __name__ == '__main__':
    app.run(host='localhost', port=9001, debug=True)