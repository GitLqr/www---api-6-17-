#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-16
import sys
sys.path.append('.')

import os
import logging
#import log_conf
import model_connect
import db_models
from data_def import DataDef

#logger = logging.getLogger('alinow_data_manage.models')
logger = logging.getLogger('recommend.data_manage')

# cache clear keys which has prefix redis_index
# return True or False
def cache_clear_prefix_index(redis_index):
    redis_py = model_connect.get_redis_py()
    if None == redis_py:
        logger.error('get redis py connect failed.')
        return False
    #print 'key_pattern: %s' % key_pattern
    try:
        del_keys = redis_py.keys(redis_index + '_*')
        pipe = redis_py.pipeline()
        logger.debug('del_keys: %s' % del_keys)
        for key in del_keys:
            logger.debug('cache delete key : %s' % key)
            pipe.delete(key)
        res = pipe.execute()
        if False == res:
            logger.error('cache batch delete data, pipeline execute failed.')
            return False
        logger.debug('cache batch delete data, pipeline execute success.')
        return True
    except:
        logger.error('cache_clear_prefix_index failed. error: %s' % str(sys.exc_info()))
        return False

def cache_clear_key(key):
    logger.debug('cache delete key: %s' % key)
    redis_py = model_connect.get_redis_py()
    if None == redis_py:
        logger.error('get redis py connect failed.')
        return False
    try:
        redis_py.delete(key)
        logger.debug('cache delete data, redis delete success.')
        return True
    except:
        logger.error('cache_clear_prefix_index failed. error: %s' % str(sys.exc_info()))
        return False



def cache_update_batch(kv_dct):
    redis_py = model_connect.get_redis_py()
    if None == redis_py:
        logger.error('get redis py connect failed.')
        return False
    try:
        pipe = redis_py.pipeline()
        for k,v in kv_dct.items():
            if k != k.strip():
                logger.warning('key with illegal character space. key:%s' % k)
            pipe.set(k.strip(), v)
        res = pipe.execute()
        logger.debug('cache batch set data, pipeline execute success.')
        return True
    except:
        logger.error('cache_update_batch. error: %s' % str(sys.exc_info()))
        return False

def cache_clear_update_batch(redis_index, kv_dct):
    redis_py = model_connect.get_redis_py()
    if None == redis_py:
        logger.error('get redis py connect failed.')
        return False
    try:
        del_keys = redis_py.keys(redis_index + '_*')
        pipe = redis_py.pipeline()
        for key in del_keys:
            logger.debug('cache delete key : %s' % key)
            pipe.delete(key)
        for k,v in kv_dct.items():
            #logger.debug('set cache key: %s, value: %s' % (k, v))
            logger.debug('set cache key: %s' % k)
            if k != k.strip():
                logger.warning('key with illegal character space. key:%s' % k)
            pipe.set(k.strip(), v)
        res = pipe.execute()
        logger.debug('cache clear update batch, pipeline execute success.')
        return True
    except:
        logger.error('cache_clear_update_batch failed. error: %s' % str(sys.exc_info()))
        return False

def cache_clear_update_all(update_dct_list):
    redis_py = model_connect.get_redis_py()
    if None == redis_py:
        logger.error('get redis py connect failed.')
        return False
    try:
        pipe = redis_py.pipeline()
        for (redis_index, kv_dct) in update_dct_list:
            del_keys = redis_py.keys(redis_index + '_*')
            for key in del_keys:
                logger.debug('cache delete key : %s' % key)
                pipe.delete(key)
            for k,v in kv_dct.items():
                #logger.debug('set cache key: %s, value: %s' % (k, v))
                logger.debug('set cache key: %s ' % k)
                if k != k.strip():
                    logger.warning('key with illegal character space. key:%s' % k)
                pipe.set(k.strip(), v)
        res = pipe.execute()
        logger.debug('cache_clear_update_all, pipeline execute success.')
        return True
    except:
        logger.error('cache_clear_update_all failed. error: %s' % str(sys.exc_info()))
        return False

