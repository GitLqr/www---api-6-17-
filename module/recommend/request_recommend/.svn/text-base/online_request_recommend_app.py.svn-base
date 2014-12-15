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
from online_recommend_result import RecommendItem, RecommendItemContainer
import module.recommend.data_manage.model_interface as model
import module.recommend.recent_feature_merge.online_recom_interface as online_recom_interface
from module.recommend.request_recommend.util import get_reason2itemlist_dict_size, is_valid_data, str_smart, check_reason, add_reason, ignore_reason
import online_clicklog_feedback

logger = logging.getLogger("recommend.online")

ITEM_RECOMMEND_FEATURE_TYPE = u"like"
#NEWS_ONLINE_URL_SEARCH_BY_QUERY  = "http://10.250.12.85/wsgi/shirong.li/online_service/get_article_list_by_feature"
NEWS_ONLINE_URL_SEARCH_BY_QUERY  = "http://rss.reader.s.aliyun.com/wsgi/online_service_new/get_article_list_by_feature"
NEWS_FETCH_MORE_TIMES = 30  #fetch at most NEWS_FETCH_MORE_TIMES size data
BACKUP_NEWS_FEATURE_COUNT = 1
NEWS_IGNORE_FEATURE_NAME_PREFIX = [
        u"newsctgy新闻",
        u"newsctgy本地新闻",
        u"newsname本地新闻_",
        u"newsinst本地新闻_",
        u"newsttag本地新闻_",
        u"newsngrm本地新闻_",
        ]

def get_max_recommend_item_count_per_resource(resource_type):
    if resource_type in [u"news"]:
        return 3
    return 1

def get_more_news_recommend(uid, feature_name, count):
    """ interface for more news recommend
    """
    logger.info("begin get_more_news_recommend,uid:%s,feature_name:%s,count:%s" % (uid, feature_name, count))
    try:
        if isinstance(feature_name, str):
            feature_name = unicode(feature_name, 'utf8')
        user_info = UserInfo(None, logger)
        user_info.uid = uid
        feature_name_list_proto = UserFeatureList()
        item = feature_name_list_proto.feature.add()
        item.feature_name = feature_name
        result = raw_get_news_online_item_by_feature_list(user_info, 'news', feature_name_list_proto,
            1, count, 1.2, 0)
        final_result = result.to_list(user_info)
        if not final_result:
            logger.info("get_more_news_recommend, uid:%s, expect_count:%s, real_count:%s, result:%s" % (uid,
            count, result.size(), result.get_summary_str(final_result)))
        else:
            logger.info("get_more_news_recommend, uid:%s, expect_count:%s, real_count:%s, result:%s" % (uid,
            count, len(final_result[0][1]), result.get_summary_str(final_result)))
        return (True, final_result)
    except:
        logger.error("bad exception in get_more_news_recommend, exception:%s" % traceback.format_exc())
        return (False, {})

def get_request_recommend(uid, count):
    """ interface for request recommend,return ordered reason to RecommedItem list
        @return (True|False, [(reason,[RecommendItem])])                    
    """ 
    try:
        logger.info("begin request recommend, uid:%s, count:%s" % (uid,count))
        result = RecommendItemContainer()
        logger.debug("begin get_request_recommend")
        user_info = UserInfo(uid, logger)
        #@note:new_user判断依据为是否有过点击/收藏等明确的意图行为;可以有过推送行为
        new_user = True
        for k,v in user_info.final_resource_visit_info.iteritems():
            if v.click_count != 0:
                new_user = False
                break
        if new_user:
            errCode, result = new_user_recommend(user_info, count)
            logger.info("new_user_recommend:uid:%s,status:%s,result count:%s" % (uid,errCode, result.size()))
        else:
            resource_distribution_info = get_resource_distribution_info(user_info.final_resource_visit_info, count)
            logger.info("resource_distribution_info, uid:%s, resource_distribution_info:%s" % (uid, resource_distribution_info))
            if not resource_distribution_info:
                logger.error("get resource_count error for user:%s" % uid)
                errCode, result = new_user_recommend(user_info, count)
                logger.info("new_user_recommend:uid:%s,status:%s,result count:%s" % (uid,errCode, result.size()))
            else:
                errCode, result = old_user_recommend(user_info, resource_distribution_info, count)
                logger.info("old_user_recommend:uid:%s,status:%s,result count:%s" % (uid,errCode, result.size()))
                if result.size() < count:
                    logger.debug("old_user_recommend result:%s" % result)
                    errCode, new_user_result = new_user_recommend(user_info, count - result.size())
                    logger.info("patch new_user_recommend:uid:%s,status:%s,result count:%s" % (uid,errCode, new_user_result.size()))
                    result.update(new_user_result)
        update_user_info(user_info, result)
        final_result = result.to_list(user_info)
        logger.info("request recommend result, uid:%s, expect_count:%s, real_count:%s, result:%s" % (uid,
            count, result.size(), result.get_summary_str(final_result)))
        return (True, final_result)
    except:
        logger.error("bad exception in get_request_recommend, exception:%s" % traceback.format_exc())
        return (False, {})


