import unittest
import requests
import os
import time

from mingdfs.frws.settings import HOST_NAME, PORT

small_file = "../prototype/small_video.mp4"
url = "http://%s:%d/file" % (HOST_NAME, PORT)
download_dir = './download_dir'
if not os.path.exists(download_dir):
    os.mkdir(download_dir)

class Test(unittest.TestCase):
    def test_upload(self):
        go = '/upload'
        form_data = {
            "user_id": 'xxx',
            "title": 'xxx',
            "category_id": 'xxx',
            "file_extension": 'mp4',
            "file_size": os.path.getsize(small_file)
        }
        upload_files = {
            'upload_file_name': open(small_file, 'rb')
        }
        r = requests.get(url + go, data=form_data, files=upload_files)
        r.raise_for_status()

    def test_download(self):
        go = '/download'
        args = {"user_id": 'xxx', "title": 'xxx', "category_id": 'xxx', "file_extension": 'mp4'}
        r = requests.get(url + go, params=args)
        save_file = download_dir + os.path.sep + str(time.time()) + '.mp4'
        with open(save_file, 'wb') as f:
            f.write(r.content)
        print(r.url)

    def test_edit(self):
        pass

    def test_stat(self):
        pass

    def test_delete(self):
        pass