def cache_clear_online_by_user(uid):
    # clear online user_resource_visitinfo
    redis_index = DataDef.ONLINE_USER_RESOURCE_VISIT_INFO_INDEX
    if False == cache_clear_prefix_index(redis_index + '_' + uid):
        return False
    # clear online user_feature_list
    redis_index = DataDef.ONLINE_USER_FEATURE_LIST_INDEX
    if False == cache_clear_prefix_index(redis_index + '_' + uid):
        return False
    # clear online user_feature_reason 
    redis_index = DataDef.ONLINE_USER_FEATURE_REASON_INDEX
    if False == cache_clear_key(redis_index + '_' + uid):
        return False
    # clear online user_favor_item_list
    redis_index = DataDef.ONLINE_USER_FAVOR_ITEM_LIST_INDEX
    if False == cache_clear_prefix_index(redis_index + '_' + uid):
        return False
    # clear online user_push_item_list
    redis_index = DataDef.ONLINE_USER_PUSH_ITEM_LIST_INDEX
    if False == cache_clear_key(redis_index + '_' + uid):
        return False
    return True

def cache_clear_online_user_resource_visitinfo():
    return cache_clear_prefix_index(DataDef.ONLINE_USER_RESOURCE_VISIT_INFO_INDEX)

# return False or True
def db_get_update_data_offline_user_resource_visitinfo(resource_type_list):
    flag = True
    kv_dct = {}
    redis_index = DataDef.OFFLINE_USER_RESOURCE_VISIT_INFO_INDEX
    for resource_type in resource_type_list:
        errorCode, uid_visitinfo_dct = db_models.get_db_offline_user_resource_visitinfo_all(resource_type)
        if False == errorCode:
            logger.error('get db offline user resource visitinfo all failed. resource_type: %s' % resource_type)
            flag = False
            continue
        for uid, visitinfo_data in uid_visitinfo_dct.items():
            kv_dct[redis_index + '_' + uid + '_' + resource_type] = visitinfo_data
    return (flag, redis_index, kv_dct)

def cache_update_offline_user_resource_visitinfo(resource_type_list):
    #logger.debug('cache_update_offline_user_resource_visitinfo, kv_dct: %s' % kv_dct)
    #res = cache_update_batch(kv_dct)
    flag, redis_index, kv_dct = db_get_update_data_offline_user_resource_visitinfo(resource_type_list)
    res = cache_clear_update_batch(redis_index, kv_dct)
    return flag and res

def cache_clear_online_user_feature_list():
    return cache_clear_prefix_index(DataDef.ONLINE_USER_FEATURE_LIST_INDEX)

def db_get_update_data_offline_user_feature_list(resource_type_list):
    flag = True
    kv_dct = {}
    redis_index = DataDef.OFFLINE_USER_FEATURE_LIST_INDEX
    for resource_type in resource_type_list:
        errorCode, uid_features_dct = db_models.get_db_offline_user_feature_list_all(resource_type)
        if False == errorCode:
            logger.error('get db offline user feature list all failed. resource_type:%s' % resource_type)
            flag = False
            continue
        for uid, features_data in uid_features_dct.items():
            kv_dct[redis_index + '_' + uid + '_' + resource_type] = features_data
    return (flag, redis_index, kv_dct)

def cache_update_offline_user_feature_list(resource_type_list):
    flag, redis_index, kv_dct = db_get_update_data_offline_user_feature_list(resource_type_list)
    res = cache_clear_update_batch(redis_index, kv_dct)
    return flag and res

def cache_clear_online_user_feature_reason():
    return cache_clear_prefix_index(DataDef.ONLINE_USER_FEATURE_REASON_INDEX)

def cache_clear_online_user_favor_item_list():
    return cache_clear_prefix_index(DataDef.ONLINE_USER_FAVOR_ITEM_LIST_INDEX)

