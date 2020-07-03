# MingDFS

一个Python编写的分布式文件系统。

![](http://serv_pro:3000/zswj123/MingDFS/raw/master/logo.gif)

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

文件资源服务器的配置和启动。

## 企业API

```
$ pip3.8 install requests requests-toolbelt
```

* 上传文件：
  * api_key: 用户需要到fmws官网注册账号，注册之后，fmws会给用户分配一个api_key
  * category_id: 用户这边的分类id，必须是字符串
  * third_user_id: 用户这边的用户id，必须是字符串
  * title: 用户这边的标题，必须是字符串
  * upload_file_name: 此为上传文件的名称，用于写在`<input type="file" name="upload_file_name">`
  * 请求url: 上传接口的地址，http://serv_pro:15673/file/upload，serv_pro和端口15673需由实际ip和端口替换
  * 请求方法: post请求表单并且上传文件
  * 代码例子:
    ```
    import requests
    from requests_toolbelt import MultipartEncoder
    from mimetypes import guess_type
    
    
    file_name = '你上传文件的文件名'
    file_path = '你上传文件的文件路径(包含文件名)'
    
    m = MultipartEncoder(fields={
        'api_key': api_key,
        'category_id': str(category_id),
        'third_user_id': str(third_user_id),
        'title': title,
        'upload_file_name': (file_name, open(file_path, 'rb'), guess_type(file_name)[0] or "application/octet-stream")
    })
    r = requests.post(upload_url, data=m, headers={'Content-Type': m.content_type})
    r.raise_for_status()
    jd = r.json()
    if jd['status'] == 0:
        print('上传失败')
    elif jd['status'] == 1:
        print('上传成功')
    else:
        print('不是服务端发送的数据')
    ```
* 下载文件
  * api_key: 用户需要到fmws官网注册账号，注册之后，fmws会给用户分配一个api_key
  * category_id: 用户这边的分类id，必须是字符串
  * third_user_id: 用户这边的用户id，必须是字符串
  * title: 用户这边的标题，必须是字符串
  * 请求方法: GET请求表单
  * 请求url: http://serv_pro:15673/file/download, serv_pro:15673由实际的ip和端口替换
  * 代码例子:
    ```
    $.ajax({
            type: 'GET',
            url: "/file/download",
            data: {
                'api_key': api_key,
                'third_user_id': third_user_id,
                'title': title,
                'category_id': category_id
            },
            cache: false,
            contentType: "application/x-www-form-urlencoded",
            dataType: "json",
            success: function (data) {
                // 如果status为1则表示获取下载url成功
                if (data.status == 1) {
                    var url = data.data[0]['url'];
                    // 用浏览器打开这个url浏览器就会自动下载该文件
                    window.open(url);
                } else {
                    alert('获取失败');
                }
            },
            error: function(err) {
                alert('网络错误');
            },
            async: true,
        });
    ```