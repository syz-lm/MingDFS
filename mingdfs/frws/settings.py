import os

HOST = '0.0.0.0'
IP = '127.0.0.1'
PORT = 15676
HOST_NAME = 'frws0'
FMWS_HOST_NAME = 'fmws0'
FMWS_IP = '127.0.0.1'
FMWS_PORT = 15675

BACKUP_DIR = '/mnt/hgfs/mingdfs/frws_backup'

SAVE_DIRS = [
    '/mnt/hgfs/mingdfs/frws'
]

FMWS_KEY = 'mm5201314'
FRWS_KEY = 'mm5201314'

REDIS_CONFIG = {
    "host": 'serv_pro',
    "port": 6379,
    "db": 0,
    "passwd": 'mm5201314'
}

SSL_KEYFILE = os.path.split(os.path.realpath(__file__))[0] + os.sep + "server.key"
SSL_CERTFILE = os.path.split(os.path.realpath(__file__))[0] + os.sep + "server.crt"

OPERA_KEY = os.urandom(16)
