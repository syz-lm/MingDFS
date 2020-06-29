# MingDFS

一个Python编写的分布式文件系统。

![](http://serv_pro:3000/zswj123/MingDFS/raw/master/logo.gif)

## FMWS

```
$ fmws --help
usage: 欢迎使用fmws。 [-h] [--SECRET_KEY SECRET_KEY] [--MYSQL_CONFIG MYSQL_CONFIG]
                 [--MAIL_CONFIG MAIL_CONFIG] [--REDIS_CONFIG REDIS_CONFIG]
                 [--HOST_NAME HOST_NAME] [--HOST HOST] [--PORT PORT]
                 [--FMWS_KEY FMWS_KEY] [--FRWS_KEY FRWS_KEY]
                 [--FMWS_CACHE FMWS_CACHE] [--STAT_INTERVAL STAT_INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  --SECRET_KEY SECRET_KEY
                        输入SESSION盐值：默认，mm5201314
  --MYSQL_CONFIG MYSQL_CONFIG
                        输入服务器MYSQL配置：默认，{"host": "serv_pro", "user": "root",
                        "passwd": "mm5201314", "db": "mingdfs", "size": 5}
  --MAIL_CONFIG MAIL_CONFIG
                        输入mail配置：默认，{"host": "smtp.qq.com", "port": 465,
                        "username": "858556393@qq.com", "password":
                        "xikqxdjcuctpbdge", "forget_password_msg":
                        "用户指定的错误信息"}
  --REDIS_CONFIG REDIS_CONFIG
                        输入redis配置：默认，{"host": "serv_pro", "port": 6379, "db":
                        0, "passwd": "mm5201314"}
  --HOST_NAME HOST_NAME
                        输入fmws服务host name：默认，fmws0
  --HOST HOST           输入fmws服务运行地址：默认，0.0.0.0
  --PORT PORT           输入fmws服务端口：默认，15675
  --FMWS_KEY FMWS_KEY   输入fmws服务访问key：默认，mm5201314
  --FRWS_KEY FRWS_KEY   输入fmws服务端口：默认，mm5201314
  --FMWS_CACHE FMWS_CACHE
                        输入fmws缓冲区路径：默认，/mnt/hgfs/mingdfs/fmws_cache
  --STAT_INTERVAL STAT_INTERVAL
                        输入统计进程执行间隔：默认，300秒

```

文件中间层服务器配置和启动。

## FRWS

```
$ frws --help
usage: 欢迎使用frws。 [-h] [--HOST HOST] [--IP IP] [--PORT PORT]
                 [--HOST_NAME HOST_NAME] [--FMWS_HOST_NAME FMWS_HOST_NAME]
                 [--FMWS_PORT FMWS_PORT] [--FMWS_KEY FMWS_KEY]
                 [--FRWS_KEY FRWS_KEY] [--SAVE_DIRS SAVE_DIRS [SAVE_DIRS ...]]

optional arguments:
  -h, --help            show this help message and exit
  --HOST HOST           输入服务器运行地址：默认，0.0.0.0
  --IP IP               输入服务器IP：默认，127.0.0.1
  --PORT PORT           输入服务器端口：默认，15676
  --HOST_NAME HOST_NAME
                        输入frws主机名：默认，frws0
  --FMWS_HOST_NAME FMWS_HOST_NAME
                        输入fmws主机名：默认，fmws0
  --FMWS_PORT FMWS_PORT
                        输入fmws服务端口：默认，15675
  --FMWS_KEY FMWS_KEY   输入fmws服务访问key：默认，mm5201314
  --FRWS_KEY FRWS_KEY   输入fmws服务端口：默认，mm5201314
  --SAVE_DIRS SAVE_DIRS [SAVE_DIRS ...]
                        输入服务器存储路径列表：默认，[]

```

文件资源服务器的配置和启动。