def db_get_update_data_offline_user_recommend_item_list(resource_type_list):
    flag = True
    kv_dct = {}
    redis_index = DataDef.OFFLINE_USER_RECOMMEND_ITEM_LIST_INDEX
    for resource_type in resource_type_list:
        errorCode, uid_data_dct = db_models.get_db_offline_user_recommend_item_list_all(resource_type)
        flag = flag and errorCode
        if False == errorCode:
            logger.error('get db offline user recommend item list all failed.')
            continue
        for uid, data in uid_data_dct.items():
            kv_dct[redis_index + '_' + uid + '_' + resource_type] = data
    return (flag, redis_index, kv_dct)

def cache_update_offline_user_recommend_item_list(resource_type_list):
    flag, redis_index, kv_dct = db_get_update_data_offline_user_recommend_item_list(resource_type_list)
    res = cache_clear_update_batch(redis_index, kv_dct)
    return flag and res

def cache_clear_online_user_push_item_list():
    return cache_clear_prefix_index(DataDef.ONLINE_USER_PUSH_ITEM_LIST_INDEX)

def db_get_update_data_offline_item_recommend_item_list(resource_type_list):
    redis_index = DataDef.OFFLINE_ITEM_RECOMMEND_ITEM_LIST_INDEX
    errorCode, itemid_data_dct = db_models.get_db_offline_item_recommend_item_list_all(resource_type_list)
    if False == errorCode:
        logger.error('get db offline item recommend item list all failed.')
        return (False, redis_index, {})
    kv_dct = {}
    for itemid, data in itemid_data_dct.items():
        kv_dct[redis_index + '_' + itemid ] = data
    return (True, redis_index, kv_dct)

def cache_update_offline_item_recommend_item_list(resource_type_list):
    #res = cache_update_batch(kv_dct)
    flag, redis_index, kv_dct = db_get_update_data_offline_item_recommend_item_list(resource_type_list)
    res = cache_clear_update_batch(redis_index, kv_dct)
    return flag and res

def db_get_update_data_offline_item_features(resource_type_list):
    redis_index = DataDef.OFFLINE_ITEM_FEATURES_INDEX
    kv_dct = {}
    errorCode, itemid_data_dct = db_models.get_db_offline_item_features_all(resource_type_list)
    flag =  errorCode
    if False == errorCode:
        logger.error('get db offline item recommend item list all failed.')
        return (False, redis_index, kv_dct)
    for itemid, data in itemid_data_dct.items():
        kv_dct[redis_index + '_' + itemid] = data
    return (True, redis_index, kv_dct)

def cache_update_offline_item_features(resource_type_list):
    #res = cache_update_batch(kv_dct)
    flag, redis_index, kv_dct = db_get_update_data_offline_item_features(resource_type_list)
    res = cache_clear_update_batch(redis_index, kv_dct)
    return flag and res

def db_get_update_data_offline_feature_hot_item_list(resource_type_list):
    redis_index = DataDef.OFFLINE_FEATURE_HOT_ITEM_LIST_INDEX
    kv_dct = {}
    errorCode, feature_data_dct = db_models.get_db_offline_feature_hot_item_list_all(resource_type_list)
    if False == errorCode:
        logger.error('get db offline item recommend item list all failed.')
        return (False, redis_index, kv_dct)
    for feature, data in feature_data_dct.items():
        kv_dct[redis_index + '_' + feature] = data
    return (True, redis_index, kv_dct)

def cache_update_offline_feature_hot_item_list(resource_type_list):
    flag, redis_index, kv_dct = db_get_update_data_offline_feature_hot_item_list(resource_type_list)
    res = cache_clear_update_batch(redis_index, kv_dct)
    return flag and res

def db_get_update_data_offline_global_hot_feature_list():
    redis_index = DataDef.OFFLINE_GLOBAL_HOT_FEATURE_LIST_INDEX
    kv_dct = {}
    errorCode, resource_data_dct = db_models.get_db_offline_global_hot_feature_list_all()
    if False == errorCode:
        logger.error('get db offline item recommend item list all failed.')
        return (False, redis_index, kv_dct)
    for resource, data in resource_data_dct.items():
        kv_dct[redis_index + '_' + resource] = data
    return (True, redis_index, kv_dct)

