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
    
* 下载单个文件
  * api_key: 用户需要到fmws官网注册账号，注册之后，fmws会给用户分配一个api_key
  * category_id: 用户这边的分类id，必须是字符串
  * third_user_id: 用户这边的用户id，必须是字符串
  * title: 用户这边的标题，必须是字符串
  * 请求方法: GET请求表单
  * 请求url: http://serv_pro:15673/file/download, serv_pro:15673由实际的ip和端口替换
  * 代码例子:
    
    ```
    import requests
    
    download_url = 'http://serv_pro:15673/file/download'
    form_data = {
        'api_key': api_key,
        'third_user_id': third_user_id,
        'category_id': category_id,
        'title': title
    }
    r = requests.get(download_url, data=form_data)
    r.raise_for_status()
    jd = r.json()
    if jd['status'] == 0:
        print(None)
    elif jd['status'] == 1:
        # 下载地址
        print(jd['data'][0]['url'])
    else:
        raise
    ```
    
* 下载多个文件
  * api_key: 用户需要到fmws官网注册账号，注册之后，fmws会给用户分配一个api_key
  * category_id: 用户这边的分类id，必须是字符串
  * third_user_id: 用户这边的用户id，必须是字符串
  * title: 用户这边的标题，必须是字符串
  * 请求方法: GET请求表单
  * 请求url: http://serv_pro:15673/file/download_many, serv_pro:15673由实际的ip和端口替换
  * 代码例子:
  
    ```
    import requests
    
    download_url = 'http://serv_pro:15673/file/download_many'
    form_data = {
        'api_key': api_key,
        'data': [
            {
                'third_user_id': third_user_id,
                'category_id': category_id,
                'title': title
            }
        ]
    }
    r = requests.get(download_url, data=form_data)
    r.raise_for_status()
    jd = r.json()
    if jd['status'] == 0:
        print(None)
    elif jd['status'] == 1:
        # 下载地址，也就是原来的数据中增加了一个url
        print(jd['data']) # [{'third_user_id': xxx, 'category_id': xxx, 'title': xxx, 'url': xxx}]
    else:
        raise
    ```
    
* 编辑文件
  * api_key: 用户需要到fmws官网注册账号，注册之后，fmws会给用户分配一个api_key
  * src_category_id: 用户这边的分类id，旧的
  * src_third_user_id: 用户这边的用户id, 旧的
  * src_title: 用户这边的标题，旧的
  * src_file_extension: 文件的扩展名，旧的
  * new_category_id: 用户这边的分类id，新的
  * new_third_user_id: 用户这边的用户id, 新的
  * new_title: 用户这边的标题，新的
  * new_file_extension: 文件的扩展名，新的
  * upload_file_name: 此为上传文件的名称，用于写在`<input type="file" name="upload_file_name">`，可选参数，带了就修改文件内容，不带只是修改文件属性
  * 请求方法: POST请求表单
  * 请求url: http://serv_pro:15673/file/edit, serv_pro:15673由实际的ip和端口替换
  
    ```
    import requests
    from requests_toolbelt import MultipartEncoder
    from mimetypes import guess_type
    
    
    file_name = '你上传文件的文件名'
    file_path = '你上传文件的文件路径(包含文件名)'
    
    m = MultipartEncoder(fields={
        'api_key': api_key,
        'src_category_id': str(category_id),
        'src_third_user_id': str(third_user_id),
        'src_title': title,
        'src_file_extension': str(file_extension),
        'new_category_id': str(new_category_id),
        'new_third_user_id': str(new_third_user_id),
        'new_title': new_title,
        'new_file_extension': str(new_file_extension),
        #'upload_file_name': (file_name, open(file_path, 'rb'), guess_type(file_name)[0] or "application/octet-stream")
    })
    r = requests.post(upload_url, data=m, headers={'Content-Type': m.content_type})
    r.raise_for_status()
    jd = r.json()
    if jd['status'] != 0:
        print('修改成功')
    else:
        print('修改失败')
    ```
    
* 删除文件
  * api_key: 用户需要到fmws官网注册账号，注册之后，fmws会给用户分配一个api_key
  * category_id: 用户这边的分类id，必须是字符串
  * third_user_id: 用户这边的用户id，必须是字符串
  * title: 用户这边的标题，必须是字符串
  * 请求方法: POST请求表单
  * 请求url: http://serv_pro:15673/file/delete, serv_pro:15673由实际的ip和端口替换
  * 代码例子:
  
    ```
    import requests
    
    delete_url = 'http://serv_pro:15673/file/delete'
    form_data = {
        'api_key': api_key,
        'third_user_id': third_user_id,
        'category_id': category_id,
        'title': title
    }
    r = requests.post(delete_url, data=form_data)
    r.raise_for_status()
    jd = r.json()
    if jd['status'] == 0:
        print('删除失败')
    elif jd['status'] == 1:
        print('删除成功')
    else:
        raise
    ```