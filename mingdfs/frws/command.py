from gevent import monkey

monkey.patch_all()

import argparse
import logging
import os
import json
from mingdfs.frws import start_frws, register_frws, debug_frws
import time
import socket
from mingdfs.utils import load_hosts, dump_hosts, add_hosts
from mingdfs.frws import settings
import traceback
from mingdfs import frws


def main(log_level=logging.DEBUG, debug=False):
    logging.basicConfig(level=log_level, format='%(levelname)s:%(asctime)s:%(name)s[%(message)s]')

    parser = argparse.ArgumentParser('欢迎使用frws。')

    parser.add_argument('--HOST', type=str, default='0.0.0.0',
                        help='输入服务器运行地址：默认，0.0.0.0')

    parser.add_argument('--IP', type=str, default='127.0.0.1',
                        help='输入服务器IP：默认，127.0.0.1')

    parser.add_argument('--PORT', type=int, default='15676',
                        help='输入服务器端口：默认，15676')

    parser.add_argument('--HOST_NAME', type=str, default='frws0',
                        help='输入frws主机名：默认，frws0')

    parser.add_argument('--FMWS_HOST_NAME', type=str, default='fmws0',
                        help='输入fmws主机名：默认，fmws0')

    parser.add_argument('--FMWS_IP', type=str, default='127.0.0.1',
                        help='输入FMWS服务器IP：默认，127.0.0.1')

    parser.add_argument('--FMWS_PORT', type=int, default=15675,
                        help='输入fmws服务端口：默认，15675')

    parser.add_argument('--FMWS_KEY', type=str, default='mm5201314',
                        help='输入fmws服务访问key：默认，mm5201314')

    parser.add_argument('--FRWS_KEY', type=str, default='mm5201314',
                        help='输入fmws服务端口：默认，mm5201314')

    # --HOST 0.0.0.0 --PORT 15676 --HOST_NAME frws0 --SAVE_DIRS / /home /usr
    parser.add_argument('--SAVE_DIRS', type=str, nargs='+', default=settings.SAVE_DIRS,
                        help='输入服务器存储路径列表：默认，%s' % settings.SAVE_DIRS)

    parser.add_argument('--REDIS_CONFIG', type=json.loads,
                        default='{"host": "serv_pro", "port": 6379, "db": 0, "passwd": "mm5201314"}',
                        help=('输入redis配置：默认，'
                              '{"host": "serv_pro", "port": 6379, "db": 0, "passwd": "mm5201314"}'))

    parser.add_argument('--SECRET_KEY', type=str, default='mm5201314',
                        help='输入SESSION盐值：默认，mm5201314')

    parser.add_argument('--PROCESS_TYPE', type=int, default=0, help='输入进程类型：0: frws, 1: register_frws')

    parser.add_argument('--BACKUP_DIR', type=str, default=settings.BACKUP_DIR,
                        help='输入备份文件的路径: 默认, /mnt/hgfs/mingdfs/frws_backup')

    flags = parser.parse_args()
    try:
        _read_command_line(flags, debug)
    except KeyboardInterrupt:
        logging.error(traceback.format_exc())


def _read_command_line(flags, debug):
    from mingdfs.frws import settings

    settings.HOST = flags.HOST
    settings.IP = flags.IP
    settings.PORT = flags.PORT
    settings.HOST_NAME = flags.HOST_NAME
    settings.FMWS_HOST_NAME = flags.FMWS_HOST_NAME
    settings.FMWS_IP = flags.FMWS_IP
    settings.FMWS_PORT = flags.FMWS_PORT

    settings.FMWS_KEY = flags.FMWS_KEY
    settings.FRWS_KEY = flags.FRWS_KEY

    settings.SAVE_DIRS = flags.SAVE_DIRS

    settings.REDIS_CONFIG = flags.REDIS_CONFIG
    settings.SECRET_KEY = flags.SECRET_KEY
    settings.BACKUP_DIR = flags.BACKUP_DIR

    logging.debug(
        'HOST: %s, IP: %s, PORT: %s, HOST_NAME: %s, FMWS_HOST_NAME: %s, FMWS_IP: %s, FMWS_PORT: %s, FMWS_KEY: %s, FRWS_KEY: %s, SAVE_DIRS: %s, REDIS_CONFIG: %s, SECRET_KEY: %s, BACKUP_DIR: %s',
        settings.HOST, settings.IP, settings.PORT, settings.HOST_NAME, settings.FMWS_HOST_NAME, settings.FMWS_IP,
        settings.FMWS_PORT, settings.FMWS_KEY,
        settings.FRWS_KEY, settings.SAVE_DIRS, str(settings.REDIS_CONFIG), settings.SECRET_KEY, settings.BACKUP_DIR)

    if settings.IP == '0.0.0.0':
        logging.error('IP不能为0.0.0.0，必须是外网地址')
        return

    if len(settings.SAVE_DIRS) == 0:
        logging.error('存储磁盘不能为空')
        return
    else:
        for save_dir in settings.SAVE_DIRS:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)  # mkdir -p

        if not os.path.exists(settings.BACKUP_DIR):
            os.makedirs(settings.BACKUP_DIR)

    def _hello():
        if 0 == register_frws(settings.HOST_NAME, settings.IP, settings.PORT,
                              settings.FMWS_KEY, settings.FMWS_HOST_NAME, settings.FMWS_PORT,
                              json.dumps(settings.SAVE_DIRS), settings.FRWS_KEY):
            logging.error('注册服务器失败')
            return
        else:
            logging.info('注册服务器成功')

    if flags.PROCESS_TYPE == 0:
        try:
            if not debug:
                start_frws(settings.HOST, settings.PORT)
            else:
                debug_frws(settings.HOST, settings.PORT)
        except:
            pass
        finally:
            if frws.REDIS_CLI: frws.REDIS_CLI.close()
    else:
        real_create_conn = socket.create_connection

        def set_src_addr(*args):
            address, timeout = args[0], args[1]
            source_address = (settings.IP, 0)
            return real_create_conn(address, timeout, source_address)

        socket.create_connection = set_src_addr

        ih = load_hosts()
        ih = add_hosts(ih, settings.FMWS_IP, settings.FMWS_HOST_NAME)
        dump_hosts(ih)

        while 1:
            try:
                _hello()
            except:
                pass
            time.sleep(30)


if __name__ == '__main__':
    main(debug=True)
