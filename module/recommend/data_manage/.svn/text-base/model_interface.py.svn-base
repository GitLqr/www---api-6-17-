#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-16
import sys
sys.path.append('.')

import os
import logging
#import log_conf
import cache_models
import db_models
from data_def import DataDef
from db_cache_conf import DB_CACHE_CONF, DefaultConf
import copy

#logger = logging.getLogger('alinow_data_manage.models')
logger = logging.getLogger('recommend.data_manage')

def db_cache_init(db_conf = DefaultConf.db_conf, cache_conf = DefaultConf.cache_conf):
    DB_CACHE_CONF.DATABASE_CONF = db_conf
    DB_CACHE_CONF.REDIS_PY_CONF = cache_conf
    return True

def get_return_none_keys(res, key_list):
    return_none_keys = []
    for key in key_list:
        if not res.has_key(key):
            return_none_keys.append(key)
    return return_none_keys

def merge_db_cache_result(cache_res, db_res):
    res = {}
    for key, value in cache_res.items():
        if DataDef.CACHE_DEFAULT_NONE_VALUE == value:
            continue
        res[key] = value
    for key, value in db_res.items():
        res[key] = value
    return res

# user resouce visitinfo
# return: (errorCode, {resource_type: data, ...})
def get_online_user_resource_visitinfo(uid, resource_type_list):
    return cache_models.get_cache_online_user_resource_visitinfo(uid, resource_type_list)

# return: (errorCode, {resource_type: data, ...})
def get_offline_user_resource_visitinfo(uid, resource_type_list):
    cache_errorCode, cache_res = cache_models.get_cache_offline_user_resource_visitinfo(uid, resource_type_list)
    return_none_keys = get_return_none_keys(cache_res, resource_type_list)
    db_errorCode = True
    db_res = {}
    if len(return_none_keys) > 0:
        logger.warning('get_offline_user_resource_visitinfo, cache has return none key: %s' % return_none_keys)
        db_errorCode, db_res = db_models.get_db_offline_user_resource_visitinfo(uid, return_none_keys)
        #logger.debug('db_Code: %s, db_res:%s' % (db_errorCode, db_res))
        for resource_type , visitinfo_data in db_res.items():
            cache_models.set_cache_offline_user_resource_visitinfo(uid, resource_type, visitinfo_data)
            logger.debug('get_offline_user_resource_visitinfo, set cache uid[%s], resource_type[%s]' % (uid, resource_type))
        if True == db_errorCode:
            for resource_type in [x for x in return_none_keys if x not in db_res.keys()]:
                cache_models.set_cache_offline_user_resource_visitinfo(uid, resource_type, DataDef.CACHE_DEFAULT_NONE_VALUE, DataDef.CACHE_NONE_EXPIRE_SECONDS)
                logger.debug('get_offline_user_resource_visitinfo, set cache uid[%s] resource_type[%s] None Value' % (uid, resource_type))
    return (cache_errorCode and db_errorCode, merge_db_cache_result(cache_res, db_res))

def set_online_user_resource_visitinfo(uid, resource_type, visitinfo_data):
    return cache_models.set_cache_online_user_resource_visitinfo(uid, resource_type, visitinfo_data)

# user feature list
# return: (errorCode, {resource_type: data, ...})
def get_online_user_feature_list(uid, resource_type_list):
    return cache_models.get_cache_online_user_feature_list(uid, resource_type_list)

# return: (errorCode, {resource_type: data, ...})
def get_offline_user_feature_list(uid, resource_type_list):
    cache_errorCode, cache_res = cache_models.get_cache_offline_user_feature_list(uid, resource_type_list)
    return_none_keys = get_return_none_keys(cache_res, resource_type_list)
    db_errorCode = True
    db_res = {}
    if len(return_none_keys) > 0:
        logger.warning('get_offline_user_feature_list, cache has return none key: %s' % return_none_keys)
        db_errorCode, db_res = db_models.get_db_offline_user_feature_list(uid, return_none_keys)
        #logger.debug('db_Code: %s, db_res:%s' % (db_errorCode, db_res))
        for resource_type , features_data in db_res.items():
            cache_models.set_cache_offline_user_feature_list(uid, resource_type, features_data)
            logger.debug('get_offline_user_feature_list, set cache uid[%s], resource_type[%s]' % (uid, resource_type))
        if True == db_errorCode:
            for resource_type in [x for x in return_none_keys if x not in db_res.keys()]:
                cache_models.set_cache_offline_user_feature_list(uid, resource_type, DataDef.CACHE_DEFAULT_NONE_VALUE, DataDef.CACHE_NONE_EXPIRE_SECONDS)
                logger.debug('get_offline_user_feature_list, set cache uid[%s] resource_type[%s] None Value' % (uid, resource_type))
    return (cache_errorCode and db_errorCode, merge_db_cache_result(cache_res, db_res))

