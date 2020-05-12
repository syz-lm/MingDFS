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
  `plat_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

```sql
CREATE TABLE `file_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(255) NOT NULL,
  `add_time` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

```sql
CREATE TABLE `plat` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plat_name` varchar(255) NOT NULL,
  `plat_add_time` int NOT NULL,
  `plat_web_site` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

```sql
CREATE TABLE `plat_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `md5_uid` varchar(255) NOT NULL,
  `plat_id` int NOT NULL,
  `add_time` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```