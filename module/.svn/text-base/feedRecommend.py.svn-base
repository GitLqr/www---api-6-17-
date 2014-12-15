#-*- coding: utf8 -*-
import sys
import web
import logging
import logging.config
import json
import conf
import db_cache
import chardet
import urllib
import urllib2
import urlparse
import time
import hashlib
import common
import feedList
import feedContent

import recommend.data_manage.model_interface as recommend_model_interface
recommend_model_interface.db_cache_init( conf.getConfig( 'db_recommend' ), conf.getConfig( 'cache_recommend' ) )
import recommend.request_recommend.online_request_recommend_app as request_recommend
import recommend.push_item_merge.push_item_interface as push_item_interface

# getLogger
logger = logging.getLogger() 

# defines
MAX_CACHE_RECOMMEND_FEEDID_COUNT = 300

# 从cache得到历史推荐feedid_list
def getHistoryRecommendFeedIdList_FromCache ( uid ):
    logger.debug( 'getHistoryRecommendFeedIdList_FromCache, uid=%s', uid )

    redis = db_cache.get_redis_feed_list()
    if redis == None: # error logging in db_cache
        return None
    
    key = uid+'_rfid'
    if not redis.Exists( key ):
        logger.error( 'getHistoryRecommendFeedIdList_FromCache faild, no key=%s', key )
        return None
    
    result = redis.LRange( key, 0, MAX_CACHE_RECOMMEND_FEEDID_COUNT+100 )
    if result == None or redis.GetLastErrNo() != 0  :
        logger.error( 'getHistoryRecommendFeedIdList_FromCache faild, key=%s, errno=%d', key, redis.GetLastErrNo() )
        return None

    if len(result) >= MAX_CACHE_RECOMMEND_FEEDID_COUNT+100 :
        redis.Del( key )
        if not redis.LPush( key, result[0:MAX_CACHE_RECOMMEND_FEEDID_COUNT] ) :
            logger.error( 'Resize RecommendFeedIdList_ToCache faild, key=%s, errno=%d', key, redis.GetLastErrNo() )
            return False
    
    if len(result) > MAX_CACHE_RECOMMEND_FEEDID_COUNT :
        return result[0:MAX_CACHE_RECOMMEND_FEEDID_COUNT]
    else:
        return result

# 得到历史推荐feedid list
def getHistoryRecommendFeedIdList ( uid ):
    feedid_list = getHistoryRecommendFeedIdList_FromCache( uid )
    feedid_list = feedList.parseFeedIdStringList( 'getHistoryRecommendFeedIdList', feedid_list )
    return feedid_list

# 将新推荐的feedid list push到cache
def pushRecommendFeedIdList_ToCache ( uid, feedid_list ):
    redis = db_cache.get_redis_feed_list()
    if redis == None: # error logging in db_cache
        return False
    
    key = uid+'_rfid'
    result = redis.LPush( key, feedid_list )
    if not result :
        logger.error( 'pushRecommendFeedIdList_ToCache faild, key=%s, errno=%d', key, redis.GetLastErrNo() )
        return False

    return True

# 根据新闻datalist, 对新闻列表进行排版 mutliTop3i
def getNewsMiniFeedLayout ( data_list ):
    if len(data_list) <= 0 :
        return 'single'
    
    # 单条模板
    if len(data_list) == 1 :
        imageDataList = data_list[0].get('imageDataList')
        if imageDataList != None and len(imageDataList) > 0 :
            return 'singleRight1i'
        else:
            return 'single'
    
    # 多条模板
    else:
        # 多图模板
        for i in xrange( 0, len(data_list) ) :
            data = data_list[i]
            imageDataList = data.get('imageDataList')
            if imageDataList == None or len(imageDataList) <= 0 :
                continue

            if len(imageDataList) >= 3 :
                if i > 0 :
                    data_list.insert( 0, data_list.pop(i) )
                return 'multiTop3i'

        # 单图图模板
        for i in xrange( 0, len(data_list) ) :
            data = data_list[i]
            imageDataList = data.get('imageDataList')
            if imageDataList == None or len(imageDataList) <= 0 :
                continue

            if len(imageDataList) >= 1 :
                if i > 0 :
                    data_list.insert( 0, data_list.pop(i) )
                return 'multiRight'

        return 'multiRight'
        