def cache_update_offline_global_hot_feature_list():
    #res = cache_update_batch(kv_dct)
    flag, redis_index, kv_dct = db_get_update_data_offline_global_hot_feature_list()
    res = cache_clear_update_batch(redis_index, kv_dct)
    return flag and res

def db_get_update_data_offline_item_id_new_to_old(resource_type_list):
    redis_index = DataDef.OFFLINE_ITEM_ID_NEW_TO_OLD_INDEX
    kv_dct = {}
    errorCode, itemid_data_dct = db_models.get_db_offline_item_id_new_to_old_all(resource_type_list)
    if False == errorCode:
        logger.error('get db offline item id new to old all failed.')
        return (False, redis_index, kv_dct)
    for itemid, data in itemid_data_dct.items():
        kv_dct[redis_index + '_' + itemid] = data
    return (True, redis_index, kv_dct)

def cache_update_offline_item_id_new_to_old(resource_type_list):
    flag, redis_index, kv_dct = db_get_update_data_offline_item_id_new_to_old(resource_type_list)
    res = cache_clear_update_batch(redis_index, kv_dct)
    return flag and res

def cache_update_all_together(all_resource_type_list, common_resource_type_list):
    update_dct_list = []
    # add online user resource visitinfo
    update_dct_list.append((DataDef.ONLINE_USER_RESOURCE_VISIT_INFO_INDEX, {}))
    # add offline user resource visitinfo
    flag, redis_index, kv_dct = db_get_update_data_offline_user_resource_visitinfo(all_resource_type_list)
    if False == flag:
        logger.error('cache_update_all_together, db_get_update_data_offline_user_resource_visitinfo failed.')
        return False
    update_dct_list.append((redis_index, kv_dct))
    # add online user feature list
    update_dct_list.append((DataDef.ONLINE_USER_FEATURE_LIST_INDEX, {}))
    # add offline user feature list 
    flag, redis_index, kv_dct = db_get_update_data_offline_user_feature_list(all_resource_type_list)
    if False == flag:
        logger.error('cache_update_all_together, db_get_update_data_offline_user_feature_list failed.')
        return False
    update_dct_list.append((redis_index, kv_dct))
    # add online user feature reason
    update_dct_list.append((DataDef.ONLINE_USER_FEATURE_REASON_INDEX, {}))
    # add online user favor item list
    update_dct_list.append((DataDef.ONLINE_USER_FAVOR_ITEM_LIST_INDEX, {}))
    # add offline user recommend item list
    flag, redis_index, kv_dct = db_get_update_data_offline_user_recommend_item_list(common_resource_type_list)
    if False == flag:
        logger.error('cache_update_all_together, db_get_update_data_offline_user_recommend_item_list failed.')
        return False
    update_dct_list.append((redis_index, kv_dct))
    # add offline item_recommend_item_list
    flag, redis_index, kv_dct = db_get_update_data_offline_item_recommend_item_list(common_resource_type_list)
    if False == flag:
        logger.error('cache_update_all_together, db_get_update_data_offline_item_recommend_item_list failed.')
        return False
    update_dct_list.append((redis_index, kv_dct))
    # add offline item_features
    flag, redis_index, kv_dct = db_get_update_data_offline_item_features(common_resource_type_list)
    if False == flag:
        logger.error('cache_update_all_together, db_get_update_data_offline_item_features failed.')
        return False
    update_dct_list.append((redis_index, kv_dct))
    # add offline item_recommend_item_list
    flag, redis_index, kv_dct = db_get_update_data_offline_feature_hot_item_list(common_resource_type_list)
    if False == flag:
        logger.error('cache_update_all_together, db_get_update_data_offline_feature_hot_item_list failed.')
        return False
    update_dct_list.append((redis_index, kv_dct))
    # add offline global_hot_feature_list
    flag, redis_index, kv_dct = db_get_update_data_offline_global_hot_feature_list()
    if False == flag:
        logger.error('cache_update_all_together, db_get_update_data_offline_global_hot_feature_list failed.')
        return False
    update_dct_list.append((redis_index, kv_dct))
    # add offline item_id_new_to_old
    flag, redis_index, kv_dct = db_get_update_data_offline_item_id_new_to_old(common_resource_type_list)
    if False == flag:
        logger.error('cache_update_all_together, db_get_update_data_offline_item_id_new_to_old failed.')
        return False
    update_dct_list.append((redis_index, kv_dct))
    return cache_clear_update_all(update_dct_list) 

