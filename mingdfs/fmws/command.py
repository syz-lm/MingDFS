from gevent import monkey

monkey.patch_all()
import argparse
import logging
import json
import os
from mingdfs.fmws.stat_process import start_stat



def main(log_level=logging.DEBUG):
    logging.basicConfig(level=log_level, format='%(levelname)s:%(asctime)s:%(name)s[%(message)s]')

    parser = argparse.ArgumentParser('欢迎使用fmws。')

    parser.add_argument('--SECRET_KEY', type=str, default='mm5201314',
                        help='输入SESSION盐值：默认，mm5201314')

    parser.add_argument('--MYSQL_CONFIG', type=json.loads, default='{"host": "serv_pro", "user": "root", "passwd": "mm5201314", "db": "mingdfs", "size": 5}',
                        help=("输入服务器MYSQL配置：默认，"
                              '{"host": "serv_pro", "user": "root", "passwd": "mm5201314", "db": "mingdfs", "size": 5}'))

    parser.add_argument('--MAIL_CONFIG', type=json.loads, default='{"host": "smtp.qq.com", "port": 465, "username": "858556393@qq.com", "password": "hacnvlxplaqkbbhj", "forget_password_msg": "[XXX: MingDFS] 您的验证码: %d"}',
                        help=('输入mail配置：默认，'
                              '{"host": "smtp.qq.com", "port": 465, "username": "858556393@qq.com", "password": "hacnvlxplaqkbbhj", "forget_password_msg": "[XXX: MingDFS] 您的验证码: 替换验证码"}'))

    parser.add_argument('--REDIS_CONFIG', type=json.loads, default='{"host": "serv_pro", "port": 6379, "db": 0, "passwd": "mm5201314"}',
                        help=('输入redis配置：默认，'
                              '{"host": "serv_pro", "port": 6379, "db": 0, "passwd": "mm5201314"}'))

    parser.add_argument('--HOST_NAME', type=str, default='fmws0',
                        help='输入fmws服务host name：默认，fmws0')

    parser.add_argument('--HOST', type=str, default='0.0.0.0',
                        help='输入fmws服务运行地址：默认，0.0.0.0')

    parser.add_argument('--PORT', type=int, default=15675,
                        help='输入fmws服务端口：默认，15675')

    parser.add_argument('--FMWS_KEY', type=str, default='mm5201314',
                        help='输入fmws服务访问key：默认，mm5201314')

    parser.add_argument('--FRWS_KEY', type=str, default='mm5201314',
                        help='输入fmws服务端口：默认，mm5201314')

    parser.add_argument('--FMWS_CACHE', type=str, default='/mnt/hgfs/mingdfs/fmws_cache',
                        help='输入fmws缓冲区路径：默认，/mnt/hgfs/mingdfs/fmws_cache')

    parser.add_argument('--STAT_INTERVAL', type=int, default=30,
                        help='输入统计进程执行间隔：默认，30秒')

    parser.add_argument('--PROCESS_TYPE', type=int, default=0,
                        help='输入启动的进程类别: 0: fmws, 1: stat_process')

    flags = parser.parse_args()
    try:
        _read_command_line(flags)
    except:
        import traceback
        logging.error(traceback.format_exc())


def _read_command_line(flags):
    from mingdfs.fmws import settings

    settings.SECRET_KEY = flags.SECRET_KEY
    settings.MYSQL_CONFIG = flags.MYSQL_CONFIG
    settings.MAIL_CONFIG = flags.MAIL_CONFIG
    settings.REDIS_CONFIG = flags.REDIS_CONFIG
    settings.HOST_NAME = flags.HOST_NAME

    settings.FMWS_KEY = flags.FMWS_KEY
    settings.FRWS_KEY = flags.FRWS_KEY

    settings.HOST = flags.HOST
    settings.PORT = flags.PORT

    settings.FMWS_CACHE = flags.FMWS_CACHE

    logging.debug('MAIL_CONFIG: %s', str(settings.MAIL_CONFIG))
    if not os.path.exists(settings.FMWS_CACHE):
        os.makedirs(settings.FMWS_CACHE, exist_ok=True)

    if flags.PROCESS_TYPE == 0:
        from mingdfs.fmws import apps
        apps.init_mr()
        apps.init_app()

        try:
            apps.start_fmws(settings.HOST, settings.PORT)
            # apps.debug(settings.HOST, settings.PORT)
        finally:
            apps.MYSQL_POOL.release()
            apps.REDIS_CLI.close()
    else:
        start_stat(flags.STAT_INTERVAL)


if __name__ == '__main__':
    main()