from unittest import TestCase


from mingdfs.fmws.apps import init_mr
from mingdfs.fmws.db import User, File
from mingdfs.fmws import settings

init_mr()

from mingdfs.fmws.apps import MYSQL_POOL, REDIS_CLI


class UserTest(TestCase):
    user = User(MYSQL_POOL)

    def test_add_user(self):
        print(self.user.add_user('xxx', 0, 'xxx', 1, 'xx@xx.xx', 'xxx', 1))

    def test_login(self):
        print(self.user.login('xxx', 'xxx'))

    def test_change_passwd(self):
        print(self.user.change_passwd('bbb', 'xxx', 'xx@xx.xx'))

    def test_pay(self):
        print(self.user.pay('xxx', 'bbb', 100))


class FileTest(TestCase):
    user = User(MYSQL_POOL)
    file = File(MYSQL_POOL)

    def test_upload_file(self):
        user_id = self.user.login('xxx', 'bbb')

        print(self.file.upload_file(user_id, 'xxx', 'xxx', 1, 1, 1, 1, 'mp4', 'xxx'))

    def test_delete_file(self):
        user_id = self.user.login('xxx', 'bbb')
        print(self.file.delete_file(user_id, 'bbb', 'bbb', 'bbb'))

    def test_edit_file(self):
        user_id = self.user.login('xxx', 'bbb')

        print(self.file.edit_file(user_id, 'xxx', 'bbb', 'xxx', 'bbb', 'xxx', 'bbb',
                                  2, 1, 2, 'mp4', 'flv'))


class Test(TestCase):
    def test_best_frws(self):
        stat_infor = REDIS_CLI.get(settings.CACHE_FRWS_STAT_INFOR_KEY)
        print(stat_infor)