def new_user_recommend(user_info, count):
    """ request recommend for new user which has no favor action(点击、收藏等)
        @return (True|False, RecommendItemContainer)
    """
    logger.debug("begin new_user_recommend")
    uid = user_info.uid
    need_global_features = False
    result = RecommendItemContainer()
    if not user_info.user_feature_info:
        for resource_type in ResourceType.RESOURCE_TYPE_LIST:
            (errCode, user_feature_list) = get_user_feature_list(uid, resource_type)
            if errCode:
                if len(user_feature_list.feature):
                    user_info.user_feature_info[resource_type] = user_feature_list
                else:
                    need_global_features = True
            else:
                logger.error("fail to get user info,uid:%s" % uid)
                return (False, result)
    #TODO:may not need to get hot features again
    #TODO:may join with old_user recommend
    logger.debug("need_global_features:%s" % need_global_features)
    if need_global_features:
        logger.debug("need global features for new user recommend,uid:%s" % uid)
        resouce_feature_name_list = get_resource_hot_feature_list(user_info, count)
        if not resouce_feature_name_list:
            return (False, result)
        logger.debug("resouce_feature_name_list:%s" % resouce_feature_name_list)
        #update user feature feature
        for resource_type, feature_name_list_proto in resouce_feature_name_list.iteritems():
            if resource_type in user_info.user_feature_info and len(user_info.user_feature_info[resource_type].feature):
                continue
            user_feature_list = UserFeatureList()
            for item in feature_name_list_proto.feature:
                cur = user_feature_list.feature.add()
                cur.feature_name = item.feature_name
                cur.visit_info.pv_count = 0
                cur.visit_info.click_count = 0
                cur.visit_info.weight = item.weight
            user_info.user_feature_info[resource_type] = user_feature_list
    resouce_feature_name_list = user_info.user_feature_info
    for resource_type, feature_name_list_proto in resouce_feature_name_list.iteritems():
        #@note:简化逻辑，直接取平均,不考虑余数不足的情况
        resource_count = (count+len(resouce_feature_name_list)-1)/len(resouce_feature_name_list)
        reason_item_list = get_item_list_by_feature_list(user_info,
                resource_type, feature_name_list_proto, resource_count)
        logger.info("current size after hot feature list,uid:%s,resource_type:%s,count:%s" % (uid,
                resource_type, reason_item_list.size()))
        logger.debug("get new_user_recommend, resource_type:%s, result:%s" % (resource_type, reason_item_list))
        if not reason_item_list:
            continue
        add_and_dedup_recommend_item(user_info, reason_item_list, result, count)
        if result.size() >= count:
            break
    return (True, result)

def old_user_recommend(user_info, resource_distribution_info, count):
    """ recommend for old user
        @return (True|False, RecommendItemContainer)
    """
    logger.debug("begin old_user_recommend")
    result = RecommendItemContainer()
    for resource_type, cur_count in resource_distribution_info.iteritems():
        reason_item_list = old_user_recommend_for_resource_type(user_info, resource_type, cur_count)
        logger.debug("get old_user_recommend, resource_type:%s, result:%s" % (resource_type, reason_item_list))
        if not reason_item_list:
            continue
        add_and_dedup_recommend_item(user_info, reason_item_list, result, count)
        if result.size() >= count:
            break
    return (True, result)

