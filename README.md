# MingDFS

一个Python编写的分布式文件系统。

![](https://raw.githubusercontent.com/kfxce/MingDFS/master/logo.gif)

## FMWS

```
$ fmws --help
usage: 欢迎使用fmws。 [-h] [--SECRET_KEY SECRET_KEY] [--MYSQL_CONFIG MYSQL_CONFIG] [--MAIL_CONFIG MAIL_CONFIG] [--REDIS_CONFIG REDIS_CONFIG] [--HOST_NAME HOST_NAME] [--HOST HOST] [--PORT PORT]
                 [--FMWS_KEY FMWS_KEY] [--FRWS_KEY FRWS_KEY] [--FMWS_CACHE FMWS_CACHE] [--STAT_INTERVAL STAT_INTERVAL] [--PROCESS_TYPE PROCESS_TYPE]

optional arguments:
  -h, --help            show this help message and exit
  --SECRET_KEY SECRET_KEY
                        输入SESSION盐值：默认，mm5201314
  --MYSQL_CONFIG MYSQL_CONFIG
                        输入服务器MYSQL配置：默认，{"host": "serv_pro", "user": "root", "passwd": "mm5201314", "db": "mingdfs", "size": 5}
  --MAIL_CONFIG MAIL_CONFIG
                        输入mail配置：默认，{"host": "smtp.qq.com", "port": 465, "username": "858556393@qq.com", "password": "hacnvlxplaqkbbhj", "forget_password_msg": "[XXX: MingDFS] 您的验证码: 替换验证码"}
  --REDIS_CONFIG REDIS_CONFIG
                        输入redis配置：默认，{"host": "serv_pro", "port": 6379, "db": 0, "passwd": "mm5201314"}
  --HOST_NAME HOST_NAME
                        输入fmws服务host name：默认，fmws0
  --HOST HOST           输入fmws服务运行地址：默认，0.0.0.0
  --PORT PORT           输入fmws服务端口：默认，15675
  --FMWS_KEY FMWS_KEY   输入fmws服务访问key：默认，mm5201314
  --FRWS_KEY FRWS_KEY   输入fmws服务端口：默认，mm5201314
  --FMWS_CACHE FMWS_CACHE
                        输入fmws缓冲区路径：默认，/mnt/hgfs/mingdfs/fmws_cache
  --STAT_INTERVAL STAT_INTERVAL
                        输入统计进程执行间隔：默认，30秒
  --PROCESS_TYPE PROCESS_TYPE
                        输入启动的进程类别: 0: fmws, 1: stat_process
```

启动成功之后，打开浏览器输入http://serv_pro:15673/就会显示登陆页面，serv_pro:15673由用户指定的ip和域名。

## FRWS

```
$ frws --help
usage: 欢迎使用frws。 [-h] [--HOST HOST] [--IP IP] [--PORT PORT] [--HOST_NAME HOST_NAME] [--FMWS_HOST_NAME FMWS_HOST_NAME] [--FMWS_IP FMWS_IP] [--FMWS_PORT FMWS_PORT] [--FMWS_KEY FMWS_KEY]
                 [--FRWS_KEY FRWS_KEY] [--SAVE_DIRS SAVE_DIRS [SAVE_DIRS ...]] [--REDIS_CONFIG REDIS_CONFIG] [--SECRET_KEY SECRET_KEY] [--PROCESS_TYPE PROCESS_TYPE]

optional arguments:
  -h, --help            show this help message and exit
  --HOST HOST           输入服务器运行地址：默认，0.0.0.0
  --IP IP               输入服务器IP：默认，127.0.0.1
  --PORT PORT           输入服务器端口：默认，15676
  --HOST_NAME HOST_NAME
                        输入frws主机名：默认，frws0
  --FMWS_HOST_NAME FMWS_HOST_NAME
                        输入fmws主机名：默认，fmws0
  --FMWS_IP FMWS_IP     输入FMWS服务器IP：默认，127.0.0.1
  --FMWS_PORT FMWS_PORT
                        输入fmws服务端口：默认，15675
  --FMWS_KEY FMWS_KEY   输入fmws服务访问key：默认，mm5201314
  --FRWS_KEY FRWS_KEY   输入fmws服务端口：默认，mm5201314
  --SAVE_DIRS SAVE_DIRS [SAVE_DIRS ...]
                        输入服务器存储路径列表：默认，['/mnt/hgfs/mingdfs/frws']
  --REDIS_CONFIG REDIS_CONFIG
                        输入redis配置：默认，{"host": "serv_pro", "port": 6379, "db": 0, "passwd": "mm5201314"}
  --SECRET_KEY SECRET_KEY
                        输入SESSION盐值：默认，mm5201314
  --PROCESS_TYPE PROCESS_TYPE
                        输入进程类型：0: frws, 1: register_frws

```
## 命令行参数例子

* frws
```
frws --IP 192.168.101.4 --PORT 15676 --HOST_NAME frws0 --PROCESS_TYPE 0 --FMWS_IP 192.168.101.4 --FMWS_PORT 15675 --FMWS_HOST_NAME fmws0 --SAVE_DIRS E:\mingdfs\frws --BACKUP_DIR E:\mingdfs\frws_backup --REDIS_CONFIG {\"host\":\"192.168.101.4\",\"port\":6379,\"db\":0,\"passwd\":\"mm5201314\"}
```

* frws_register_process
```
fmws_register_process --IP 192.168.101.4 --PORT 15676 --HOST_NAME frws0 --PROCESS_TYPE 1 --FMWS_IP 192.168.101.4 --FMWS_PORT 15675 --FMWS_HOST_NAME fmws0 --SAVE_DIRS E:\mingdfs\frws --BACKUP_DIR E:\mingdfs\frws_backup --REDIS_CONFIG {\"host\":\"192.168.101.4\",\"port\":6379,\"db\":0,\"passwd\":\"mm5201314\"}
```

* fmws
```
fmws --MYSQL_CONFIG {\"host\":\"192.168.101.4\",\"user\":\"root\",\"passwd\":\"mm5201314\",\"db\":\"mingdfs\",\"size\":5} --REDIS_CONFIG {\"host\":\"192.168.101.4\",\"port\":6379,\"db\":0,\"passwd\":\"mm5201314\"} --HOST_NAME fmws0 --HOST 0.0.0.0 --PORT 15675 --FMWS_CACHE E:\mingdfs\fmws_cache --PROCESS_TYPE 0
```

* fmws_stat_process
```
fmws_stat_process --MYSQL_CONFIG {\"host\":\"192.168.101.4\",\"user\":\"root\",\"passwd\":\"mm5201314\",\"db\":\"mingdfs\",\"size\":5} --REDIS_CONFIG {\"host\":\"192.168.101.4\",\"port\":6379,\"db\":0,\"passwd\":\"mm5201314\"} --HOST_NAME fmws0 --HOST 0.0.0.0 --PORT 15675 --FMWS_CACHE E:\mingdfs\fmws_cache --PROCESS_TYPE 1
```

**XX: Windows下json输入参数，双引号必须转义，且不能有空格**