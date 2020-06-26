from gevent import monkey

monkey.patch_all()

import argparse
import logging
import os
import time
from mingdfs.frws import start_frws, register_frws
from multiprocessing import Process


def main(log_level=logging.DEBUG):
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

    parser.add_argument('--FMWS_PORT', type=int, default=15675,
                        help='输入fmws服务端口：默认，15675')

    parser.add_argument('--FMWS_KEY', type=str, default='mm5201314',
                        help='输入fmws服务访问key：默认，mm5201314')

    parser.add_argument('--FRWS_KEY', type=str, default='mm5201314',
                        help='输入fmws服务端口：默认，mm5201314')

    # --HOST 0.0.0.0 --PORT 15676 --HOST_NAME frws0 --SAVE_DIRS / /home /usr
    from mingdfs.frws import settings
    parser.add_argument('--SAVE_DIRS', type=str, nargs='+', default=settings.SAVE_DIRS, help='输入服务器存储路径列表：默认，%s' % settings.SAVE_DIRS)

    flags = parser.parse_args()
    try:
        _read_command_line(flags)
    except KeyboardInterrupt:
        import traceback
        logging.error(traceback.format_exc())


def _read_command_line(flags):
    from mingdfs.frws import settings

    settings.HOST = flags.HOST
    settings.IP = flags.IP
    settings.PORT = flags.PORT
    settings.HOST_NAME = flags.HOST_NAME
    settings.FMWS_HOST_NAME = flags.FMWS_HOST_NAME
    settings.FMWS_PORT = flags.FMWS_PORT

    settings.FMWS_KEY = flags.FMWS_KEY
    settings.FRWS_KEY = flags.FRWS_KEY

    settings.SAVE_DIRS = flags.SAVE_DIRS

    logging.debug('HOST: %s, IP: %s, PORT: %s, HOST_NAME: %s, FMWS_HOST_NAME: %s, FMWS_PORT: %s, FMWS_KEY: %s, FRWS_KEY: %s, SAVE_DIRS: %s',
                  settings.HOST, settings.IP, settings.PORT, settings.HOST_NAME, settings.FMWS_HOST_NAME, settings.FMWS_PORT, settings.FMWS_KEY,
                  settings.FRWS_KEY, settings.SAVE_DIRS)

    if len(settings.SAVE_DIRS) == 0:
        logging.error('存储磁盘不能为空')
        return
    else:
        for save_dir in settings.SAVE_DIRS:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)  # mkdir -p

    def _hello():
        if 0 == register_frws(settings.HOST_NAME, settings.IP, settings.PORT,
                              settings.FMWS_KEY, settings.FMWS_HOST_NAME, settings.FMWS_PORT):
            logging.error('注册服务器失败')
        else:
            logging.info('注册服务器成功')

    check_p = Process(target=_hello)

    frws_p = Process(target=start_frws, args=(settings.HOST, settings.PORT))

    frws_p.daemon = True
    frws_p.start()

    time.sleep(5)
    check_p.start()

    frws_p.join()


if __name__ == '__main__':
    main()