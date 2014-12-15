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
from online_data_def import ResourceType, UserInfo, LogFeedBackKey
import module.recommend.data_manage.model_interface as model
import module.recommend.recent_feature_merge.online_recom_interface as online_recom_interface
from module.recommend.request_recommend.util import is_valid_data, limit_protobuf_repeated_scala_field_size

logger = logging.getLogger("recommend.online_clicklog_feedback")

#NEWS_ONLINE_URL_GET_ITEM_FEATURES = "http://10.250.12.85/wsgi/shirong.li/online_service/get_feature_list"
NEWS_ONLINE_URL_GET_ITEM_FEATURES = "http://rss.reader.s.aliyun.com/wsgi/online_service_new/get_feature_list"
NEWS_TIMEOUT_SECONDS = 1.0

MAX_FAVOR_ITEM_LIST_COUNT_PER_PERSON = 1000

def merge_user_recent_feature(log_dict):
    """ interface for online log collector
        @note: the following key must exists in log_dict: uid, item_id, card_feature, type
        @return True|False to indicate whether the input log_dict is accepted
    """
    #@note:对于重复的点击的去重，暂时还没定处理策略
    logger.debug("begin merge_user_recent_feature")
    logger.info("log_dict:%s" % log_dict)
    if LogFeedBackKey.UID not in log_dict:
        logger.warn("uid missing")
        return False
    uid = log_dict[LogFeedBackKey.UID]
    if LogFeedBackKey.ITEM_ID not in log_dict:
        logger.warn("item_id missing")
        return False
    item_id = log_dict[LogFeedBackKey.ITEM_ID]
    if len(item_id) <= ResourceType.RESOURCE_TYPE_LENTH:
        logger.warn("invalid item_id format")
        return False
    if LogFeedBackKey.CARD_FEATURE not in log_dict:
        logger.warn("card_feature missing")
        return False
    card_feature = log_dict[LogFeedBackKey.CARD_FEATURE]
    if LogFeedBackKey.TYPE not in log_dict:
        logger.warn("type missing")
        return False
    favor_type = log_dict[LogFeedBackKey.TYPE]
    resource_type = ResourceType.get_resource_type(item_id)
    #整体策略：尽可能更新正确的信息，即时是部分也行
    #更新用户的recent feature list
    errCode1 = update_user_recent_feature_list(uid, resource_type, item_id, card_feature, favor_type)
    #更新favor item id 列表
    errCode2 = update_user_favor_item_id_list(uid, resource_type, item_id, favor_type)
    #更新user resource visit info
    errCode3 = update_user_recent_resource_visit_info(uid, resource_type, favor_type)
    return errCode1 and errCode2 and errCode3

def update_user_recent_feature_list(uid, resource_type, item_id, card_feature, favor_type):
    """ update user feature list, @return True|False
    """
    errCode, kv_dict = model.get_online_user_feature_list(uid, [resource_type])
    if not is_valid_data(errCode, kv_dict, "online_user_feature_list", {"uid":uid, "resource_type":resource_type}):
        return False
    user_feature_list = UserFeatureList()
    try:
        if kv_dict:
            assert(resource_type in kv_dict)
            user_feature_list.ParseFromString(kv_dict[resource_type])
            logger.debug("user_feature_list:%s" % user_feature_list)
    except:
        logger.error("bad get_online_user_feature_list:%s" % traceback.format_exc())
        return False
    errCode, item_feature_list_proto = get_item_features(resource_type, item_id)
    logger.debug("resource_type:%s, item_id:%s, user_feature_list:%s, item_feature_list:%s, card_feature:%s, favor_type:%s" % (
        resource_type, item_id, user_feature_list, item_feature_list_proto, card_feature, favor_type))
    if not errCode:
        logger.info("fail to get item feature list for click feedback:%s" % item_id)
        #still continue process for update by card_feature
    return raw_update_user_action(uid, resource_type, user_feature_list, item_feature_list_proto, card_feature, favor_type)

