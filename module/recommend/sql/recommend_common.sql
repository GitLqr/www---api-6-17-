
##########online##########
#描述：用户最近推送记录 
CREATE TABLE IF NOT EXISTS user_recent_push_item_id_list (
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    uid VARCHAR(255) NOT NULL, 
    item_id_list MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    UNIQUE (uid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#描述：用户最近推送理由
CREATE TABLE IF NOT EXISTS user_recent_push_feature_list (
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    uid VARCHAR(255) NOT NULL, 
    item_feature_list MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    UNIQUE(uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#描述：用户最近喜欢记录 
CREATE TABLE IF NOT EXISTS user_recent_favor_item_id_list (
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    uid VARCHAR(255) NOT NULL, 
    resource_type VARCHAR(8), 
    item_id_list MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    CONSTRAINT uc_uid_resource_type UNIQUE (uid, resource_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX user_recent_favor_item_id_list_uid_index ON user_recent_favor_item_id_list (uid);
CREATE INDEX user_recent_favor_item_id_list_resourcetype_index ON user_recent_favor_item_id_list (resource_type);

#描述：用户即时兴趣 
CREATE TABLE IF NOT EXISTS user_recent_feature_list (
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    uid VARCHAR(255) NOT NULL, 
    resource_type VARCHAR(8), 
    user_feature_list MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    CONSTRAINT uc_uid_resource_type UNIQUE (uid, resource_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX user_recent_feature_list_uid_index ON user_recent_feature_list (uid);
CREATE INDEX user_recent_feature_list_resourcetype_index ON user_recent_feature_list (resource_type);

#描述：用户即时资源偏好 
CREATE TABLE IF NOT EXISTS user_recent_resource_visit_info (
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    uid VARCHAR(255) NOT NULL, 
    resource_type VARCHAR(8), 
    visit_info MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    CONSTRAINT uc_uid_resource_type UNIQUE (uid, resource_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX user_recent_resource_visit_info_uid_index ON user_recent_resource_visit_info (uid);
CREATE INDEX user_recent_resource_visit_info_resourcetype_index ON user_recent_resource_visit_info (resource_type);

##########offline global##########
#描述：资源的热门feature列表 
CREATE TABLE IF NOT EXISTS resource_hot_feature_list(
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    resource_type VARCHAR(8) NOT NULL, 
    item_feature_list MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    UNIQUE(resource_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#描述：用户资源偏好 
CREATE TABLE IF NOT EXISTS user_resource_visit_info(
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    uid VARCHAR(255) NOT NULL, 
    resource_type VARCHAR(8), 
    visit_info MEDIUMBLOB, 
    PRIMARY KEY (`id`),
    CONSTRAINT uc_uid_resource_type UNIQUE (uid, resource_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX user_resource_visit_info_uid_index ON user_resource_visit_info(uid);
CREATE INDEX user_resource_visit_info_resourcetype_index ON user_resource_visit_info (resource_type);

#描述：记录离线端数据更新状态
CREATE TABLE IF NOT EXISTS offline_update_status(
    `id` bigint(10) NOT NULL AUTO_INCREMENT, 
    day_index VARCHAR(16) NOT NULL, 
    db_update_time DATETIME, 
    status VARCHAR(32), 
    try_times INT, 
    cache_update_time DATETIME, 
    PRIMARY KEY (`id`),
    UNIQUE (day_index)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
