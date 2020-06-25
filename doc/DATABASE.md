# DATABASE

## 一、创建数据库和表的SQL语句

数据库为MySQL8。

```sql
create database mingdfs;
```

```sql
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `money` int NOT NULL COMMENT '余额',
  `api_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '商户使用api操作时不用登陆使用的标识',
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '用户名',
  `register_time` int NOT NULL COMMENT '注册时间',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '邮箱',
  `passwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '密码',
  `last_login_time` int NOT NULL COMMENT '最后登录时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `file` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `third_user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `category_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `add_time` int NOT NULL,
  `last_edit_time` int NOT NULL,
  `last_access_time` int NOT NULL,
  `file_size` int NOT NULL,
  `file_extension` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE UNIQUE INDEX unique_user_name ON user(user_name);
CREATE UNIQUE INDEX unique_email ON user(email);
CREATE UNIQUE INDEX unique_api_key ON user(api_key);

CREATE UNIQUE INDEX unique_uttc ON file(user_id, third_user_id, title, category_id);
#drop index unique_uttc on file;
#下面这行索引key的长度会超过限制
#CREATE UNIQUE INDEX unique_uttcf ON file(user_id, third_user_id, title, category_id, file_extension);
```