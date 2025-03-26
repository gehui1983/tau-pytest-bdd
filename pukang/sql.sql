create TABLE  distrit_code(
       `id` INT NOT NULL AUTO_INCREMENT COMMENT '自增ID',
       `code` varchar(8) CHARACTER set utf8mb4 COLLATE utf8mb4_general_ci not null comment '编码：1-省和直辖市,2-市,3-县和区',
       `name` varchar(24) CHARACTER set utf8mb4 COLLATE utf8mb4_general_ci not null comment '名称：1-省和直辖市,2-市,3-县和区',
       `parent_code` varchar(8) CHARACTER set utf8mb4 COLLATE utf8mb4_general_ci  not null DEFAULT '000000' comment '上级行政编码,1-省和直辖市, 2-市',
       `level` INT NOT NULL COMMENT '级别：1-省和直辖市,2-市,3-县和区',
        PRIMARY KEY (`id`) USING BTREE,
        KEY `code` (`code`) USING BTREE,
        KEY `parent_code` (`parent_code`) USING BTREE
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

