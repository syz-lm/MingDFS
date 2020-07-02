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
        'url': 'http://%s:%d/file/upload'
    },
    'download': {
        'method': 'post',
        'url': 'http://%s:%d/file/download'
    },
    'edit': {
        'method': 'post',
        'url': 'http://%s:%d/file/edit'
    },
    'delete': {
        'method': 'post',
        'url': 'http://%s:%d/file/delete'
    },
    'stat': {
        'method': 'get',
        'url': 'http://%s:%d/file/stat'
    }
}


CACHE_FRWS_STAT_INFOR_KEY = 'frws_stat_infor'
CACHE_FRWS_COMPUTERS_KEY = 'frws_computers'
CACHE_STAT_INTERVAL_KEY = 'stat_interval'

CACHE_STAT_BEST_FRWS_KEY = 'best_frws'