def old_user_recommend_for_resource_type(user_info, resource_type, cur_count):
    """ get resource_type recommend for old user
        @return RecommendItemContainer
    """
    logger.debug("begin old_user_recommend_for_resource_type")
    if ResourceType.RESOURCE_TYPE_NEWS == resource_type:
        return old_user_recommend_for_news_like(user_info, resource_type, cur_count)
    else:
        return old_user_recommend_for_item(user_info, resource_type, cur_count)

def old_user_recommend_for_news_like(user_info, resource_type, count):
    """ get news recommend for old user
        @return RecommendItemContainer
    """
    logger.debug("begin old_user_recommend_for_news_like")
    uid = user_info.uid
    assert(count > 0)
    (errCode, user_feature_list) = get_user_feature_list(uid, resource_type)
    if errCode:
        user_info.user_feature_info[resource_type] = user_feature_list
    result = RecommendItemContainer()
    if errCode and len(user_feature_list.feature):
        result = get_news_online_item_by_feature_list(user_info, resource_type, user_feature_list, count)
        logger.info("current size after news::features,uid:%s,resource_type:%s,count:%s" % (uid,
                resource_type, result.size()))
        logger.debug("get old_user_recommend_news::features, resource_type:%s, result:%s" % (resource_type, result))
        if result.size() >= count:
            logger.info("finish old_user_recommend_for_news_like::features, uid:%s, count:%s" % (uid, result.size()))
            return result
    logger.info("finish old_user_recommend_for_news_like::recent, uid:%s, count:%s" % (uid, result.size()))
    return result

def old_user_recommend_for_item(user_info, resource_type, count):
    """ get item like recommend for old user
        @return RecommendItemContainer
    """
    result = RecommendItemContainer()
    uid = user_info.uid
    logger.debug("begin old_user_recommend_for_item")
    #policy *:user item list
    result = old_user_recommend_for_item_user2itemlist(user_info, resource_type, result, count)
    logger.info("current size after user2itemlist,uid:%s,resource_type:%s,count:%s" % (uid,
            resource_type, result.size()))
    if result.size() >= count:
        return result
    #policy *:user favor item list => item list
    result = old_user_recommend_for_item_item2itemlist(user_info, resource_type, result, count)
    logger.info("current size after item2itemlist,uid:%s,resource_type:%s,count:%s" % (uid,
            resource_type, result.size()))
    if result.size() >= count:
        return result
    #policy *:user feature list => item list
    result = old_user_recommend_for_item_userfeaturelist2itemlist(user_info, resource_type, result, count)
    logger.info("current size after userfeaturelist2itemlist,uid:%s,resource_type:%s,count:%s" % (uid,
            resource_type, result.size()))
    return result

def old_user_recommend_for_item_user2itemlist(user_info, resource_type, result, count):
    #user => item list
    if result.size() >= count:
        return result
    left_count = count - result.size()
    uid = user_info.uid
    logger.info("recommend by user2itemlist, uid:%s, resource_type:%s" % (uid, resource_type))
    user2itemlist = get_item_list_by_user(user_info, resource_type, left_count)
    logger.debug("get old_user_recommend_for_item::get_item_list_by_user, resource_type:%s, result:%s" % (resource_type, user2itemlist))
    result.update(user2itemlist)
    return result

def old_user_recommend_for_item_userfeaturelist2itemlist(user_info, resource_type, result, count):
    #user feature list => item list
    if result.size() >= count:
        return result
    left_count = count - result.size()
    uid = user_info.uid
    logger.info("recommend by userfeaturelist2itemlist, uid:%s, resource_type:%s" % (uid, resource_type))
    userfeaturelist2itemlist = get_item_list_by_user_feature(user_info, resource_type, left_count)
    logger.debug("get old_user_recommend_for_item::get_item_list_by_user_feature, resource_type:%s, result:%s" % (resource_type, userfeaturelist2itemlist))
    result.update(userfeaturelist2itemlist)
    return result

def old_user_recommend_for_item_item2itemlist(user_info, resource_type, result, count):
    #user favor item list => item list
    if result.size() >= count:
        return result
    left_count = count - result.size()
    uid = user_info.uid
    logger.info("recommend by item2itemlist, uid:%s, resource_type:%s" % (uid, resource_type))
    item2item_list = get_item_list_by_item(user_info, resource_type, left_count)
    logger.debug("get old_user_recommend_for_item::get_item_list_by_item, resource_type:%s, result:%s" % (resource_type, item2item_list))
    result.update(item2item_list)
    return result


