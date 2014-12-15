#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-16
import sys
sys.path.append('.')

import os
import logging
#import log_conf
import model_connect
from data_def import DataDef

logger = logging.getLogger('recommend.data_manage')
#logger = logging.getLogger('alinow_data_manage.models')

def cache_get_batch_data(key_prefix, index_list):
    logger.debug('do cache_get_batch_data, key_prefix: %s, index_list: %s' % (key_prefix, index_list))
    keys = []
    for index in index_list:
        key = key_prefix + '_' + index
        if isinstance(key, unicode):
            key = key.encode('utf8')
        if key != key.strip():
            logger.warning('key has Illegal character space. key:%s' % key)
        keys.append(key.strip())
    #redis = model_connect.get_redis()
    redis_py = model_connect.get_redis_py()
    if None == redis_py:
        logger.error('get redist connect error.')
        return (False, {})
    try:
        logger.debug('cache_get_batch_data, keys: %s' % keys)
        #datas = redis.MGet( keys )
        datas = redis_py.mget( keys )
        res = {}
        for i, data in enumerate(datas):
            if None != data and '' != data:
                res[index_list[i]] = data
        return (True, res)
    except:
        logger.error('cache_get_batch_data failed. error:%s' % str(sys.exc_info()))
        return (False, {})
    
def cache_get_data(key):
    #redis = model_connect.get_redis()
    redis_py = model_connect.get_redis_py()
    if None == redis_py:
        logger.error('get redist connect error.')
        return (False, None)
    #data = redis.Get(key)
    if isinstance(key, unicode):
        key = key.encode('utf8')
    if key != key.strip():
        logger.warning('key has Illegal character space. key:%s' % key)
    try:
        data = redis_py.get(key.strip())
        return (True, data)
    except:
        logger.error('cache_get_data failed. error: %s' % str(sys.exc_info()))
        return (False, None)

def cache_set_data(key_prefix, key_tail, value, expire_time = None):
    if None == value:
        logger.error('value is none. key: %s' % (key_prefix + '_' + key_tail))
        return False
    #redis = model_connect.get_redis()
    redis_py = model_connect.get_redis_py()
    if None == redis_py:
        logger.error('get redist connect error.')
        return False
    key = key_prefix + '_' + key_tail
    #if not redis.Set(key, value):
    if key != key.strip():
        logger.warning('key has Illegal character space. key:%s' % key)
        key = key.strip()
    try:
        if not redis_py.set(key, value):
            logger.error('redist set error. key: %s' % key)
            return False
        if None != expire_time and False == redis_py.expire(key, expire_time):
            return False
        return True
    except:
        logger.error('cache_set_data failed. error: %s' % str(sys.exc_info()))
        return False

# user resouce visitinfo
# return: (errorCode, {resource_type: data, ...})
def get_cache_online_user_resource_visitinfo(uid, resource_type_list):
    if len(resource_type_list) <= 0:
        logger.info('get online user resource visitinfo, resource_type_list is empty.')
        return (True, {})
    redis_index = DataDef.ONLINE_USER_RESOURCE_VISIT_INFO_INDEX
    return cache_get_batch_data(redis_index + '_' + uid, resource_type_list)

# return: (errorCode, {resource_type: data, ...})
def get_cache_offline_user_resource_visitinfo(uid, resource_type_list):
    if len(resource_type_list) <= 0:
        logger.info('get offline user resource visitinfo, resource_type_list is empty.')
        return (True, {})
    redis_index = DataDef.OFFLINE_USER_RESOURCE_VISIT_INFO_INDEX
    return cache_get_batch_data(redis_index + '_' + uid, resource_type_list)

def set_cache_online_user_resource_visitinfo(uid, resource_type, visitinfo_data, expire_time = None):
    redis_index = DataDef.ONLINE_USER_RESOURCE_VISIT_INFO_INDEX
    return cache_set_data(redis_index + '_' + uid, resource_type, visitinfo_data, expire_time)
    