def do_cache_update():
    all_resource_type_list = ['movi', 'news']
    common_resource_type_list = ['movi']
    if False == cache_clear_online_user_resource_visitinfo():
        logger.error('cache_clear_online_user_resource_visitinfo failed.')
    if False == cache_update_offline_user_resource_visitinfo(all_resource_type_list):
        logger.error('cache_update_offline_user_resource_visitinfo failed.')
    if False == cache_clear_online_user_feature_list():
        logger.error('cache_clear_online_user_feature_list failed.')
    if False == cache_update_offline_user_feature_list(all_resource_type_list):
        logger.error('cache_update_offline_user_feature_list failed.')
    if False == cache_clear_online_user_feature_reason():
        logger.error('cache_clear_online_user_feature_reason failed.')
    if False == cache_clear_online_user_favor_item_list():
        logger.error('cache_clear_online_user_favor_item_list failed.')
    if False == cache_update_offline_user_recommend_item_list(common_resource_type_list):
        logger.error('cache_update_offline_user_recommend_item_list failed.')
    if False == cache_clear_online_user_push_item_list():
        logger.error('cache_clear_online_user_push_item_list failed.')
    if False == cache_update_offline_item_recommend_item_list(common_resource_type_list):
        logger.error('cache_update_offline_item_recommend_item_list failed.')
    if False == cache_update_offline_item_features(common_resource_type_list):
        logger.error('cache_update_offline_item_features failed.')
    if False == cache_update_offline_feature_hot_item_list(common_resource_type_list):
        logger.error('cache_update_offline_feature_hot_item_list failed.')
    if False == cache_update_offline_global_hot_feature_list():
        logger.error('cache_update_offline_global_hot_feature_list failed.')
    if False == cache_update_offline_item_id_new_to_old(common_resource_type_list):
        logger.error('cache_update_offline_item_id_new_to_old failed.')

def clear_online_cache():
    if False == cache_clear_online_user_resource_visitinfo():
        logger.error('cache_clear_online_user_resource_visitinfo failed.')
    if False == cache_clear_online_user_feature_list():
        logger.error('cache_clear_online_user_feature_list failed.')
    if False == cache_clear_online_user_feature_reason():
        logger.error('cache_clear_online_user_feature_reason failed.')
    if False == cache_clear_online_user_favor_item_list():
        logger.error('cache_clear_online_user_favor_item_list failed.')
    if False == cache_clear_online_user_push_item_list():
        logger.error('cache_clear_online_user_push_item_list failed.')

def clear_all_cache():
    cache_prefix = DataDef.ONLINE_USER_RESOURCE_VISIT_INFO_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.OFFLINE_USER_RESOURCE_VISIT_INFO_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.ONLINE_USER_FEATURE_LIST_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.OFFLINE_USER_FEATURE_LIST_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.ONLINE_USER_FEATURE_REASON_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.ONLINE_USER_FAVOR_ITEM_LIST_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.OFFLINE_USER_RECOMMEND_ITEM_LIST_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.ONLINE_USER_PUSH_ITEM_LIST_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.OFFLINE_ITEM_RECOMMEND_ITEM_LIST_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.OFFLINE_ITEM_FEATURES_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.OFFLINE_FEATURE_HOT_ITEM_LIST_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.OFFLINE_GLOBAL_HOT_FEATURE_LIST_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
    cache_prefix = DataDef.OFFLINE_ITEM_ID_NEW_TO_OLD_INDEX
    if False == cache_clear_prefix_index(cache_prefix):
        logger.error('clear_all_cache failed. cache_prefix:%s' % cache_prefix)
