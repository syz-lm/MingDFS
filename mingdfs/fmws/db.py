import json
import logging
import math

from mingdfs.db_mysql import MySQLBase
from mingdfs.fmws import settings


class User(MySQLBase):
    """
    Table Name:
        user

    Fields:
        id int
        user_name str
        money int
        api_key str
        register_time int
        email str
        passwd str
        last_login_time int
    """
    def get_user_name_by_user_id(self, user_id):
        sql = 'select user_name from user where id = %s'
        args = (user_id,)
        results = self.mysql_pool.query(sql, args)
        if len(results) != 0:
            return results[0]['user_name']
        else:
            return None

    def get_api_key_by_user_id(self, user_id):
        sql = 'select api_key from user where id = %s'
        args = (user_id, )
        results = self.mysql_pool.query(sql, args)
        if results and len(results) != 0:
            return results[0]['api_key']
        else:
            return None

    def get_user_id_by_api_key(self, api_key):
        sql = 'select id from user where api_key = %s'
        args = (api_key, )
        results = self.mysql_pool.query(sql, args)
        if len(results) != 0:
            return results[0]['id']
        else:
            return None

    def exists(self, user_name, email):
        sql = "select id from user where user_name = %s or email = %s"
        args = (user_name, email)
        results = self.mysql_pool.query(sql, args)
        if len(results) != 0:
            return True
        else:
            return False

    def add_user(self, user_name, money, api_key, register_time, email, passwd, last_login_time):
        sql = ("insert into user(user_name, money, api_key, register_time, email, passwd, last_login_time)"
               "value(%s, %s, %s, %s, %s, %s, %s)")
        args = (user_name, money, api_key, register_time, email, passwd, last_login_time)
        affect_rows = self.mysql_pool.edit(sql, args)
        if affect_rows != 0:
            return True
        else:
            return False

    def login(self, user_name, passwd):
        sql = "select id from user where user_name = %s and passwd = %s"
        args = (user_name, passwd)
        result = self.mysql_pool.query(sql, args)
        if len(result) != 0:
            return result[0]['id']
        else:
            return None

    def change_passwd(self, passwd, user_name, email):
        sql = "update user set passwd = %s where user_name = %s and email = %s"
        args = (passwd, user_name, email)
        affect_rows = self.mysql_pool.edit(sql, args)
        return affect_rows != 0

    def _get_money(self, user_name, passwd):
        sql = "select money from user where user_name = %s and passwd = %s"
        args = (user_name, passwd)
        result = self.mysql_pool.query(sql, args)
        if len(result) != 0:
            return result[0]['money']
        else:
            return False

    def pay(self, user_name, passwd, money):
        left_money = self._get_money(user_name, passwd)
        if money != False:
            now_money = money + left_money
            sql = "update user set money = %s where user_name = %s and passwd = %s"
            args = (now_money, user_name, passwd)
            affect_rows = self.mysql_pool.edit(sql, args)
            if affect_rows != 0:
                return True
            else:
                return False


class FRWS(MySQLBase):
    """
    Table Name:
        frws

    Fields:
        id int
        host_name: str
        ip: str
        port: int
        save_dirs: str
        fmws_cache: str
        fmws_key: str
        frws_key: str
    """
    def exists(self, host_name, ip, port):
        sql = 'select id from frws where host_name = %s and ip = %s and port = %s'
        args = (host_name, ip, port)
        results = self.mysql_pool.query(sql, args)
        if results is not None and len(results) != 0:
            return True
        else:
            return False

    def add_frws(self, host_name, ip, port, save_dirs, fmws_key, frws_key):
        sql = ("insert into frws(host_name, ip, port, save_dirs, fmws_key, frws_key) "
               "values(%s, %s, %s, %s, %s, %s)")

        args = (host_name, ip, port, save_dirs, fmws_key, frws_key)
        an = self.mysql_pool.edit(sql, args)
        if an > 0: return True
        else: return False

    def get_host_name_port_by_file_id(self, file_id):
        sql = 'select host_name, port from frws where id = (select frws_id from file where id = %s)'
        args = (file_id, )
        results = self.mysql_pool.query(sql, args)
        print('debug', results, args)
        if results is not None and len(results) != 0:
            return results[0]
        else:
            return {}

    def get_frws_id_by_host_name_port(self, host_name, port):
        sql = 'select id from frws where host_name = %s and port = %s'
        args = (host_name, port)
        results = self.mysql_pool.query(sql, args)
        if results is not None and len(results) != 0:
            return results[0]['id']
        else:
            return None