def set_online_user_feature_list(uid, resource_type, user_feature_list_data):
    return cache_models.set_cache_online_user_feature_list(uid, resource_type, user_feature_list_data)

# user feature reason
# return: (errorCode, data)
def get_online_user_feature_reason(uid):
    return cache_models.get_cache_online_user_feature_reason(uid)

def set_online_user_feature_reason(uid, item_feature_list_data):
    return cache_models.set_cache_online_user_feature_reason(uid, item_feature_list_data)

# user favor itemlist
# return: (errorCode, {resource_type: data, ...})
def get_online_user_favor_item_list(uid, resource_type_list):
    return cache_models.get_cache_online_user_favor_item_list(uid, resource_type_list)

def set_online_user_favor_item_list(uid, resource_type, item_id_list_data):
    return cache_models.set_cache_online_user_favor_item_list(uid, resource_type, item_id_list_data)

# user recommend itemlist
# return: (errorCode, {resource_type: data, ...})
def get_offline_user_recommend_item_list(uid, resource_type_list):
    cache_errorCode, cache_res = cache_models.get_cache_offline_user_recommend_item_list(uid, resource_type_list)
    return_none_keys = get_return_none_keys(cache_res, resource_type_list)
    db_errorCode = True
    db_res = {}
    if len(return_none_keys) > 0:
        logger.warning('get_offline_user_recommend_item_list, cache has return none key: %s' % return_none_keys)
        db_errorCode, db_res = db_models.get_db_offline_user_recommend_item_list(uid, return_none_keys)
        #logger.debug('db_Code: %s, db_res:%s' % (db_errorCode, db_res))
        for key , data in db_res.items():
            cache_models.set_cache_offline_user_recommend_item_list(uid, key, data)
            logger.debug('get_offline_user_feature_list, set cache uid[%s], resource_type[%s]' % (uid, key))
        if True == db_errorCode:
            for key in [x for x in return_none_keys if x not in db_res.keys()]:
                cache_models.set_cache_offline_user_recommend_item_list(uid, key, DataDef.CACHE_DEFAULT_NONE_VALUE, DataDef.CACHE_NONE_EXPIRE_SECONDS)
                logger.debug('get_offline_user_feature_list, set cache uid[%s] resource_type[%s] None Value' % (uid, key))
    return (cache_errorCode and db_errorCode, merge_db_cache_result(cache_res, db_res))

# user push itemlist
# return: (errorCode, data)
def get_online_user_push_item_list(uid):
    return cache_models.get_cache_online_user_push_item_list(uid)

def set_online_user_push_item_list(uid, item_id_list_data):
    return cache_models.set_cache_online_user_push_item_list(uid, item_id_list_data)

# item recommend item list
# return: (errorCode, {item_id: data, ...})
def get_offline_item_recommend_item_list(itemid_list):
    cache_errorCode, cache_res = cache_models.get_cache_offline_item_recommend_item_list(itemid_list)
    return_none_keys = get_return_none_keys(cache_res, itemid_list)
    db_errorCode = True
    db_res = {}
    if len(return_none_keys) > 0:
        logger.warning('get_offline_item_recommend_item_list, cache has return none key: %s' % return_none_keys)
        db_errorCode, db_res = db_models.get_db_offline_item_recommend_item_list(return_none_keys)
        #logger.debug('db_Code: %s, db_res:%s' % (db_errorCode, db_res))
        for key , data in db_res.items():
            cache_models.set_cache_offline_item_recommend_item_list(key, data)
            logger.debug('get_offline_item_recommend_item_list, set cache item_id[%s]' % key)
        if True == db_errorCode:
            for key in [x for x in return_none_keys if x not in db_res.keys()]:
                cache_models.set_cache_offline_item_recommend_item_list(key, DataDef.CACHE_DEFAULT_NONE_VALUE, DataDef.CACHE_NONE_EXPIRE_SECONDS)
                logger.debug('get_offline_item_recommend_item_list, set cache item_id[%s] None Value' % key)
    return (cache_errorCode and db_errorCode, merge_db_cache_result(cache_res, db_res))

# item features
# return: (errorCode, {item_id: data, ...})
def get_offline_item_features(itemid_list):
    cache_errorCode, cache_res = cache_models.get_cache_offline_item_features(itemid_list)
    return_none_keys = get_return_none_keys(cache_res, itemid_list)
    db_errorCode = True
    db_res = {}
    if len(return_none_keys) > 0:
        logger.warning('get_offline_item_features, cache has return none key: %s' % return_none_keys)
        db_errorCode, db_res = db_models.get_db_offline_item_features(return_none_keys)
        #logger.debug('db_Code: %s, db_res:%s' % (db_errorCode, db_res))
        for key , data in db_res.items():
            cache_models.set_cache_offline_item_features(key, data)
            logger.debug('get_offline_item_features, set cache item_id[%s]' % key)
        if True == db_errorCode:
            for key in [x for x in return_none_keys if x not in db_res.keys()]:
                cache_models.set_cache_offline_item_features(key, DataDef.CACHE_DEFAULT_NONE_VALUE, DataDef.CACHE_NONE_EXPIRE_SECONDS)
                logger.debug('get_offline_item_features, set cache item_id[%s] None Value' % key)
    return (cache_errorCode and db_errorCode, merge_db_cache_result(cache_res, db_res))