def set_cache_offline_user_resource_visitinfo(uid, resource_type, visitinfo_data, expire_time = None):
    redis_index = DataDef.OFFLINE_USER_RESOURCE_VISIT_INFO_INDEX
    return cache_set_data(redis_index + '_' + uid, resource_type, visitinfo_data, expire_time)
    
# user feature list
# return: (errorCode, {resource_type: data, ...})
def get_cache_online_user_feature_list(uid, resource_type_list):
    if len(resource_type_list) <= 0:
        logger.error('get cache online user feature list, resource_type_list is empty.')
        return (True, {})
    redis_index = DataDef.ONLINE_USER_FEATURE_LIST_INDEX
    return cache_get_batch_data(redis_index + '_' + uid, resource_type_list)

# return: (errorCode, {resource_type: data, ...})
def get_cache_offline_user_feature_list(uid, resource_type_list):
    if len(resource_type_list) <= 0:
        logger.error('get cache offline user feature list, resource_type_list is empty.')
        return (True, {})
    redis_index = DataDef.OFFLINE_USER_FEATURE_LIST_INDEX
    return cache_get_batch_data(redis_index + '_' + uid, resource_type_list)

def set_cache_online_user_feature_list(uid, resource_type, user_feature_list_data, expire_time = None):
    redis_index = DataDef.ONLINE_USER_FEATURE_LIST_INDEX
    return cache_set_data(redis_index + '_' + uid, resource_type, user_feature_list_data, expire_time)

def set_cache_offline_user_feature_list(uid, resource_type, user_feature_list_data, expire_time = None):
    redis_index = DataDef.OFFLINE_USER_FEATURE_LIST_INDEX
    return cache_set_data(redis_index + '_' + uid, resource_type, user_feature_list_data, expire_time)

# user feature reason
# return: (errorCode, data)
def get_cache_online_user_feature_reason(uid):
    redis_index = DataDef.ONLINE_USER_FEATURE_REASON_INDEX
    return cache_get_data(redis_index + '_' + uid)

def set_cache_online_user_feature_reason(uid, item_feature_list_data, expire_time = None):
    redis_index = DataDef.ONLINE_USER_FEATURE_REASON_INDEX
    return cache_set_data(redis_index, uid, item_feature_list_data, expire_time)

# user favor itemlist
# return: (errorCode, {resource_type: data, ...})
def get_cache_online_user_favor_item_list(uid, resource_type_list):
    if len(resource_type_list) <= 0:
        logger.error('get cache online user favor item list, resource_type_list is empty.')
        return (True, {})
    redis_index = DataDef.ONLINE_USER_FAVOR_ITEM_LIST_INDEX
    return cache_get_batch_data(redis_index + '_' + uid, resource_type_list)

def set_cache_online_user_favor_item_list(uid, resource_type, item_id_list_data, expire_time = None):
    redis_index = DataDef.ONLINE_USER_FAVOR_ITEM_LIST_INDEX
    return cache_set_data(redis_index + '_' + uid, resource_type, item_id_list_data, expire_time)

# user recommend itemlist
# return: (errorCode, {resource_type: data, ...})
def get_cache_offline_user_recommend_item_list(uid, resource_type_list):
    if len(resource_type_list) <= 0:
        logger.error('get cache offline user recommend item list, resource_type_list is empty.')
        return (True, {})
    redis_index = DataDef.OFFLINE_USER_RECOMMEND_ITEM_LIST_INDEX
    return cache_get_batch_data(redis_index + '_' + uid, resource_type_list)

def set_cache_offline_user_recommend_item_list(uid, resource_type, feature_name_item_id_list_data, expire_time = None):
    redis_index = DataDef.OFFLINE_USER_RECOMMEND_ITEM_LIST_INDEX
    return cache_set_data(redis_index + '_' + uid, resource_type, feature_name_item_id_list_data, expire_time)

# user push itemlist
# return: (errorCode, data)
def get_cache_online_user_push_item_list(uid):
    redis_index = DataDef.ONLINE_USER_PUSH_ITEM_LIST_INDEX
    return cache_get_data(redis_index + '_' + uid)