def raw_update_user_action(uid, resource_type, user_feature_list, item_feature_list_proto, card_feature, favor_type):
    print_user_feature_list = lambda result: '\n'.join(["%s:%s:%s:%s:%s" % (feature.feature_name, feature.visit_info.pv_count,
            feature.visit_info.click_count, feature.visit_info.weight,
            online_recom_interface.GetScore(feature.visit_info)) for feature in result.feature])
    print_item_feature_list = lambda result: '\n'.join(["%s" % (feature.feature_name) for feature in result.feature])
    
    logger.debug("visit item_list:%s,proto:%s" % (print_item_feature_list(item_feature_list_proto), item_feature_list_proto))
    #logger.debug("before user feature list(result):%s" % print_user_feature_list(user_feature_list))
    result = online_recom_interface.MergeFeature(user_feature_list, item_feature_list_proto, card_feature, favor_type)
#    #merge card feature for click
#    if favor_type in ["click", "like"] and card_feature:
#        existing_card_feature = False
#        for item in result.feature:
#            if item.feature_name == card_feature:
#                if favor_type == "click":
#                    item.visit_info.click_count += 1
#                else:
#                    item.visit_info.click_count += 1 #TODO:same here
#                existing_card_feature = True
#                logger.info("clickfeedback existing user feature:%s" % card_feature)
#                break
#        if not existing_card_feature:
#            logger.info("clickfeedback new user feature:%s" % card_feature)
#            item = result.feature.add()
#            item.feature_name = card_feature
#            item.visit_info.pv_count = 1
#            item.visit_info.click_count = 1
#            item.visit_info.weight = 0
#    #logger.debug("after user feature list(result):%s" % print_user_feature_list(result))
    errCode = model.set_online_user_feature_list(uid, resource_type, result.SerializeToString())
    if not errCode:
        logger.error("fail to set_online_user_feature_list,uid:%s, resource_type:%s" % (uid, resource_type))
    else:
        logger.info("successfully to set_online_user_feature_list,uid:%s, resource_type:%s" % (uid, resource_type))
    errCode_visitinfo = update_user_recent_resource_visit_info(uid, resource_type, favor_type)
    return errCode and errCode_visitinfo

def update_user_favor_item_id_list(uid, resource_type, item_id, favor_type):
    """ update user favor item id list, @return True|False
    """
    resource_type = ResourceType.get_resource_type(item_id)
    assert(resource_type)
    errCode, kv_dict = model.get_online_user_favor_item_list(uid, [resource_type])
    if not is_valid_data(errCode, kv_dict, "online_user_favor_item_list", {"uid":uid, "resource_type":resource_type}):
        return False
    logger.debug("resource_type:%s, kv_dict:%s" % (resource_type, kv_dict))
    item_id_list_proto = ItemIdList()
    try:
        if kv_dict:
            assert(resource_type in kv_dict)
            item_id_list_proto.ParseFromString(kv_dict[resource_type])
            logger.debug("favor item_id_list:%s" % item_id_list_proto)
    except:
        logger.error("bad ItemIdList from get_online_user_favor_item_list:uid:%s, resource_type:%s, exception:%s" % (uid, resource_type, traceback.format_exc()))
        return False
    item_id_list_proto.item_id.append(item_id)
    limit_protobuf_repeated_scala_field_size(item_id_list_proto, "item_id", MAX_FAVOR_ITEM_LIST_COUNT_PER_PERSON)
    logger.debug("new item_id_list:%s" % item_id_list_proto)
    errCode = model.set_online_user_favor_item_list(uid, resource_type, item_id_list_proto.SerializeToString())
    if not errCode:
        logger.warn("fail to set_online_user_favor_item_list, uid:%s, resource_type:%s" % (uid, resource_type))
    else:
        logger.info("successfully to set_online_user_favor_item_list, uid:%s, resource_type:%s" % (uid, resource_type))
    return errCode

