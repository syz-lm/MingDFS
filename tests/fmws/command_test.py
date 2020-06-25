import unittest
import subprocess
from mingdfs.fmws import command


class Test(unittest.TestCase):
    def main(self, times):
        try:
            p = subprocess.Popen(["/usr/local/python3.8/bin/python3.8", command.__file__,
                                  '--SECRET_KEY', 'asdf',
                                  '--MYSQL_CONFIG', '{"host": "serv_pro", "user": "root", "passwd": "mm5201314", "db": "mingdfs", "size": 5}',
                                  '--MAIL_CONFIG', '{"host": "smtp.qq.com", "port": 465, "username": "858556393@qq.com", "password": "xikqxdjcuctpbdge", "forget_password_msg": "用户指定的错误信息"}',
                                  '--REDIS_CONFIG', '{"host": "serv_pro", "port": 6379, "db": 0, "passwd": "mm5201314"}',
                                  '--HOST_NAME', 'fmws0',
                                  '--HOST', '0.0.0.0',
                                  '--PORT', '15675',
                                  '--FMWS_KEY', 'mm5201314',
                                  '--FRWS_KEY', 'mm5201314',
                                  '--FMWS_CACHE', '/mnt/hgfs/mingdfs/fmws_cache'], stdout=subprocess.PIPE)
            p.wait(timeout=times)
            print(p.stdout.read().decode())
        except subprocess.TimeoutExpired as e:
            print(e)
            p.kill()

    def test_main_3_seconds(self):
        self.main(3)

    def test_main_3600_seconds(self):
        self.main(3600)