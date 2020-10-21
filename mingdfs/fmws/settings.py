import os

# session 盐值
SECRET_KEY = 'mm5201314'

MYSQL_CONFIG = {
    "host": 'serv_pro',
    "user": "root",
    "passwd": "mm5201314",
    "db": "mingdfs",
    "size": 5
}

IS_LOGIN = 'user_id'

MAIL_CONFIG = {
    'host': "smtp.qq.com",
    'port': 465,
    'username': '858556393@qq.com',
    'password': 'xikqxdjcuctpbdge',
    'forget_password_msg': "%d"
}

REDIS_CONFIG = {
    "host": 'serv_pro',
    "port": 6379,
    "db": 0,
    "passwd": 'mm5201314'
}

TEMPLATES_FOLDER = "../templates"
STATIC_FOLDER = "../static"


HOST_NAME = 'fmws0'
HOST = '0.0.0.0'
PORT = 15675
FMWS_KEY = 'mm5201314'
FRWS_KEY = 'mm5201314'

FMWS_CACHE = '/mnt/hgfs/mingdfs/fmws_cache'

FRWS_API_TEMPLATE = {
    'upload': {
        'method': 'post',
        'url': 'https://%s:%d/file/upload'
    },
    'download': {
        'method': 'post',
        'url': 'https://%s:%d/file/download'
    },
    'edit': {
        'method': 'post',
        'url': 'https://%s:%d/file/edit'
    },
    'delete': {
        'method': 'post',
        'url': 'https://%s:%d/file/delete'
    },
    'stat': {
        'method': 'get',
        'url': 'https://%s:%d/file/stat'
    },
    'delete_rollback': {
        'method': 'get',
        'url': 'https://%s:%d/file/delete_rollback'
    },
    'get_video_first_photo': {
        'method': 'post',
        'url': 'https://%s:%d/file/get_video_first_photo'
    }
}

CACHE_FRWS_STAT_INFOR_KEY = 'mingdfs_frws_stat_infor'
CACHE_FRWS_COMPUTERS_KEY = 'mingdfs_frws_computers'
CACHE_STAT_INTERVAL_KEY = 'mingdfs_stat_interval'

# 仅在统计信息中使用的一个索引
CACHE_STAT_BEST_FRWS_KEY = 'best_frws'

SSL_KEYFILE = os.path.split(os.path.realpath(__file__))[0] + os.sep + "server.key"
SSL_CERTFILE = os.path.split(os.path.realpath(__file__))[0] + os.sep + "server.crt"
