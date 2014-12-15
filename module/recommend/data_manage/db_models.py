#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-16
import sys
sys.path.append('.')

import os
import sys
import logging
#import log_conf
import model_connect
import cache_models
from data_def import DataDef

#logger = logging.getLogger('alinow_data_manage.models')
logger = logging.getLogger('recommend.data_manage')

def sql_list_to_str(str_list):
    sqlStr = ""
    for str in str_list:
        sqlStr += "'%s'," % str
    return sqlStr[:-1]

# return: (errorCode, {k: v, ...})
# require: sql语句查询返回必须两列，第一列为key，第二列为value
# exp: select k, v from table_name where k in ('k1','k2',...)
def sql_query_to_dct(sql):
    db = model_connect.getdb()
    if None == db:
        logger.error('get db connect error.')
        return (False, {})
    logger.debug('get db connect success.')
    res = {}
    try:
        logger.debug('sql: %s' % sql)
        #rs = db.query(sql.encode('utf8'))
        if isinstance(sql, unicode):
            sql = sql.encode('utf8')
        rs = db.query(sql)
        for rd in rs:
            key = rd[0]
            value = rd[1]
            if isinstance(key, unicode):
                #logger.debug('do encode utf8 raw_key: %s' % key)
                key = key.encode('utf8')
                #logger.debug('res key: %s' % key)
            if isinstance(value, unicode):
                value = value.encode('utf8')
            if key != key.strip():
                logger.warning('key has Illegal character space. key:%s' % key)
            res[key.strip()] = value
    except:
        logger.error('db query failed, error: %s' % str(sys.exc_info()))
        return (False, {})
    return (True, res)

def sql_multi_query_to_dct(sql_list):
    result = {}
    errorCode = True
    for sql in sql_list:
        ec, res = sql_query_to_dct(sql)
        errorCode = errorCode and ec
        for k, v in res.items():
            result[k] = v
    return (errorCode, result)

def split_itemid_list_to_resource_dct(itemid_list):
    resource_itemid_dct = {}
    for itemid in itemid_list:
        resource = DataDef.get_resource_type_from_item_id(itemid)
        if not resource_itemid_dct.has_key(resource):
            resource_itemid_dct[resource] = []
        resource_itemid_dct[resource].append(itemid)
    return resource_itemid_dct

def split_feature_name_list_to_resource_dct(feature_name_list):
    resource_featurename_dct = {}
    for featurename in feature_name_list:
        resource = DataDef.get_resource_type_from_feature_name(featurename)
        if not resource_featurename_dct.has_key(resource):
            resource_featurename_dct[resource] = []
        resource_featurename_dct[resource].append(featurename)
    return resource_featurename_dct

# return: (errorCode, {resource_type: data, ...})
def get_db_offline_user_resource_visitinfo(uid, resource_type_list):
    if len(resource_type_list) <= 0:
        logger.info('get db offline user resource visitinfo, resource_type_list is empty.')
        return (True, {})
    sql = "select resource_type, visit_info from user_resource_visit_info where uid='%s' and resource_type in (%s)" % (uid, sql_list_to_str(resource_type_list))
    return sql_query_to_dct(sql)

# return False or True
def get_db_offline_user_resource_visitinfo_all(resource_type):
    sql = "select uid, visit_info from user_resource_visit_info where resource_type = '%s'" % resource_type
    return sql_query_to_dct(sql)

def get_db_offline_user_feature_list_single(uid, resource_type):
    sql = "select uid, user_feature_list from %s_user_feature_list where uid = '%s'" % (resource_type, uid)
    return sql_query_to_dct(sql)

# return: (errorCode, {resource_type: data, ...})
def get_db_offline_user_feature_list(uid, resource_type_list):
    if len(resource_type_list) <= 0:
        logger.info('get db offline user feature list, resource type list is empty.')
        return (True, {})
    result = {}
    errorCode = True
    for resource_type in resource_type_list:
        ec, res = get_db_offline_user_feature_list_single(uid, resource_type)
        errorCode = errorCode and ec
        if res != {} and isinstance(res, dict) and res.has_key(uid):
            result[resource_type] = res[uid]
    return (errorCode, result)

def get_db_offline_user_feature_list_all(resource_type):
    sql = "select uid, user_feature_list from %s_user_feature_list" % resource_type
    return sql_query_to_dct(sql)

# user recommend itemlist
def get_db_offline_user_recommend_item_list_single(uid, resource_type):
    sql = "select uid, feature_name_item_id_list from %s_user_feature_item_id_list where uid='%s'" % (resource_type, uid)
    return sql_query_to_dct(sql)

# return: (errorCode, {resource_type: data, ...})
def get_db_offline_user_recommend_item_list(uid, resource_type_list):
    if len(resource_type_list) <= 0:
        logger.info('get db offline user recommend item list, resource type list is empty.')
        return (True, {})
    result = {}
    errorCode = True
    for resource_type in resource_type_list:
        ec,res = get_db_offline_user_recommend_item_list_single(uid, resource_type)
        errorCode = errorCode and ec
        if {} != res and isinstance(res, dict) and res.has_key(uid):
            result[resource_type] = res[uid]
    return (errorCode, result)

def get_db_offline_user_recommend_item_list_all(resource_type):
    sql = "select uid, feature_name_item_id_list from %s_user_feature_item_id_list" % resource_type
    return sql_query_to_dct(sql)