def get_item_list_by_user(user_info, resource_type, count):
    """ get item list by user from offline recommendation
        @return RecommendItemContainer
    """
    logger.debug("begin get_item_list_by_user")
    uid = user_info.uid
    result = RecommendItemContainer()
    errCode, kv_dict = model.get_offline_user_recommend_item_list(uid, [resource_type])
    if not is_valid_data(errCode, kv_dict, "offline_user_recommend_item_list", {"uid":uid, "resource_type":resource_type}):
        return result
    if not kv_dict:
        return result
    try:
        assert(resource_type in kv_dict)
        reason2itemidlist = FeatureNameItemIdList()
        reason2itemidlist.ParseFromString(kv_dict[resource_type])
        for reason2itemid in reason2itemidlist.feature_name_item_id_list:
            if result.size() >= count:
                logger.debug("break for enough result")
                break
            reason = reason2itemid.feature_name
            item_id_list = ItemIdList()
            for i in reason2itemid.item_id:
                item_id_list.item_id.append(i)
            filter_and_compose_recommend_item_list(user_info, reason, item_id_list, result)
    except:
        logger.error("bad ItemIdList from get_offline_user_recommend_item_list:%s" % traceback.format_exc())
    return result

def get_item_list_by_user_feature(user_info, resource_type, count):
    """ get item list by: first get user feature list, then get item list by feature list
        @return RecommendItemContainer
    """
    logger.debug("begin get_item_list_by_user_feature")
    uid = user_info.uid
    (errCode, user_feature_list) = get_user_feature_list(uid, resource_type)
    if errCode:
        user_info.user_feature_info[resource_type] = user_feature_list
    result = RecommendItemContainer()
    if errCode and len(user_feature_list.feature):
        result = get_item_list_by_feature_list(user_info, resource_type,
                user_feature_list, count)
        if result.size() >= count:
            return result
    return result

def get_item_list_by_item(user_info, resource_type, count):
    """ get item_list by item recommendation
        @return RecommendItemContainer
    """
    logger.debug("begin get_item_list_by_item")
    uid = user_info.uid
    result = RecommendItemContainer()
    #get favor item_id列表
    errCode, kv_dict = model.get_online_user_favor_item_list(uid, [resource_type])
    if not is_valid_data(errCode, kv_dict, "online_user_favor_item_list", {"uid":uid, "resource_type":resource_type}):
        return result
    if not kv_dict:
        return result
    assert(resource_type in kv_dict)
    try:
        item_id_list_proto = ItemIdList()
        item_id_list_proto.ParseFromString(kv_dict[resource_type])
        reason_list = [resource_type+ITEM_RECOMMEND_FEATURE_TYPE+v for  v in item_id_list_proto.item_id]
        item_id_list = []
        for v in item_id_list_proto.item_id:
            if not check_reason(user_info, resource_type+ITEM_RECOMMEND_FEATURE_TYPE+v):
                continue
            item_id_list.append(v)
        if not item_id_list:
            logger.info("all item id list have no item2item result:%s" % item_id_list)
            return result
        #@note: use latest item first
        item_id_list.reverse()
        #recommend by item id
        errCode, kv_dict = model.get_offline_item_recommend_item_list(item_id_list)
        if not is_valid_data(errCode, kv_dict, "offline_item_recommend_item_list", {"item_id_list":"..."}):
            return result
        if not kv_dict:
            for item_id in item_id_list:
                reason = resource_type + ITEM_RECOMMEND_FEATURE_TYPE + item_id
                ignore_reason(user_info, reason)
            return result
        for item_id in item_id_list:
            if result.size() >= count:
                break
            if item_id not in kv_dict:
                logger.info("no item2itemid list for id:%s" % item_id)
                ignore_reason(user_info, reason)
                continue
            k = item_id
            v = kv_dict[k]
            reason = resource_type + ITEM_RECOMMEND_FEATURE_TYPE + k
            item_id_list_proto = ItemIdList()
            item_id_list_proto.ParseFromString(v)
            filter_and_compose_recommend_item_list(user_info, reason, item_id_list_proto, result)
    except:
        logger.error("bad get_item_list_by_item:%s" % traceback.format_exc())
    return result

