from flask import Flask, request, send_file
import requests
import os
import io

config = {
    'file_serv_upload_url': 'http://localhost:9001',
    'file_serv_view_url': 'http://localhost:9001/view',
    'file_cache_dir': './file_cache'
}

app = Flask(__name__, static_folder='./web_serv_static',
            template_folder='./web_serv_templates')


@app.route('/', methods=['GET'])
def upload_file():
    """上传文件

    GET 请求form表单 {"file_name": xxx}
        返回json 成功 {"data": [], "status": 1}
                失败 {"data": [], "status": 0}
    """
    if request.method == 'GET':
        file_name = request.form['file_name']
        file = request.files['file_name']
        cache_file_name = config['file_cache_dir'] + os.path.sep + file_name
        file.save(cache_file_name)
        files = {'file_name': open(cache_file_name, 'rb')}
        try:
            r = requests.get(config['file_serv_upload_url'], data={'file_name': file_name}, files=files)
            os.remove(cache_file_name)

            return {"data": [], "status": 1}
        except Exception as e:
            print(e)
        finally:
            r.close()

        return {"data": [], "status": 0}


@app.route('/view', methods=['GET'])
def view_file():
    """获取文件

    GET 请求url参数 {"file_name": xxx}
        返回 二进制数据内容
    """
    if request.method == 'GET':
        file_name = request.args.get('file_name')
        try:
            r = requests.get(config['file_serv_view_url'], params={'file_name': file_name})
            return send_file(io.BytesIO(r.content), attachment_filename=file_name)
        except Exception as e:
            print(e)
        finally:
            r.close()


if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)