# item recommend item list
#def get_db_offline_item_recommend_item_list_resource_single(resource_type, itemid_list):
#    sql = 'select item_id, item_id_list from %s_item_recommend_list where item_id in (%s)' % (resource_type, sql_list_to_str(itemid_list))
#    return sql_query_to_dct(sql)

# return: (errorCode, {item_id: data, ...})
def get_db_offline_item_recommend_item_list(itemid_list):
    resource_itemid_dct = split_itemid_list_to_resource_dct(itemid_list) 
    errorCode = True
    result = {}
    sql_list = []
    for resource_type ,itemid_list in resource_itemid_dct.items():
        sql = 'select item_id, item_id_list from %s_item_recommend_list where item_id in (%s)' % (resource_type, sql_list_to_str(itemid_list))
        sql_list.append(sql)
    return sql_multi_query_to_dct(sql_list)

def get_db_offline_item_recommend_item_list_all(resource_type_list):
    sql_list = []
    for resource_type in resource_type_list:
        sql = 'select item_id, item_id_list from %s_item_recommend_list' % resource_type
        sql_list.append(sql)
    return sql_multi_query_to_dct(sql_list)

# item features
#def get_db_offline_item_features_resource_single(resource_type, itemid_list):
#    sql = 'select item_id, item_feature_list from %s_item_feature_list where item_id in (%s)' % (resource_type, sql_list_to_str(itemid_list))
#    return sql_query_to_dct(sql)

# return: (errorCode, {item_id: data, ...})
def get_db_offline_item_features(itemid_list):
    resource_itemid_dct = split_itemid_list_to_resource_dct(itemid_list)
    errorCode = True
    result = {}
    sql_list = []
    for resource_type ,itemid_list in resource_itemid_dct.items():
        sql = 'select item_id, item_feature_list from %s_item_feature_list where item_id in (%s)' % (resource_type, sql_list_to_str(itemid_list))
        sql_list.append(sql)
    return sql_multi_query_to_dct(sql_list)
     
def get_db_offline_item_features_all(resource_type_list):
    sql_list = []
    for resource_type in resource_type_list:
        sql = 'select item_id, item_feature_list from %s_item_feature_list' % resource_type
        sql_list.append(sql)
    return sql_multi_query_to_dct(sql_list)
     
# feature hot item list
#def get_db_offline_feature_hot_item_list_resource_single(resource_type, feature_name_list):
#    sql = 'select feature_name, item_id_list from %s_feature_recommend_list where feature_name in (%s)' % (resource_type, sql_list_to_str(feature_name_list))
#    return sql_query_to_dct(sql)

# return: (errorCode, {feature_names: data, ...})
def get_db_offline_feature_hot_item_list(feature_names):
    resource_featurename_dct = split_feature_name_list_to_resource_dct(feature_names)
    errorCode = True
    result = {}
    sql_list = []
    for resource_type, feature_name_list in resource_featurename_dct.items():
        sql = 'select feature_name, item_id_list from %s_feature_recommend_list where feature_name in (%s)' % (resource_type, sql_list_to_str(feature_name_list))
        sql_list.append(sql)
    return sql_multi_query_to_dct(sql_list)
         
def get_db_offline_feature_hot_item_list_all(resource_type_list):
    sql_list = []
    for resource_type in resource_type_list:
        sql = 'select feature_name, item_id_list from %s_feature_recommend_list' % resource_type
        sql_list.append(sql)
    return sql_multi_query_to_dct(sql_list)
         
# global hot feature list
# return: (errorCode, {resource_type: data, ...})
def get_db_offline_global_hot_feature_list(resource_type_list):
    sql = "select resource_type, item_feature_list from resource_hot_feature_list where resource_type in (%s)" % sql_list_to_str(resource_type_list) 
    return sql_query_to_dct(sql)
         
def get_db_offline_global_hot_feature_list_all():
    sql = "select resource_type, item_feature_list from resource_hot_feature_list"
    return sql_query_to_dct(sql)
         
# global hot feature list
# global hot feature list
# return: (errorCode, {resource_type: data, ...})
#def get_db_offline_item_id_new_to_old_resource_single(resource_type, new_item_id_list):
#    sql = 'select new_item_id, old_item_id from %s_item_id_new_to_old where new_item_id in (%s)' % (resource_type, sql_list_to_str(new_item_id_list))
#    return sql_query_to_dct(sql)

# return: (errorCode, {resource_type: data, ...})
def get_db_offline_item_id_new_to_old(new_item_id_list):
    resource_itemid_dct = split_itemid_list_to_resource_dct(new_item_id_list)
    errorCode = True
    result = {}
    sql_list = []
    for resource_type ,itemid_list in resource_itemid_dct.items():
        sql = 'select new_item_id, old_item_id from %s_item_id_new_to_old where new_item_id in (%s)' % (resource_type, sql_list_to_str(new_item_id_list))
        sql_list.append(sql)
    return sql_multi_query_to_dct(sql_list)

def get_db_offline_item_id_new_to_old_all(resource_type_list):
    sql_list = []
    for resource_type in resource_type_list:
        sql = 'select new_item_id, old_item_id from %s_item_id_new_to_old' % resource_type
        sql_list.append(sql)
    return sql_multi_query_to_dct(sql_list)
