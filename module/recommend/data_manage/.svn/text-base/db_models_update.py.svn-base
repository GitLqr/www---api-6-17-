#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-17
import sys
sys.path.append('.')

import os
import sys
import logging
#import log_conf
import model_connect

#logger = logging.getLogger('alinow_data_manage.models_handler')
logger = logging.getLogger('recommend.data_manage')

def do_db_excute(sql):
    db = model_connect.getdb()
    if None == db:
        logger.error('get db connect error.')
        return False
    logger.debug('get db connect success.')
    try:
        if isinstance(sql, unicode):
            sql = sql.encode('utf8')
        logger.debug('sql: %s' % sql)
        return db.executeEx(sql)
    except:
        logger.error('db insert data failed, error: %s' % str(sys.exc_info()))
        return False


def set_db_offline_user_resource_visitinfo(uid, resource_type, visit_info_data):
    sql = "insert into user_resource_visit_info(uid, resource_type, visit_info) values('%s', '%s', '%s')" % (uid, resource_type, visit_info_data)
    return do_db_excute(sql)

def set_db_offline_user_feature_list(uid, resource_type, user_feature_list_data):
    sql = "insert into %s_user_feature_list(uid, user_feature_list) values('%s', '%s')" % (resource_type, uid, user_feature_list_data)
    return do_db_excute(sql)

def set_db_offline_user_recommend_item_list(uid, resource_type, feature_name_item_id_list_data):
    sql = "insert into %s_user_feature_item_id_list(uid, feature_name_item_id_list) values('%s', '%s')" % (resource_type, uid, feature_name_item_id_list_data)
    return do_db_excute(sql)

def set_db_offline_item_recommend_item_list(item_id, resource_type, item_id_list_data):
    sql = "insert into %s_item_recommend_list(item_id, item_id_list) values('%s', '%s')" % (resource_type, item_id, item_id_list_data)
    return do_db_excute(sql)

def set_db_offline_item_features(item_id, resource_type, item_feature_list_data):
    sql = "insert into %s_item_feature_list(item_id, item_feature_list) values('%s', '%s')" % (resource_type, item_id, item_feature_list_data)
    return do_db_excute(sql)

def set_db_offline_feature_hot_item_list(feature_name, resource_type, item_id_list_data):
    sql = "insert into %s_feature_recommend_list(feature_name, item_id_list) values('%s', '%s')" % (resource_type, feature_name, item_id_list_data)
    return do_db_excute(sql)

def set_db_offline_global_hot_feature_list(resource_type, item_id_list_data):
    sql = "insert into resource_hot_feature_list(resource_type, item_feature_list) values('%s', '%s')" % (resource_type, item_id_list_data)
    return do_db_excute(sql)

def set_db_offline_item_id_new_to_old(resource_type, new_item_id, old_item_id):
    sql = "insert into %s_item_id_new_to_old(new_item_id, old_item_id) values('%s', '%s')" % (resource_type, new_item_id, old_item_id)
    return do_db_excute(sql)