def update_user_recent_resource_visit_info(uid, resource_type, favor_type):
    """ update user recent resource visit info, @return True|False
    """
    errCode, kv_dict = model.get_online_user_resource_visitinfo(uid, [resource_type])
    if not is_valid_data(errCode, kv_dict, "online_user_resource_visitinfo", {"uid":uid, "resource_type":resource_type}):
        return False
    logger.debug("resource_type:%s, kv_dict:%s" % (resource_type, kv_dict))
    visit_info_proto = VisitInfo()
    try:
        if kv_dict:
            assert(resource_type in kv_dict)
            visit_info_proto.ParseFromString(kv_dict[resource_type])
            logger.debug("resource_visit info,resource_type:%s,visit_info:%s" % (resource_type, visit_info_proto))
    except:
        logger.error("bad ItemIdList from get_online_user_favor_item_list:uid:%s, resource_type:%s, exception:%s" % (uid, resource_type, traceback.format_exc()))
        return False
    #TODO:define constants outside
    if favor_type in ["click", "like"]:
        logger.info("update uid:%s, click_count:%s" % (uid, visit_info_proto.click_count))
        visit_info_proto.click_count += 1
    elif favor_type == "show":
        visit_info_proto.pv_count += 1
    else:
        logger.warn("ignore unknown type:%s" % favor_type)
        return False
    errCode = model.set_online_user_resource_visitinfo(uid, resource_type, visit_info_proto.SerializeToString())
    if not errCode:
        logger.warn("fail to update_user_recent_resource_visit_info, uid:%s, resource_type:%s" % (uid, resource_type))
    else:
        logger.info("successfully to update_user_recent_resource_visit_info, uid:%s, resource_type:%s" % (uid, resource_type))
    return errCode


def get_item_features(resource_type, item_id):
    """ get item features list proto
        @return errCode, item_feature_list_proto
    """
    if ResourceType.RESOURCE_TYPE_NEWS == resource_type:
        return get_item_features_for_news(resource_type, item_id)
    else:
        return get_item_features_for_item(resource_type, item_id)

def get_item_features_for_news(resource_type, item_id):
    """ get item features list proto for news, fail if item_id not exist or other failure
        @return errCode, item_feature_list_proto
    """
    try:
        socket_out = urllib2.urlopen(NEWS_ONLINE_URL_GET_ITEM_FEATURES, item_id,
                timeout=NEWS_TIMEOUT_SECONDS)
        return_data = socket_out.read()
    except:
        logger.error("fail to talk with online news server:%s" % traceback.format_exc())
        return False, None
    try:
        output = ItemFeatureList()
        output.ParseFromString(return_data)
        if not len(output.feature):
            #fail for empty result
            return False, output
        return True, output
    except:
        logger.error("bad parse news return value:%s" % traceback.format_exc())
        return False, None

def get_item_features_for_item(resource_type, item_id):
    """ get item features list proto for item, fail if item_id not exist or other failure
        @return errCode, item_feature_list_proto
    """
    errCode, data = model.get_offline_item_features([item_id])
    if not is_valid_data(errCode, data, "offline_item_features", {"item_id":item_id}):
        return False, None
    try:
        assert(item_id in data)
        result = ItemFeatureList()
        result.ParseFromString(data[item_id])
        return True, result
    except:
        logger.error("bad get_offline_item_features:%s" % traceback.format_exc())
        return False, None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(name)s    %(filename)s +%(lineno)d    %(levelname)s   %(message)s")
    if len(sys.argv) < 2:
        print "usage:%s click(c)"
        sys.exit(1)
    import module.recommend.data_manage.model_interface as model
    db_conf = {
             'db_name': 'alinow_zhijun',
             'host': '10.250.12.84',
             'passwd': '',
             'user': 'root',
             'port': 3306,
             'charset': 'utf8'
        }
    cache_conf = {
             'host':'10.250.12.84',
             'port':6379,
        }
    model.db_cache_init(db_conf, cache_conf)

    if sys.argv[1] in [ "c", "click"]:
        for i in range(0, 1):
            errCode = merge_user_recent_feature({"uid":"uid0", "item_id":"newsaafb62a8eb52d47afe0c411c54673dfd",
                "card_feature":u"newssorc搜狐地产八卦", "type":"click"})
            errCode = merge_user_recent_feature({"uid":"uid0", "item_id":"moviw1droITejVlEmhPH",
                "card_feature":u"movibtqt搞笑", "type":"click"})
    else:
        print "usage:%s request(r)|click(c)"
        sys.exit(1)