# feature hot item list
# return: (errorCode, {feature_names: data, ...})
def get_offline_feature_hot_item_list(feature_names):
    #logger.debug('get_offline_feature_hot_item_list, feature_names: %s' % feature_names)
    cache_errorCode, cache_res = cache_models.get_cache_offline_feature_hot_item_list(feature_names)
    return_none_keys = get_return_none_keys(cache_res, feature_names)
    db_errorCode = True
    db_res = {}
    if len(return_none_keys) > 0:
        logger.warning('get_offline_feature_hot_item_list, cache has return none key: %s' % return_none_keys)
        db_errorCode, db_res = db_models.get_db_offline_feature_hot_item_list(return_none_keys)
        #logger.debug('db_Code: %s, db_res:%s' % (db_errorCode, db_res))
        for key , data in db_res.items():
            cache_models.set_cache_offline_feature_hot_item_list(key, data)
            logger.debug('get_offline_feature_hot_item_list, set cache feature_names[%s]' % key)
        if True == db_errorCode:
            for key in [x for x in return_none_keys if x not in db_res.keys()]:
                cache_models.set_cache_offline_feature_hot_item_list(key, DataDef.CACHE_DEFAULT_NONE_VALUE, DataDef.CACHE_NONE_EXPIRE_SECONDS)
                logger.debug('get_offline_feature_hot_item_list, set cache item_id[%s] None Value' % key)
    return (cache_errorCode and db_errorCode, merge_db_cache_result(cache_res, db_res))

# global hot feature list
# return: (errorCode, {resource_type: data, ...})
def get_offline_global_hot_feature_list(resource_type_list):
    cache_errorCode, cache_res = cache_models.get_cache_offline_global_hot_feature_list(resource_type_list)
    return_none_keys = get_return_none_keys(cache_res, resource_type_list)
    db_errorCode = True
    db_res = {}
    if len(return_none_keys) > 0:
        logger.warning('get_offline_global_hot_feature_list, cache has return none key: %s' % return_none_keys)
        db_errorCode, db_res = db_models.get_db_offline_global_hot_feature_list(return_none_keys)
        #logger.debug('db_Code: %s, db_res:%s' % (db_errorCode, db_res))
        for key , data in db_res.items():
            cache_models.set_cache_offline_global_hot_feature_list(key, data)
            logger.debug('get_offline_global_hot_feature_list, set cache resource_type[%s]' % key)
        if True == db_errorCode:
            for key in [x for x in return_none_keys if x not in db_res.keys()]:
                cache_models.set_cache_offline_global_hot_feature_list(key, DataDef.CACHE_DEFAULT_NONE_VALUE, DataDef.CACHE_NONE_EXPIRE_SECONDS)
                logger.debug('get_offline_global_hot_feature_list, set cache resource_type[%s] None Value' % key)
    return (cache_errorCode and db_errorCode, merge_db_cache_result(cache_res, db_res))

# item new id to old id
# return: (errorCode, {new_item_id: old_item_id, ...})
def get_offline_item_id_new_to_old(new_item_id_list):
    cache_errorCode, cache_res = cache_models.get_cache_offline_item_id_new_to_old(new_item_id_list)
    return_none_keys = get_return_none_keys(cache_res, new_item_id_list)
    db_errorCode = True
    db_res = {}
    if len(return_none_keys) > 0:
        logger.warning('get_offline_item_id_new_to_old, cache has return none key: %s' % return_none_keys)
        db_errorCode, db_res = db_models.get_db_offline_item_id_new_to_old(return_none_keys)
        #logger.debug('db_Code: %s, db_res:%s' % (db_errorCode, db_res))
        for key , data in db_res.items():
            cache_models.set_cache_offline_item_id_new_to_old(key, data)
            logger.debug('get_offline_item_id_new_to_old, set cache new_item_id[%s]' % key)
        if True == db_errorCode:
            for key in [x for x in return_none_keys if x not in db_res.keys()]:
                cache_models.set_cache_offline_item_id_new_to_old(key, DataDef.CACHE_DEFAULT_NONE_VALUE, DataDef.CACHE_NONE_EXPIRE_SECONDS)
                logger.debug('get_offline_item_id_new_to_old, set cache new_item_id[%s] None Value' % key)
    return (cache_errorCode and db_errorCode, merge_db_cache_result(cache_res, db_res))
