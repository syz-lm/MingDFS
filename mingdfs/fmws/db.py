from mingdfs.db_mysql import MySQLBase


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

    SQL:
        注册
        insert into user(user_name, money, api_key, register_time, email, passwd, last_login_time)
                    value('xxx', 100, 'xxx', 15242342, 'xxx@xx.xx', 'xxx', 123123123)
        登录
        select id from user where user_name = %s and passwd = %s
        API访问
        select id from user where api_key = 'xxx'
        修改密码
        update user set passwd = 'xxx' where user_name = 'xxx' and email = 'xxx@xx.xx'
        充值
        select money from user where user_name = 'xxx' and passwd = 'xxx'
        update user set money = 12312 where user_name = 'xxx' and passwd = 'xxx'
    """
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

    SQL:
        上传文件
        insert into file(user_id, title, category_id, add_time, last_edit_time, last_access_time, file_size, file_extension,
                        third_user_id)
                    value(xxx, 'xxx', xxx, 12412231, 12312, 1231231, 12312, 'xxx', xxx)
        删除文件
        delete from file
            where user_id = xxx and title = 'xxx' and category_id = 'xxx' and third_user_id = xxx
        修改文件(不修改文件内容)
        update file set third_user_id = xxx, title = 'xxx', category_id = 'xxx', last_edit_time = xxx,
                    file_size = xxx, file_extension = xxx
            where user_id = xxx and third_user_id = xxx and category_id = xxx and title = 'xxx'
        修改文件内容(先删除，再重新上传)
        delete from file
            where user_id = xxx and title = 'xxx' and category_id = 'xxx' and third_user_id = xxx
        insert into file(user_id, title, category_id, add_time, last_edit_time, last_access_time, file_size, file_extension,
                        third_user_id)
                    value(xxx, 'xxx', xxx, 12412231, 12312, 1231231, 12312, 'xxx', xxx)
    """
    def upload_file(self, user_id, title, category_id, add_time, last_edit_time, last_access_time, file_size, file_extension,
                    third_user_id):
        sql = ("insert into file(user_id, title, category_id, add_time, last_edit_time, last_access_time, file_size, file_extension,"
               "third_user_id)"
               "value(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        args = (user_id, title, category_id, add_time, last_edit_time, last_access_time, file_size, file_extension,
                third_user_id)
        affect_rows = self.mysql_pool.edit(sql, args)
        if affect_rows != 0:
            return True
        else:
            return False

    def delete_file(self, user_id, third_user_id, title, category_id):
        sql = "delete from file where user_id = %s and title = %s and category_id = %s and third_user_id = %s"
        args = (user_id, third_user_id, title, category_id)
        affect_rows = self.mysql_pool.edit(sql, args)
        if affect_rows != 0:
            return True
        else:
            return False

    def edit_file(self, user_id, src_third_user_id, new_third_user_id,
                  src_title, new_title, src_category_id, new_category_id,
                  last_edit_time, src_file_size, new_file_size,
                  src_file_extension, new_file_extension):
        sql = ("update file set third_user_id = %s, title = %s, category_id = %s, last_edit_time = %s,"
               "file_size = %s, file_extension = %s"
               "where user_id = %s and third_user_id = %s and category_id = %s and title = %s"
               " and file_size = %s and file_extension = %s")
        args = (new_third_user_id, new_title, new_category_id, last_edit_time, new_file_size, new_file_extension,
                user_id, src_third_user_id, src_category_id, src_title, src_file_size, src_file_extension)
        affect_rows = self.mysql_pool.edit(sql, args)
        if affect_rows != 0:
            return True
        else:
            return False