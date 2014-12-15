#!/usr/bin/env python
# -*- coding: utf8 -*-
import logging, logging.config
import traceback
import urllib,urllib2
import sys
sys.path.append('/usr/local/lib/python/')
sys.path.append('.')
from alinow_backend_proto.common_pb2 import VisitInfo,ItemFeature,UserFeature,ItemFeatureList,UserFeatureList
from alinow_backend_proto.item_pb2 import ItemIdList,FeatureNameItemIdList
from alinow_backend_proto.news_pb2 import FeatureNameLimit,FeatureNameLimitList,NewsItemFeatureInfo,NewsItemFeatureInfoList,NewsFeatureItemList
import module.recommend.data_manage.model_interface as model
import module.recommend.recent_feature_merge.online_recom_interface as online_recom_interface

logger = logging.getLogger("recommend.online")
MAX_SAME_REASON_COUNT_PER_USER = 1000000
   
def get_reason2itemlist_dict_size(reason2itemlist):
    """ get all reason item size
    """
    size = 0
    for k,v in reason2itemlist.iteritems():
        size += len(v)
    return size

def is_valid_data(errCode, data, desc, log_item_dict):
    if not errCode:
        if not data:
            logger.warn("fail to get_%s, param:%s" % (desc, log_item_dict))
            return False
        else:
            logger.warn("failget %s, param:%s" % (desc, log_item_dict))
            return True
    else:
        if not data:
            logger.info("no %s, param:%s" % (desc, log_item_dict))
        return True

def str_smart(obj, delimeter=', '):
    #return "%s" % obj
    if isinstance(obj,dict):
        return "{%s}" % delimeter.join(["%s: %s" % (str_smart(k),str_smart(v)) for k,v in
obj.iteritems()]) 
    elif isinstance(obj,list):
        return "[%s]" % delimeter.join(["%s" % str_smart(k) for k in obj]) 
    elif isinstance(obj, set):
        return "set([%s])" % delimeter.join(["%s" % str_smart(k) for k in obj]) 
    else:
        return "%s" % obj 

def check_reason(user_info, feature_name):
    if feature_name in user_info.recent_push_reason_info:
        logger.debug("empty result, ignore:%s" % feature_name)
        return False
    return True

def add_reason(user_info, reason):
    #@note: just do nothing here
    return True

def ignore_reason(user_info, reason):
    user_info.recent_push_reason_info.setdefault(reason, 0)
    user_info.recent_push_reason_info[reason] += 1

def limit_protobuf_repeated_scala_field_size(msg, field_name, final_size):
    field = getattr(msg, field_name)
    if len(field) <= final_size:
        return
    result = field[0:final_size]
    msg.ClearField(field_name)
    for i in result:
        field.append(i)
    return