def get_item_list_by_feature_list(user_info, resource_type, feature_name_list_proto, count):
    """ get item list by check with all feature list
        @return RecommendItemContainer
    """
    logger.debug("begin get_item_list_by_feature_list")
    feature_name_list = []
    result = RecommendItemContainer()
    filtered_feature_name_list_proto = UserFeatureList()
    for v in feature_name_list_proto.feature:
        feature_name = v.feature_name
        if not check_reason(user_info, feature_name):
            continue
        feature_name_list.append(feature_name)
        cur = filtered_feature_name_list_proto.feature.add()
        cur.feature_name = feature_name
    if not feature_name_list:
        logger.info("no new reason from feature list,current feature_name size:%s" % len(feature_name_list_proto.feature))
        logger.debug("current feature_name_list_proto:%s" % feature_name_list_proto)
        return result
    #news like
    if ResourceType.RESOURCE_TYPE_NEWS == resource_type:
        return get_news_online_item_by_feature_list(user_info, resource_type, filtered_feature_name_list_proto, count)
    #items like
    errCode, kv_dict = model.get_offline_feature_hot_item_list(feature_name_list)
    if not is_valid_data(errCode, kv_dict, "offline_feature_hot_item_list", {"feature_name_list":"..."}):
        return result
    if not kv_dict:
        for k in feature_name_list:
            ignore_reason(user_info, k)
        return result
    try:
        #logger.debug("%s" % feature_name_list)
        for k in feature_name_list: #@note:ordered
            logger.debug("check result with feature_name:%s" % k)
            if result.size() >= count:
                logger.debug("fetch enough recommend result, count:%s" % count)
                break
            if k not in kv_dict:
                logger.info("no result for feature_name:%s" % k)
                ignore_reason(user_info, k)
                continue
            v = kv_dict[k]
            item_id_list = ItemIdList()
            item_id_list.ParseFromString(v)
            filter_and_compose_recommend_item_list(user_info, k, item_id_list, result)
        logger.debug("get_item_list_by_feature_list,result_size:%s, uid:%s, resource_type:%s" % (result.size(), user_info.uid, resource_type))
    except:
        logger.error("bad ItemIdList for get_item_list_by_feature_list:%s" % traceback.format_exc())
    return result

########################################data model helper#############################################

def get_user_feature_list(uid, resource_type):
    """ get recent user feature list(merge with offline)
        @return (errCode, user_feature_list_proto) 
    """
    errCode, kv_dict = model.get_online_user_feature_list(uid, [resource_type])
    if not errCode:
        logger.warn("fail to connect with server for online_user_feature_list,uid:%s,resource_type:%s" % (uid, resource_type))
        (errCode, user_feature_list_proto) = get_offline_user_feature_list(uid, resource_type)
    else:
        if kv_dict: #fetched before
            (errCode, user_feature_list_proto) = convert_user_feature_list(errCode, kv_dict, uid, resource_type, "online_user_feature_list")
        else:
            (errCode, user_feature_list_proto) = get_offline_user_feature_list(uid, resource_type)
    logger.debug("errCode:%s,get user_feature_list, resource_type:%s, uid:%s, feature_list:%s" % (
        errCode, resource_type, uid, user_feature_list_proto))
    return (errCode, user_feature_list_proto)

def get_offline_user_feature_list(uid, resource_type):
    """ get offline user feature list
        @return (errCode, user_feature_list_proto) 
    """
    errCode, kv_dict = model.get_offline_user_feature_list(uid, [resource_type])
    return convert_user_feature_list(errCode, kv_dict, uid, resource_type, "offline_user_feature_list")

def get_news_online_item_by_feature_list(user_info, resource_type, feature_name_list_proto, count):
    """ talk with news online item interface by feature list, @return RecommendItemContainer
        @note: should filter visited feature in user_info for user_feature_list, and update user_info
    """
    max_recommend_item_count_per_reason = get_max_recommend_item_count_per_resource(resource_type)
    fetch_more_times = NEWS_FETCH_MORE_TIMES
    return raw_get_news_online_item_by_feature_list(user_info, resource_type,
            feature_name_list_proto, count, max_recommend_item_count_per_reason,
            fetch_more_times, BACKUP_NEWS_FEATURE_COUNT)