class File(MySQLBase):
    """
    Table Name:
        file

    Fields:
        id int
        user_id int
        third_user_id Any
        title str
        category_id Any
        add_time int
        last_edit_time int
        last_access_time int
        file_size int
        file_extension str
        frws_id int
    """

    def get_file_id(self, user_id, third_user_id, title, category_id):
        sql = 'select id from file where user_id = %s and third_user_id = %s and title = %s and category_id = %s'
        args = (user_id, third_user_id, title, category_id)
        results = self.mysql_pool.query(sql, args)
        if results is not None and len(results) != 0:
            return results[0]['id']
        else:
            return None

    def get_frws_id_host_name_port(self, user_id, third_user_id, title, category_id):
        sql = 'select a.frws_id as frws_id, b.host_name as host_name, b.port as port from file a inner join frws b on a.frws_id = b.id where a.user_id = %s and a.third_user_id = %s and a.title = %s and category_id = %s'
        args = (user_id, third_user_id, title, category_id)
        results = self.mysql_pool.query(sql, args)
        if results is not None and len(results) != 0:
            return results[0]
        else:
            return None

    def get_total_pages_by_user_id(self, user_id):
        sql = 'select count(id) as count from file where user_id = %s'
        args = (user_id, )
        results = self.mysql_pool.query(sql, args)
        if results is not None and len(results) != 0:
            count = results[0]['count']
            return math.ceil(count / 25)
        else:
            return None

    def all_file_size(self, user_id):
        sql = 'select sum(file_size) as all_file_size from file where user_id = %s'
        args = (user_id, )
        results = self.mysql_pool.query(sql, args)
        if results is not None and len(results) != 0:
            return results[0]['all_file_size']
        else:
            return None

    def page_files(self, user_id, page):
        sql = ("""
                select
                    third_user_id,
                    title,
                    category_id,
                    add_time,
                    last_edit_time,
                    last_access_time,
                    file_size,
                    file_extension
                from file
                where
                    user_id = %s 
                order by id desc, last_access_time desc 
                limit %s, 25
                """)
        args = (user_id, (page - 1) * 25)

        results = self.mysql_pool.query(sql, args)
        if results != None and len(results) != 0:
            return results
        else:
            return []

    def get_file_extension(self, user_id, third_user_id, title, category_id):
        sql = 'select file_extension from file where user_id = %s and third_user_id = %s and title = %s and category_id = %s'
        args = (user_id, third_user_id, title, category_id)
        results = self.mysql_pool.query(sql, args)
        if len(results) != 0:
            return results[0]['file_extension']
        else:
            return None

    def get_file_extension_file_id(self, user_id, third_user_id, title, category_id):
        sql = 'select file_extension, id from file where user_id = %s and third_user_id = %s and title = %s and category_id = %s'
        args = (user_id, third_user_id, title, category_id)
        results = self.mysql_pool.query(sql, args)
        if len(results) != 0:
            return results[0]
        else:
            return None

    def get_file_extension_host_name_port(self, user_id, third_user_id, title, category_id):
        sql = 'select a.file_extension as file_extension, b.host_name as host_name, b.port as port from file a inner join frws b on a.frws_id = b.id where a.user_id = %s and a.third_user_id = %s and a.title = %s and a.category_id = %s'
        args = (user_id, third_user_id, title, category_id)
        results = self.mysql_pool.query(sql, args)
        if len(results) != 0:
            return results[0]
        else:
            return None

    def get_file_extension_host_name_port_ip(self, user_id, third_user_id, title, category_id):
        sql = 'select a.file_extension as file_extension, b.host_name as host_name, b.port as port, b.ip as ip from file a inner join frws b on a.frws_id = b.id where a.user_id = %s and a.third_user_id = %s and a.title = %s and a.category_id = %s'
        args = (user_id, third_user_id, title, category_id)
        print(sql % args)
        results = self.mysql_pool.query(sql, args)
        if len(results) != 0:
            return results[0]
        else:
            return None

    def get_file_extension_host_name_port_file_size(self, user_id, third_user_id, title, category_id):
        sql = 'select a.file_extension as file_extension, b.host_name as host_name, b.port as port, a.file_size as file_size from file a inner join frws b on a.frws_id = b.id where a.user_id = %s and a.third_user_id = %s and a.title = %s and a.category_id = %s'
        args = (user_id, third_user_id, title, category_id)
        results = self.mysql_pool.query(sql, args)
        if len(results) != 0:
            return results[0]
        else:
            return None

    def exists(self, user_id, third_user_id, title, category_id):
        sql = 'select id from file where user_id = %s and third_user_id = %s and title = %s and category_id = %s'
        args = (user_id, third_user_id, title, category_id)
        results = self.mysql_pool.query(sql, args)
        if len(results) != 0:
            return True
        else:
            return False

    def upload_file(self, user_id, title, category_id, add_time, last_edit_time, last_access_time, file_size, file_extension,
                    third_user_id, frws_id):
        sql = ("insert into file(user_id, title, category_id, add_time, last_edit_time, last_access_time, file_size, file_extension,"
               "third_user_id, frws_id)"
               "value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        args = (user_id, title, category_id, add_time, last_edit_time, last_access_time, file_size, file_extension,
                third_user_id, frws_id)
        affect_rows = self.mysql_pool.edit(sql, args)
        if affect_rows != 0:
            return True
        else:
            return False

    def delete_file(self, user_id, third_user_id, title, category_id):
        sql = "delete from file where user_id = %s and title = %s and category_id = %s and third_user_id = %s"
        args = (user_id, title, category_id, third_user_id)
        print(sql, args)
        affect_rows = self.mysql_pool.edit(sql, args)
        if affect_rows != 0:
            return True
        else:
            return False

    def edit_last_access_time(self, user_id, third_user_id, title, category_id, last_access_time):
        sql = "update file set last_access_time = %s where user_id = %s and third_user_id = %s and title = %s and category_id = %s"
        args = (last_access_time, user_id, third_user_id, title, category_id)
        af = self.mysql_pool.edit(sql, args)
        if af != 0:
            return True
        else:
            return False

    def edit_file(self, user_id, src_third_user_id, new_third_user_id,
                  src_title, new_title, src_category_id, new_category_id,
                  last_edit_time,
                  src_file_extension, new_file_extension, frws_id):
        sql = ("update file set third_user_id = %s, title = %s, category_id = %s, last_edit_time = %s,"
               "file_extension = %s, frws_id = %s "
               "where user_id = %s and third_user_id = %s and category_id = %s and title = %s"
               " and file_extension = %s")
        args = (new_third_user_id, new_title, new_category_id, last_edit_time, new_file_extension,
                frws_id, user_id, src_third_user_id, src_category_id, src_title, src_file_extension)
        affect_rows = self.mysql_pool.edit(sql, args)
        if affect_rows != 0:
            return True
        else:
            return False


class RediOP:
    def __init__(self, redis_cli):
        self.redis_cli = redis_cli

    def get_best_frws_host_name_port(self):
        stat_infor = self.redis_cli.get(settings.CACHE_FRWS_STAT_INFOR_KEY)
        if stat_infor is None:
            return {"data": [], "status": 0}
        logging.debug('stat_infor: %s', stat_infor)
        stat_infor = json.loads(stat_infor.decode())
        print("stat_infor", stat_infor)
        best_frws = stat_infor[settings.CACHE_STAT_BEST_FRWS_KEY]

        host_name = None
        port = None
        for k, v in best_frws.items():
            host_name = k
            port = v['port']
            break
        if host_name != None and port != None:
            return host_name, port
        else:
            return None, None