def set_cache_online_user_push_item_list(uid, item_id_list_data, expire_time = None):
    redis_index = DataDef.ONLINE_USER_PUSH_ITEM_LIST_INDEX
    return cache_set_data(redis_index, uid, item_id_list_data, expire_time)

# item recommend item list
# return: (errorCode, {item_id: data, ...})
def get_cache_offline_item_recommend_item_list(itemid_list):
    if len(itemid_list) <= 0:
        logger.error('get cache offline item recommend item list, itemid_list is empty.')
        return (True, {})
    redis_index = DataDef.OFFLINE_ITEM_RECOMMEND_ITEM_LIST_INDEX
    return cache_get_batch_data(redis_index , itemid_list)

def set_cache_offline_item_recommend_item_list(itemid, item_id_list_data, expire_time = None):
    redis_index = DataDef.OFFLINE_ITEM_RECOMMEND_ITEM_LIST_INDEX
    return cache_set_data(redis_index , itemid, item_id_list_data, expire_time)

# item features
# return: (errorCode, {item_id: data, ...})
def get_cache_offline_item_features(itemid_list):
    if len(itemid_list) <= 0:
        logger.error('get cache offline item features, itemid_list is empty.')
        return (True, {})
    redis_index = DataDef.OFFLINE_ITEM_FEATURES_INDEX
    return cache_get_batch_data(redis_index, itemid_list)

def set_cache_offline_item_features(itemid, item_feature_list_data, expire_time = None):
    redis_index = DataDef.OFFLINE_ITEM_FEATURES_INDEX
    return cache_set_data(redis_index, itemid, item_feature_list_data, expire_time)

# feature hot item list
# return: (errorCode, {feature_names: data, ...})
def get_cache_offline_feature_hot_item_list(feature_names):
    logger.debug('get_cache_offline_feature_hot_item_list, feature_names: %s' % feature_names)
    if len(feature_names) <= 0:
        logger.error('get cache offline feature hot item list, feature names is empty.')
        return (True, {})
    redis_index = DataDef.OFFLINE_FEATURE_HOT_ITEM_LIST_INDEX
    return cache_get_batch_data(redis_index, feature_names)

def set_cache_offline_feature_hot_item_list(feature_name, item_id_list_data, expire_time = None):
    redis_index = DataDef.OFFLINE_FEATURE_HOT_ITEM_LIST_INDEX
    return cache_set_data(redis_index, feature_name, item_id_list_data, expire_time)

# global hot feature list
# return: (errorCode, {resource_type: data, ...})
def get_cache_offline_global_hot_feature_list(resource_type_list):
    if len(resource_type_list) <= 0:
        logger.error('get cache offline global hot feature list, resource_type_list is empty.')
        return (True, {})
    redis_index = DataDef.OFFLINE_GLOBAL_HOT_FEATURE_LIST_INDEX
    return cache_get_batch_data(redis_index, resource_type_list)

def set_cache_offline_global_hot_feature_list(resource_type, item_feature_list_data, expire_time = None):
    redis_index = DataDef.OFFLINE_GLOBAL_HOT_FEATURE_LIST_INDEX
    return cache_set_data(redis_index, resource_type, item_feature_list_data, expire_time)

# global hot feature list
# return: (errorCode, {resource_type: data, ...})
def get_cache_offline_item_id_new_to_old(new_item_id_list):
    if len(new_item_id_list) <= 0:
        logger.error('get cache offline item id new to old, new item id list is empty.')
        return (True, {})
    redis_index = DataDef.OFFLINE_ITEM_ID_NEW_TO_OLD_INDEX
    return cache_get_batch_data(redis_index, new_item_id_list)

def set_cache_offline_item_id_new_to_old(new_item_id, old_item_id_data, expire_time = None):
    redis_index = DataDef.OFFLINE_ITEM_ID_NEW_TO_OLD_INDEX
    return cache_set_data(redis_index, new_item_id, old_item_id_data, expire_time)