def raw_get_news_online_item_by_feature_list(user_info, resource_type, feature_name_list_proto,
        count, max_recommend_item_count_per_reason, fetch_more_times, backup_feature_count):
    """ talk with news online item interface by feature list, @return RecommendItemContainer
        @note: should filter visited feature in user_info for user_feature_list, and update user_info
    """
    result = RecommendItemContainer()
    input = FeatureNameLimitList()
    logger.debug("feature list proto:%s" % feature_name_list_proto)
    for i in feature_name_list_proto.feature:
        if not check_reason(user_info,  i.feature_name):
            continue
        #@note: temp logic to ignore some feature type
        continue_out = False
        for prefix in NEWS_IGNORE_FEATURE_NAME_PREFIX:
            if i.feature_name.startswith(prefix):
                logger.info("ignore feature:%s" % i.feature_name)
                continue_out = True
                break
        if continue_out:
            continue
        cur = input.feature_name_limit.add()
        cur.feature_name = i.feature_name
        cur.limit = int(count * max_recommend_item_count_per_reason * fetch_more_times)
        if len(input.feature_name_limit) >= count + backup_feature_count:
            logger.info("break for enough feature count:%s,feature list:%s" %
                    (len(input.feature_name_limit), input))
            break
        #logger.debug("feature_name:%s,limit:%s" % (cur.feature_name, cur.limit))
    if not input.feature_name_limit:
        logger.info("no new feature to get for news:%s, feature_list size:%s" % (resource_type, len(feature_name_list_proto.feature)))
        logger.debug("current feature_list :%s" % (feature_name_list_proto))
        return result
    try:
        #socket_out = urllib2.urlopen(NEWS_ONLINE_URL_SEARCH_BY_QUERY, urllib.urlencode(input.SerializeToString()))
        socket_out = urllib2.urlopen(NEWS_ONLINE_URL_SEARCH_BY_QUERY, input.SerializeToString(),
                timeout=online_clicklog_feedback.NEWS_TIMEOUT_SECONDS)
        return_data = socket_out.read()
    except:
        logger.error("fail to talk with online news server,featurelists:%s,exceptions:%s" %
                (input, traceback.format_exc()))
        return result
    try:
        output = NewsFeatureItemList()
        output.ParseFromString(return_data)
        logger.debug("get news online item list result,user_info:%s,result:%s" % (user_info, output))
    except:
        logger.error("bad parse news return value:%s" % traceback.format_exc())
        return result
    for reason_item_id_list in output.feature_item:
        if not len(reason_item_id_list.item_feature_info):
            continue
        reason = reason_item_id_list.feature_name
        resource_type = ResourceType.get_resource_type(reason)
        item_list = []
        for i in reason_item_id_list.item_feature_info:
            if i.item_id in user_info.recent_push_item_id_list:
                logger.debug("ignore existing item id:%s" % i.item_id)
                continue
            item = RecommendItem()
            item.item_id = i.item_id
            item.item_info_json = i.item_info
            item.feature_name_list = i.item_feature_list 
            item_list.append(item)
            user_info.recent_push_item_id_list.add(i.item_id)
            logger.info("item_list:%s" %item_list)
            if len(item_list) >= max_recommend_item_count_per_reason:
                logger.debug("real_list size:%s, select part:%s" % (len(reason_item_id_list.item_feature_info),
                            max_recommend_item_count_per_reason))
                break
        if not item_list or len(item_list) < max_recommend_item_count_per_reason:
            logger.info("not enough data, discard:%s" % (item_list))
            ignore_reason(user_info, reason)
            #fetch not enough data, discard this reason
            continue
        result.add(reason, item_list)
        add_reason(user_info, reason)
        if result.size() >= count:
            break
    if not result:
        logger.info("get empty get_news_online_item_by_feature_list")
    return result

