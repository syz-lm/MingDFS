import requests
import os
import time
from unittest import TestCase

small_file = "small_video.mp4"
big_file = "/Volumes/GoodByeUbuntu/reborn/video/1584405236.4538555_Forrest.Gump.1994.BluRay.720p.AAC.x264-iSCG.mp4"
test_api = 'http://localhost:9000'
download_dir = './flask_test_download'


class Test(TestCase):
    def test_upload_small_video(self):
        files = {'file_name': open(small_file, 'rb')}
        r = requests.get(test_api, data={"file_name": small_file}, files=files)
        print(r.status_code)

    def test_view_small_video(self):
        r = requests.get(test_api + '/view', params={"file_name": small_file})
        save_file = download_dir + os.path.sep + str(time.time()) + '.mp4'
        with open(save_file, 'wb') as f:
            f.write(r.content)

    def test_upload_big_video(self):
        files = {'file_name': open(big_file, 'rb')}
        r = requests.get(test_api, data={"file_name": small_file}, files=files)
        print(r.status_code)

    def test_view_big_video(self):
        r = requests.get(test_api + '/view', params={"file_name": big_file})
        save_file = download_dir + os.path.sep + str(time.time()) + '.mp4'
        with open(save_file, 'wb') as f:
            f.write(r.content)

    def test_eye_host(self):
        r = requests.get(test_api + '/eye_host')
        print(r.text)