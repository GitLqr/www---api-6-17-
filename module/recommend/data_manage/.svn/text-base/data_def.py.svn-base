#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-16

class DataDef:
    
    # for redis index
    ONLINE_USER_RESOURCE_VISIT_INFO_INDEX = 'OURV'
    OFFLINE_USER_RESOURCE_VISIT_INFO_INDEX = 'FURV'
    ONLINE_USER_FEATURE_LIST_INDEX = 'OUFL'
    OFFLINE_USER_FEATURE_LIST_INDEX = 'FUFL'
    ONLINE_USER_FEATURE_REASON_INDEX = 'OUFR'
    ONLINE_USER_FAVOR_ITEM_LIST_INDEX = 'OUFI'
    OFFLINE_USER_RECOMMEND_ITEM_LIST_INDEX = 'FURI'
    ONLINE_USER_PUSH_ITEM_LIST_INDEX = 'OUPI'
    OFFLINE_ITEM_RECOMMEND_ITEM_LIST_INDEX = 'FIRI'
    OFFLINE_ITEM_FEATURES_INDEX = 'FIFI'
    OFFLINE_FEATURE_HOT_ITEM_LIST_INDEX = 'FFHI'
    OFFLINE_GLOBAL_HOT_FEATURE_LIST_INDEX = 'FGHF'
    OFFLINE_ITEM_ID_NEW_TO_OLD_INDEX = 'FINO'

    # for resource type
    RESOURCE_TYPE_BAD_VALUE = 'no_resource_type'
    RESOURCE_TYPE_MOVIE_VALUE = 'movi'
    RESOURCE_TYPE_MOVIE_SET = set(['movi','tele','cart','show'])

    # for cache none expire time
    CACHE_DEFAULT_NONE_VALUE = 'NULL'
    CACHE_NONE_EXPIRE_SECONDS = 3 * 60 * 60

    @staticmethod
    def get_resource_type_from_item_id(item_id):
        if 4 > len(item_id):
            return DataDef.RESOURCE_TYPE_BAD_VALUE
        resource_type = item_id[0:4]
        #if resource_type in DataDef.RESOURCE_TYPE_MOVIE_SET:
        #    return DataDef.RESOURCE_TYPE_MOVIE_VALUE
        return resource_type

    @staticmethod
    def get_resource_type_from_feature_name(feature_name):
        if 4 > len(feature_name):
            return DataDef.RESOURCE_TYPE_BAD_VALUE
        resource_type = feature_name[0:4]
        #if resource_type in DataDef.RESOURCE_TYPE_MOVIE_SET:
        #    return DataDef.RESOURCE_TYPE_MOVIE_VALUE
        return resource_type