# 根据新推荐的item信息， 生成minifeed
def makeRecommendMiniFeed ( reason, title, item_list ):
    minifeed = {}
    minifeed['updateTime'] = int(time.time())
    minifeed['layout'] = "single"
    minifeed['area'] = ""
    minifeed['title'] = title
    minifeed['feedId'] = ''
    minifeed['visibility'] = 1
    minifeed['feed_type'] = "add"
    minifeed['data'] = []
    minifeed['reason'] = reason 

    short_type = reason[0:4]
    feedid_type = short_type
    if short_type == 'news' :
        minifeed['type'] = 'news'
    elif short_type == 'movi' or short_type == 'tele' or short_type == 'cart' or short_type == 'show' :
        minifeed['type'] = 'video'
        feedid_type = 'vdeo'
    elif short_type == 'novl' :
        minifeed['type'] = 'story'
    else:
        logger.error( 'makeRecommendMiniFeed faild, type invalid, %s', short_type )
        return ('', None)

    data_list = []
    itemids = ''
    for item_info in item_list :
        try:
            item = {}
            if item_info.item_info_json != None:
                item = json.loads( item_info.item_info_json, strict=False )

            item['id'] = item_info.item_id

            itemids += item['id']
            data_list.append( item )

        except:
            logger.error( 'makeRecommendMiniFeed data item faild, item_info=%s, %s', item_info, str(sys.exc_info()) )

    if len(data_list) <= 0 :
        return ('', None)

    minifeed['data'] = data_list

    if short_type == 'news' :
        minifeed['layout'] = getNewsMiniFeedLayout( data_list )    

    feedid = feedid_type + hashlib.new("md5", itemids).hexdigest()[0:16]
    minifeed['feedId'] = feedid

    return (feedid, minifeed)
    
# 得到新推荐feed list
def getRecommendFeedList ( uid, count, exclude_itemid_list = None):
    logger.debug( 'getRecommendFeedList, uid=%s, count=%d', uid, count )

    # 反馈已存在的id， 用于推荐去重
    t = time.time()
    push_item_interface.push_item_id_list_merge( uid, exclude_itemid_list )
    logger.debug( 'push_item_id_list_merge, Spent=%d', (time.time()-t)*1000 )
    t = time.time()
    # 得到推荐
    (success, result) = request_recommend.get_request_recommend( uid, count )
    logger.debug( 'get_request_recommend, Spent=%d', (time.time()-t)*1000 )
    if not success :
        logger.error( 'getRecommendFeedList faild, recommend return faild' )
        return (None,None)

    str_feedid_list = []
    feedid_list = []
    minifeed_list = []
    itemid_list = []
    for reason, item_list in result :
        # 记录所有的item id
        for item in item_list :
            itemid_list.append( item.item_id )
            
        (strReason, title) = reason

        # 生成minifeed
        (feedid, minifeed) = makeRecommendMiniFeed( strReason, title, item_list )
        if feedid == '' or minifeed == None :
            continue        

        # 记录feedid
        str_feedid_list.append( '%d\t%s' % (int(time.time()), feedid) )
        feedid_list.append( [int(time.time()), feedid, ''] )
        minifeed_list.append( minifeed )

    # 反馈item id ， 用于下次推荐去重
    push_item_interface.push_item_id_list_merge( uid, itemid_list )

    logger.debug( 'getRecommendFeedList ok, %s', str(feedid_list) )

    # 保存feedidlist到cache
    pushRecommendFeedIdList_ToCache( uid, str_feedid_list )

    # 得到minifeed data字段里面的内容
    minifeed_list = feedContent.getMiniFeedsDataContent_ForList( minifeed_list )

    return (feedid_list, minifeed_list)


