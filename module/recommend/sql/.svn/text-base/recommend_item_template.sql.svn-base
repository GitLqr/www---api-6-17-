
##############item:%(resource_type)s#############
#描述：根据用户推荐Item和理由列表 
CREATE TABLE IF NOT EXISTS %(resource_type)s_user_feature_item_id_list (
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    uid VARCHAR(255) NOT NULL, 
    feature_name_item_id_list MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    UNIQUE (uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#描述：用户feature偏好 
CREATE TABLE IF NOT EXISTS %(resource_type)s_user_feature_list(
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    uid VARCHAR(255) NOT NULL, 
    user_feature_list MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    UNIQUE (uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#描述：根据item得到推荐列表
CREATE TABLE IF NOT EXISTS %(resource_type)s_item_recommend_list(
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    item_id VARCHAR(32) NOT NULL, 
    item_id_list MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    UNIQUE (item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#描述：根据feature_name得到推荐列表 
CREATE TABLE IF NOT EXISTS %(resource_type)s_feature_recommend_list(
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    feature_name VARCHAR(200) NOT NULL, 
    item_id_list BLOB, 
    PRIMARY KEY (`id`),
    UNIQUE (feature_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#描述：获取item_feature列表
CREATE TABLE IF NOT EXISTS %(resource_type)s_item_feature_list(
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    item_id VARCHAR(32) NOT NULL, 
    item_feature_list MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    UNIQUE (item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#描述：获取new_item_id -> old_item_id
CREATE TABLE IF NOT EXISTS %(resource_type)s_item_id_new_to_old(
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    new_item_id VARCHAR(32) NOT NULL, 
    old_item_id TINYTEXT NOT NULL , 
    PRIMARY KEY (`id`),
    UNIQUE (new_item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
