import argparse
import logging
import os
from mingdfs.frws import start_frws, register_frws


def main(log_level=logging.DEBUG):
    logging.basicConfig(level=log_level, format='%(levelname)s:%(asctime)s:%(name)s[%(message)s]')

    parser = argparse.ArgumentParser('欢迎使用frws。')

    parser.add_argument('--HOST', type=str, default='0.0.0.0',
                        help='输入服务器IP：默认，0.0.0.0')

    parser.add_argument('--PORT', type=int, default='15676',
                        help='输入服务器端口：默认，15676')

    parser.add_argument('--HOST_NAME', type=str, default='frws0',
                        help='输入服务器注册主机名：默认，frws0')

    parser.add_argument('--REGISTER_API', type=str, default='http://fmws:15675/register_frws',
                        help='输入注册API：默认，http://fmws:15675/register_frws')

    # --HOST 0.0.0.0 --PORT 15676 --HOST_NAME frws0 --SAVE_DIRS / /home /usr
    parser.add_argument('--SAVE_DIRS', type=str, nargs='+', default=[], help='输入服务器存储路径列表：默认，[]')

    flags = parser.parse_args()
    try:
        _read_command_line(flags)
    except KeyboardInterrupt:
        import traceback
        logging.error(traceback.format_exc())


def _read_command_line(flags):
    from mingdfs.frws import settings

    settings.HOST = flags.HOST
    settings.PORT = flags.PORT
    settings.HOST_NAME = flags.HOST_NAME
    settings.REGISTER_API = flags.REGISTER_API
    settings.SAVE_DIRS = flags.SAVE_DIRS
    if len(settings.SAVE_DIRS) == 0:
        logging.error('存储磁盘不能为空')
        return
    else:
        for save_dir in settings.SAVE_DIRS:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)  # mkdir -p
    if 0 == register_frws(settings.HOST_NAME, settings.HOST, settings.PORT, settings.REGISTER_API):
        logging.error('注册服务器失败')
        return
    start_frws(settings.HOST, settings.PORT)


if __name__ == '__main__':
    main()