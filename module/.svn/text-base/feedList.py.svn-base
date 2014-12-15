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
import common

# getLogger
logger = logging.getLogger() 

# global vars
MAX_FEED_COUNT_FOR_FRONTPAGE = 300

# 解析feedid 字符串列表
# [update_time\tfeedid\tresouce_id, ...]
def parseFeedIdStringList ( call_name, str_feedid_list):
    if( str_feedid_list == None ):
        return []

    result = []
    for feedid in str_feedid_list :
        feedid_fds = feedid.split( '\t' )
        if len(feedid_fds) < 2 or feedid_fds[0] == '' or feedid_fds[1] == '':
            logger.error( '%s, parse feedid faild ,%s', call_name, feedid )
            continue

        feedid_fds[0] = int(feedid_fds[0])

        if len(feedid_fds) < 3 :
            feedid_fds.append( '' )

        result.append( feedid_fds )

    return result

# 从cache得到用户feed 列表
def getUserFeedIdList_FromCache( uid ):
    logger.debug( 'getUserFeedIdList_FromCache, id=%s', uid )

    redis = db_cache.get_redis_feed_list()
    if redis == None: # error logging in db_cache
        return None
    
    key = uid+'_ufid'

    if not redis.Exists( key ):
        logger.error( 'getUserFeedIdList_FromCache faild, no key=%s', key )
        return None
    
    result = redis.LRange( key, 0, -1 )
    if result == None or redis.GetLastErrNo() != 0  :
        logger.error( 'getUserFeedIdList_FromCache faild, key=%s, errno=%d', key, redis.GetLastErrNo() )
        return None
    
    return result

# 将用户feed 列表更新到cache
def updateUserFeedIdList_ToCache( uid, feedid_list ) :
    redis = db_cache.get_redis_feed_list()
    if redis == None: # error logging in db_cache
        return False 
    
    key = uid+'_ufid'
    redis.Del( key )
    if not redis.LPush( key, feedid_list ):
        logger.error( 'updateUserFeedIdList_ToCache faild, key=%s, errno=%d', key, redis.GetLastErrNo() )
        return False
    
    return True

# 从db得到用户feed 列表
def getUserFeedIdList_FromDB( uid ) :
    logger.debug( 'getUserFeedIdList_FromDB, id=%s', uid )

    db = db_cache.getdb()
    if db == None: # error logging in db_cache
        return None
    
    result = []
    try:
        rs = db.query( 'select resource_id, feed_id, last_modify_time from subscription where user_id=\'%s\' order by last_modify_time desc' % uid )
        strResourceIds = ''
        for rd in rs :
            if strResourceIds != '' :
                strResourceIds += ',' 
            strResourceIds += '\'' + rd[0] + '\''

        if strResourceIds == '' :
            return []
        
        resUpdateTimes = {}
        rs1 = db.query( 'select resource_id, update_time from resource_info where resource_id in (%s) order by update_time desc' % strResourceIds )
        for rd in rs1 :
            resUpdateTimes[rd[0]] = rd[1]

        for rd in rs :
            ut = resUpdateTimes.get( rd[0] )
            if ut == None :
                ut = rd[2]
            
            result.append( '%d\t%s\t%s' % (time.mktime(time.strptime(str(ut), "%Y-%m-%d %H:%M:%S")) , \
                                            rd[1], \
                                            rd[0]) )
    
        return result

    except:
        logger.error( 'getUserFeedIdList_FromDB faild, %s', str(sys.exc_info()) )
        return None


# 得到用户feed 列表
def getUserFeedIdList( uid, nocache = False ) :
    feedid_list = None
    if not nocache :
        feedid_list = getUserFeedIdList_FromCache( uid )

    if feedid_list == None :
        feedid_list = getUserFeedIdList_FromDB( uid )
        if feedid_list != None :
            updateUserFeedIdList_ToCache( uid, feedid_list )
        
    if feedid_list == None:
        return []

    feedid_list = parseFeedIdStringList( 'getUserFeedIdList', feedid_list )
    return feedid_list

# 从cache得到首页feed 列表
def getFeedIdList_FromCache( key ):
    logger.debug( 'getFeedIdList_FromCache, key=%s', key )

    redis = db_cache.get_redis_feed_list()
    if redis == None: # error logging in db_cache
        return None
    
    key = key+'_fid'
    
    if not redis.Exists( key ):
        logger.error( 'getFeedIdList_FromCache faild, no key=%s', key )
        return None

    result = redis.LRange( key, 0, MAX_FEED_COUNT_FOR_FRONTPAGE )
    if result == None or redis.GetLastErrNo() != 0  :
        logger.error( 'getFeedIdList_FromCache faild, key=%s, errno=%d', key, redis.GetLastErrNo() )
        return None

    return result

# 将首页feed 列表更新到cache
def updateFeedIdList_ToCache( key, feedid_list ) :
    redis = db_cache.get_redis_feed_list()
    if redis == None: # error logging in db_cache
        return False 
    
    key = key+'_fid'
    redis.Del( key )
    if not redis.LPush( key, feedid_list ):
        logger.error( 'updateLocationFeedIdList_ToCache faild, key=%s, errno=%d', key, redis.GetLastErrNo() )
        return False

    return True 

