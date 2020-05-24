# DATABASE

## 一、创建数据库和表的SQL语句

数据库为MySQL8。

```sql
create database mingdfs;
```

```sql
CREATE TABLE `file` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) NOT NULL,
  `file_size` int NOT NULL,
  `file_type_id` int NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `last_edit_time` int NOT NULL,
  `last_access_time` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_file_name_index` (`file_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```sql
CREATE TABLE `file_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(255) NOT NULL,
  `add_time` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```sql
CREATE TABLE `payment_flow` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `money` int NOT NULL,
  `add_time` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```sql
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `money` int NOT NULL COMMENT '余额',
  `integral` int NOT NULL COMMENT '积分',
  `api_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '商户使用api操作时不用登陆使用的标识',
  `user_id` int NOT NULL COMMENT 'SYX用户id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```sql
create unique index unique_file_name_index on file(file_name);
```