def get_resource_hot_feature_list(user_info, count):
    """ get resource hot feature list, maybe top level category for per resource type, filter existing feature_name list pushed to user
        @return {resource_type:feature_name_list}
    """
    #@note:下期推荐策略：从最重要的resource开始.这里均匀选取
    #1.确定各个resource_type的数量比例:均匀选取
    #2.取每个resource的feature list按照重要性从高到低排列
    result = {}
    errCode, kv_dict = model.get_offline_global_hot_feature_list(ResourceType.RESOURCE_TYPE_LIST)
    if not is_valid_data(errCode, kv_dict, "global_hot_feature_list", {"resource_type_list":"..."}):
        return {}
    if not kv_dict:
        return {}
    try:
        for k,v in kv_dict.iteritems():
            item_feature_list = ItemFeatureList()
            item_feature_list.ParseFromString(v)
            result[k] = item_feature_list
            logger.debug("resource_type:%s, hot_feature_list:%s" % (k, result[k]))
    except:
        logger.error("bad get_offline_global_hot_feature_list:%s" % traceback.format_exc())
    logger.info("input resource_type_size:%s, result resource_type_size:%s" % (len(ResourceType.RESOURCE_TYPE_LIST), len(kv_dict)))
    logger.debug("get_resource_hot_feature_list, user_info:%s, count:%s, result:%s" % (user_info, count, result))
    return result

def update_user_info(user_info, recommend_result):
    """ update recommend_result to user_info
        @return None
    """
    #@note:暂时不获取item_feature结构（不管是news还是item类，为了计算用户的feature和feature偏好的pv部分）；
    #@note:item_id列表的push由外围世荣处保证
    for reason,item_list in recommend_result.reason2itemidlist.iteritems():
        add_reason(user_info, reason)
        for v in item_list:
            resource_type = ResourceType.get_resource_type(v.item_id)
            assert(resource_type)
            user_info.recent_resource_visit_info.setdefault(resource_type, VisitInfo())
            user_info.recent_resource_visit_info[resource_type].pv_count += 1
    #set online user_feature_reason and user resource visit info
    feature_list = ItemFeatureList()
    for reason,weight in user_info.recent_push_reason_info.iteritems():
        feature = feature_list.feature.add()
        feature.feature_name = reason
        feature.weight = weight
    uid = user_info.uid
    errCode = model.set_online_user_feature_reason(uid, feature_list.SerializeToString())
    if not errCode:
        logger.warn("fail to set_online_user_feature_reason, uid:%s" % uid)
    for resource_type,visit_info in user_info.recent_resource_visit_info.iteritems():
        errCode = model.set_online_user_resource_visitinfo(uid, resource_type, visit_info.SerializeToString())
        if not errCode:
            logger.warn("fail to set_online_user_resource_visitinfo, uid:%s, resource_type:%s" % (uid, resource_type))
    #feedback for show action
    update_user_feature_list_for_show_action(user_info, recommend_result)

def update_user_feature_list_for_show_action(user_info, recommend_result):
    """ update user info pv(show) action info
    """
    uid = user_info.uid
    reasons = {}
    #get resource_type list
    for k in recommend_result.reason_list:
        resource_type = ResourceType.get_resource_type(k)
        reasons.setdefault(resource_type, [])
        reasons[resource_type].append(k)
    #update show action info
    for k,v in reasons.iteritems():
        user_feature_list = None
        if k in user_info.user_feature_info:
            user_feature_list = user_info.user_feature_info[k]
        else:
            errCode, user_feature_list = get_user_feature_list(uid, k)
            if not errCode:
                continue
        item_feature_list = ItemFeatureList()
        for i in v:
            cur_feature = item_feature_list.feature.add()
            cur_feature.feature_name = i
        errCode = online_clicklog_feedback.raw_update_user_action(uid, k, user_feature_list, item_feature_list,
                card_feature='', favor_type='show')
        logger.info("update user action info, uid:%s,resource_type:%s,errCode:%s" % (uid, k, errCode))
    return None


############################################recommend util####################################################

def add_and_dedup_recommend_item(user_info, reason_item_list, result, count):
    """ add current result to final result, and dedup, remove the extra more item
        note:input recommend_item_list may be more than count
        @return None
    """
    result.merge_dedup(reason_item_list, count)
    return None