# 从db得到ALL地区的非news feed 列表
def getGlobalNoNewsFeedIdList_FromDB( ) :
    logger.debug( 'getGlobalNoNewsFeedIdList_FromDB' )

    db = db_cache.getdb()
    if db == None: # error logging in db_cache
        return None
    
    result = []
    try:
        rs = db.query( 'select feed_id, update_time from feed where visibility=1 and type!=\'news\' order by update_time desc limit %d' % MAX_FEED_COUNT_FOR_FRONTPAGE )
        for rd in rs :
            result.append( '%d\t%s' % (time.mktime(time.strptime(str(rd[1]), "%Y-%m-%d %H:%M:%S")) , rd[0]) )
    
        print 'getGlobalNoNewsFeedIdList_FromDB: ============================================='
        print str(result)
        return result

    except:
        logger.error( 'getGlobalNoNewsFeedIdList_FromDB faild, %s', str(sys.exc_info()) )
        return None

# 从db得到ALL地区的news feed 列表
def getGlobalNewsFeedIdList_FromDB( ) :
    logger.debug( 'getGlobalNewsFeedIdList_FromDB' )

    db = db_cache.getdb()
    if db == None: # error logging in db_cache
        return None
    
    result = []
    try:
        rs = db.query( 'select feed_id, update_time from feed where visibility=1 and type=\'news\' and area=\'china\' order by update_time desc limit %d' % MAX_FEED_COUNT_FOR_FRONTPAGE )
        for rd in rs :
            result.append( '%d\t%s' % (time.mktime(time.strptime(str(rd[1]), "%Y-%m-%d %H:%M:%S")) , rd[0]) )
    
        print 'getGlobalNewsFeedIdList_FromDB: ============================================='
        print str(result)
        return result

    except:
        logger.error( 'getGlobalNewsFeedIdList_FromDB faild, %s', str(sys.exc_info()) )
        return None

# 从db得到指定地区的news feed 列表
def getLocalNewsFeedIdList_FromDB( areaName ) :
    logger.debug( 'getLocalNewsFeedIdList_FromDB, area=%s' , areaName )

    db = db_cache.getdb()
    if db == None: # error logging in db_cache
        return None
    
    result = []
    try:
        rs = db.query( 'select feed_id, update_time from feed where visibility=1 and type=\'news\' and area=\'%s\' order by update_time desc limit %d' % (areaName, MAX_FEED_COUNT_FOR_FRONTPAGE) )
        for rd in rs :
            result.append( '%d\t%s' % (time.mktime(time.strptime(str(rd[1]), "%Y-%m-%d %H:%M:%S")) , rd[0]) )
    
        print 'getLocalNewsFeedIdList_FromDB: ============================================='
        print str(result)
        return result

    except:
        logger.error( 'getLocalNewsFeedIdList_FromDB faild, %s', str(sys.exc_info()) )
        return None

# 得到ALL地区的非news feed 列表
def getGlobalNoNewsFeedIdList( nocache = False ) :
    key = 'all_user_front_page_feed'
    feedid_list = None
    if not nocache :
        feedid_list = getFeedIdList_FromCache( key )

    if feedid_list == None or len(feedid_list) == 0 :
        feedid_list = getGlobalNoNewsFeedIdList_FromDB( )
        if feedid_list != None :
            updateFeedIdList_ToCache( key, feedid_list )
        
    if feedid_list == None:
        return []

    return parseFeedIdStringList( 'getGlobalNoNewsFeedIdList', feedid_list )

# 得到ALL地区的news feed 列表
def getGlobalNewsFeedIdList( nocache = False ) :
    key = 'china_news'
    feedid_list = None
    if not nocache :
        feedid_list = getFeedIdList_FromCache( key )

    if feedid_list == None or len(feedid_list) == 0 :
        feedid_list = getGlobalNewsFeedIdList_FromDB( )
        if feedid_list != None :
            updateFeedIdList_ToCache( key, feedid_list )
        
    if feedid_list == None:
        return []

    return parseFeedIdStringList( 'getGlobalNewsFeedIdList', feedid_list )

# 得到ALL地区的news feed 列表
def getLocalNewsFeedIdList( areaName, nocache = False ) :
    areaName = areaName.strip()
    if areaName == '' :
        return []
    
    key = '%s_news' % areaName
    feedid_list = None
    if not nocache :
        feedid_list = getFeedIdList_FromCache( key )

    if feedid_list == None or len(feedid_list) == 0 :
        feedid_list = getLocalNewsFeedIdList_FromDB( areaName )
        if feedid_list != None :
            updateFeedIdList_ToCache( key, feedid_list )
        
    if feedid_list == None:
        return []

    return parseFeedIdStringList( 'getLocalNewsFeedIdList', feedid_list )

# 从得到地域 feed 列表
def getFrontpageFeedIdList( areaName, nocache = False ) :
    # 得到本地化news feedid list
    news_feedid_list = None
    areas = areaName.split( ',' )[0:2]
    areas.reverse()
    for area in areas :
        news_feedid_list = getLocalNewsFeedIdList( area, nocache )
        if news_feedid_list != None and len(news_feedid_list) > 0 :
            break        

    # 如果本地化news 列表为空，则去全局news list
#    if news_feedid_list == None or len(news_feedid_list) <= 0 :
    global_news_feedid_list = getGlobalNewsFeedIdList( nocache )
    
    # 得到非新闻 feed list
    feedid_list = getGlobalNoNewsFeedIdList( nocache )

    # 合并列表
    feedid_list += news_feedid_list if news_feedid_list != None else []
    feedid_list += global_news_feedid_list if global_news_feedid_list != None else []

    return feedid_list