def get_resource_distribution_info(final_resource_visit_info, count):
    """ determine the distribution of different resource type
        @return {resource_type:count}
    """
    result = {}
    get_resource_weight = lambda visit_info,n: (pow(visit_info.click_count, 2)+1.0) / (pow(visit_info.pv_count, 1.6)+visit_info.pv_count+n)
    resouce_count = len(final_resource_visit_info)
    weight = {}
    sum = 0
    for k in ResourceType.RESOURCE_TYPE_LIST:
        if k not in final_resource_visit_info:
            v = VisitInfo()
            logger.debug("resource:%s not visited before" % k)
        else:
            v = final_resource_visit_info[k]
        logger.debug("resource:%s info:%s" % (k, v))
        weight[k] = min(3.0, get_resource_weight(v,count)/get_resource_weight(VisitInfo(),count))
        sum += weight[k]
    temp_sum = 0
    for k,v in weight.iteritems():
        result[k] = int(count*weight[k]/sum)
        logger.debug("resource:%s weight:%s" % (k, result[k]))
        temp_sum += result[k]
    bad_resource_set = set()
    for i in result:
        if result[i] == 0:
            result[i] = 1
            temp_sum += 1
            bad_resource_set.add(i)
    while temp_sum < count:
        for k,v in result.iteritems():
            if temp_sum >= count:
                break
            if k in bad_resource_set:
                continue
            result[k] += 1
            temp_sum += 1
    #for k in ResourceType.RESOURCE_TYPE_LIST:
    #    #@note:简单策略，直接平均取上整
    #    result[k] = (count+len(ResourceType.RESOURCE_TYPE_LIST)-1)/len(ResourceType.RESOURCE_TYPE_LIST)
    return result

def filter_and_compose_recommend_item_list(user_info, reason, item_id_list_proto, result):
    """ try set result[reason] = item_id_list_proto and compose result if no dedup, update user_info
        @return None
    """
    logger.debug("try to add recommend, reason:%s, item_id_list_proto:%s" % (reason, item_id_list_proto))
    if  not check_reason(user_info, reason):
        logger.debug("existing feature_type, ignore:%s" % reason)
        return 
    result_item_id_list = []
    resource_type = ResourceType.get_resource_type(reason)
    for v in item_id_list_proto.item_id:
        if v in user_info.recent_push_item_id_list:
            continue
        result_item_id_list.append(v)
        user_info.recent_push_item_id_list.add(v)
        max_recommend_item_count_per_reason = get_max_recommend_item_count_per_resource(resource_type)
        if len(result_item_id_list) >= max_recommend_item_count_per_reason:
            logger.debug("real_list size:%s, select part:%s" % (len(item_id_list_proto.item_id),
                        max_recommend_item_count_per_reason))
            break
    if not result_item_id_list:
        logger.info("all item id list has been pushed")
        logger.debug("all item id list has been pushed:%s" % item_id_list_proto)
        return
    if not result_item_id_list:
        return
    result_recommend_item = [RecommendItem(item_id=v) for v in result_item_id_list]
    result.add(reason, result_recommend_item)
    add_reason(user_info, reason)
    return

def convert_user_feature_list(errCode, kv_dict, uid, resource_type, desc):
    """ convert user feature list kv_dict to user_feature_list_proto
        @return (errCode, user_feature_list_proto) 
    """
    if not is_valid_data(errCode, kv_dict, desc, {"uid":uid, "resource_type":resource_type}):
        return (False, None)
    if not kv_dict:
        return (True, UserFeatureList())
    result = UserFeatureList()
    assert(resource_type in kv_dict)
    try:
        result.ParseFromString(kv_dict[resource_type])
    except:
        logger.error("bad convert_user_feature_list:%s" % traceback.format_exc())
        return False, result
    return True, result 

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(name)s    %(filename)s +%(lineno)d    %(levelname)s   %(message)s")
    logging.config.fileConfig('logging.conf')
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

    feature_list = [
        "newsctgy财经",
        "newsctgy科技",
        "newsctgy国内",
        "newsctgy新闻",
        "newsctgy趣味",
        "newsctgy体育",
        "newsctgy生活",
        "newsctgy娱乐",
        "newsctgy汽车",
        "newsctgy文史",
        "newsctgy时尚",
        "newsctgy游戏",
        "newsctgy社会",
        "newsctgy国际",
        "newsctgy军事",
        "newsctgy美图",
        "newsctgy房产",
        "newsctgy女人",
        "newsctgy本地新闻"
    ]

    #for feature in feature_list:
    #    get_more_news_recommend('uid', feature, 50)
    #sys.exit(1)

    if len(sys.argv) < 2:
        print "usage:%s request(r)"
        sys.exit(1)
    if sys.argv[1] in [ "r", "request"]:
        for i in range(0, 1):
            errCode, reason2itemlist_dict = get_request_recommend(uid="868943006799672", count=2)
    else:
        print "usage:%s request(r)|click(c)"
        sys.exit(1)


