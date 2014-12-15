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
import string
import hashlib

import music_interface
import video_interface
import news_interface

#sys.path.append('./module')
import novel.novel_reader as novel_reader

import recommend.data_manage.model_interface as recommend_model_interface
recommend_model_interface.db_cache_init( conf.getConfig( 'db_recommend' ), conf.getConfig( 'cache_recommend' ) )

# getLogger
logger = logging.getLogger() 

# 得到minifeeds ，从cache
def getMiniFeeds_FromCache ( feedids ):
    logger.debug( 'getMiniFeeds_FromCache, ids=(%s)', string.join(feedids,',') )

    if len( feedids ) <= 0 :
        return {}
    
    redis = db_cache.get_redis_minifeed()
    if redis == None: # error logging in db_cache
        return None

    keys = [ feedid+'_mfeed' for feedid in feedids] 
    minifeeds = redis.MGet( keys )
    if minifeeds == None :
        logger.error( 'getMiniFeeds_FromCache faild, errno=%d', redis.GetLastErrNo() )
        return None

    result = {}
    index = 0
    for feedid in feedids :
        result[feedid] = minifeeds[index]
        #print feedids[index] , len( minifeed )
        index += 1

    return result

# 更新minifeed ，到cache
def updateMiniFeed_ToCache ( feedid, minifeed ):
    redis = db_cache.get_redis_minifeed()
    if redis == None: # error logging in db_cache
        return False

    if isinstance( minifeed, dict ) :
        minifeed = json.dumps(minifeed, ensure_ascii=False)

    key = feedid+'_mfeed'
    if not redis.Set( key, minifeed ) :
        logger.error( 'updateMiniFeed_ToCache faild, key=%s, errno=%d', key, redis.GetLastErrNo() )
        return False
        
    return True

# 得到minifeeds ，从DB
def getMiniFeeds_FromDB ( feedids ):
    if len( feedids ) <= 0 :
        return {}
    
    db = db_cache.getdb()
    if db == None: # error logging in db_cache
        return None
    
    result = {}
    strFeedIds = ''
    for feedid in feedids :
        if feedid == '' :
            continue
        
        if strFeedIds != '' :
            strFeedIds += ',' 
        strFeedIds += '\'' + feedid + '\''

    logger.debug( 'getMiniFeeds_FromDB, ids=(%s)', strFeedIds )

    try:
        rs = db.query( 'select feed_id, jsonstr from feed where feed_id in (%s)' % strFeedIds )
        #print 'select feed_id, jsonstr from feed where feed_id in (%s)' % strFeedIds
        for rd in rs :
            result[rd[0]] = rd[1]
            updateMiniFeed_ToCache( rd[0], rd[1] )
    
        return result

    except:
        logger.error( 'getMiniFeeds_FromDB faild, %s', str(sys.exc_info()) )
        return None

# 检测minifeed格式是否正确
def checkMiniFeedFormat ( minifeed ):
    if not isinstance(minifeed, dict):
        return False

    feedid = minifeed.get('feedId')
    if feedid == None or feedid == '' :
        return False    
    
    minifeed_data = minifeed.get('data')
    if minifeed_data == None or not isinstance(minifeed_data, list) or len(minifeed_data) <= 0 :
        return False

    for data in minifeed_data :
        if not isinstance(data,dict) or not data.has_key('id'):
            return False
        
    return True
    
# 判断minifeed data节点里是否有内容 
def isHasContentInMiniFeedData ( data ):
    return len( data ) > 3 
    
# 得到minifeeds
def getMiniFeeds ( feedids, nocache = False ):
    minifeeds = None 
    if not nocache :
        minifeeds = getMiniFeeds_FromCache( feedids )

    no_cache_feedids = []
    if minifeeds == None:
        no_cache_feedids = feedids 
    else:
        for feedid, minifeed in minifeeds.iteritems() :
            if minifeed == '':
                no_cache_feedids.append( feedid )

    minifeeds_db = getMiniFeeds_FromDB( no_cache_feedids )

    if minifeeds == None:
        if minifeeds_db == None :
            pass
        else:
            minifeeds = minifeeds_db 
    else:
        if minifeeds_db == None :
            pass
        else:
            minifeeds.update( minifeeds_db )
            
    # 解析minifeed成dict
    for key, strMiniFeed in minifeeds.iteritems() :
        if strMiniFeed == None or strMiniFeed == '' :
            minifeeds[key] = None
            logger.error( 'the minifeed is blank, id=%s', key )
            continue            
        
        try:
            minifeed = json.loads( strMiniFeed, strict=False )
            if not checkMiniFeedFormat( minifeed ):
                logger.error( 'the minifeed format is error, id=%s', key )
                minifeeds[key] = None
            else:
                minifeeds[key] = minifeed
        except:
            logger.error( 'the minifeed is invalid, json load faild, id=%s, err=%s', key, str(sys.exc_info() ) )
            minifeeds[key] = None

    return minifeeds

# 获取feed 的摘要内容
# 摘要内容会和minifeed一起放到cache，所以不需要再单独cache摘要内容
def getMiniFeedDataSummary ( id, srcid ):
    logger.debug( 'getMiniFeedDataSummary from third interface, id=%s, srcid=%s', id, srcid )

    # cache没有发现，则调用内容获取接口
    if isinstance( srcid, unicode ):
        srcid = srcid.encode( 'utf8' )

    cat = id[0:4]
    status = 0
    msg = ''
    content = {}

#    if cat == 'news':
        #content = getNewsContent( srcContId )
#        return {}
    if cat == 'movi' :
        (status,msg,content) = video_interface.video_interface( {'id':srcid, 'info_type':1} )
#    elif cat == 'music' :
#        content = music_interface.Music_interface.Get_music_detail( srcContId )
    elif cat == 'novl' :
        novel_reader_obj = novel_reader.NovelReader()
        (status,msg,content) = novel_reader_obj.fetch_novel_info( {'id':srcid, 'info_type':4} )
    else:
        logger.error( "getMiniFeedDataSummary faild, type is invalid, id=%s, srcid=%s", id, srcid )
        return {}
        
    if content == None or len(content) == 0 :
        logger.error( "getMiniFeedDataSummary faild, id=%s, srcid=%s", id, srcid )
        return {}

    return content
    
# 取minifeed里面的data内容
def getMiniFeedDataContent ( feedid, minifeed, srcids ):
    # 对每个mini_feed，检测data里面是否有内容数据，
    # 如果没有，则请求内容获取接口
    success = False
    modified = False
    minifeed_datas = minifeed['data']
    i = 0
    for data in minifeed_datas :
        # 没有内容，则需要请求内容接口
        if not isHasContentInMiniFeedData( data ) :
            id = data['id'] 
            srcid = srcids.get(id)
            if srcid == None or srcid == '':
                logger.error( 'getMiniFeedDataSummary faild, get srcid faild, id=%s', id )
                continue
            
            content = getMiniFeedDataSummary( id, srcid )
            if content != None and len(content) > 0 :
                content['id'] = id
                minifeed_datas[i] = content
                modified = True
                success = True
        else:
            success = True

        i += 1
    
    # 如果对data节点有修改，则更新到cache
    if modified :
        updateMiniFeed_ToCache( feedid, json.dumps(minifeed, ensure_ascii=False) )

    return success    

# 根据id得到数据的源ID
def getMiniFeedDataSrcIds ( idlist ):
    if len(idlist) <= 0 :
        return {}
        
    (success, srcids) = recommend_model_interface.get_offline_item_id_new_to_old( idlist )
    if not success :
        logger.error( 'getMiniFeedDataSrcIds faild, ids=%s', str(idlist) )
        return {}
    else:
        logger.debug( 'getMiniFeedDataSrcIds, ids=%s, srcids=%s', str(idlist), str(srcids) )
        return srcids   
    
def getMiniFeedDataSrcId ( id ):
    (success, srcids) = recommend_model_interface.get_offline_item_id_new_to_old( [id] )
    if not success :
        logger.error( 'getMiniFeedDataSrcId faild, id=%s', id )
        return None
    else:
        srcid = srcids.get( id )
        if srcid == None or srcid == '' :
            logger.error( 'getMiniFeedDataSrcId faild, id=%s', id )
            return None
        else:
            logger.debug( 'getMiniFeedDataSrcId, id=%s, srcid=%s', id, srcid )
            return srcid

# 得到minifeed 中的data content
def getMiniFeedsDataContent ( minifeeds ):
    logger.debug( 'getMiniFeedsDataContent...' )
    # 根据minifeed中的data节点里的id字段，得到数据源id
    def __getMiniFeedDataSrcIds ( minifeeds ):
        ids = []
        # 找出没有resid字段的data里的id
        for key, minifeed in minifeeds.iteritems() :
            if minifeed == None :
                continue
            for data in minifeed['data'] :
                if not isHasContentInMiniFeedData( data ) :
                    ids.append(data['id'])

        # 得到老的ID
        srcids = getMiniFeedDataSrcIds( ids )
        return srcids

    # 得到源ID 
    srcids = __getMiniFeedDataSrcIds( minifeeds )

    # 更新到data节点
    for key, minifeed in minifeeds.iteritems() :
        if minifeed == None :
            continue
        
        if not getMiniFeedDataContent( key, minifeed, srcids ) :
            logger.error( 'getMiniFeedDataContent faild and throw, id=%s', key ) 
            minifeeds[key] = None

    return minifeeds

# 得到minifeed 中的data content
def getMiniFeedsDataContent_ForList ( minifeed_list ):
    logger.debug( 'getMiniFeedsDataContent_ForList...' )
    # 根据minifeed中的data节点里的id字段，得到数据源id
    def __getMiniFeedDataSrcIds ( minifeed_list ):
        ids = []
        # 找出没有resid字段的data里的id
        for minifeed in minifeed_list :
            for data in minifeed['data'] :
                if not isHasContentInMiniFeedData( data ) :
                    ids.append(data['id'])

        # 得到老的ID
        srcids = getMiniFeedDataSrcIds( ids )
        return srcids

    # 得到源ID 
    srcids = __getMiniFeedDataSrcIds( minifeed_list )

    # 更新到data节点
    for i in xrange( len(minifeed_list)-1, -1, -1 ):
        minifeed = minifeed_list[i]
        if not getMiniFeedDataContent( minifeed['feedId'], minifeed, srcids ) :
            logger.error( 'getMiniFeedDataContent faild and throw, id=%s', minifeed['feedId'] ) 
            del( minifeed_list[i] )

    return minifeed_list

# 从cache 获取feed 的详细内容
def getFeedContent_FromCache ( contId ):
    logger.debug( 'getFeedContent_FromCache, id=%s', contId )

    redis = db_cache.get_redis_feed_content()
    if redis == None: # error logging in db_cache
        return None

    key = contId + '_fc'
    content = redis.Get( key )
    if content == None or content == '' :
        logger.error( "getFeedContent_FromCache, key=%s, err=%d", key, redis.GetLastErrNo() )
        return None
        
    return content

# 保持feed 的详细内容到cache
def updateFeedContent_ToCache ( contId, content ):
    redis = db_cache.get_redis_feed_content()
    if redis == None: # error logging in db_cache
        return False

    key = contId + '_fc'
    if not redis.Set( key, content ) :
        logger.error( 'updateFeedContent_ToCache faild, key=%s, errno=%d', key, redis.GetLastErrNo() )
        return False
        
    return True

# 获取feed 的详细内容
def getFeedContent ( contId, nocache = False ):
    #首先从cache获取内容
    content = None
    if not nocache :
        content = getFeedContent_FromCache( contId )

    if content != None:
        try:
            return json.loads( content, strict=False )
        except:
            logger.error( 'getFeedContent, json load faild, id=%s, err=%s', contId, str(sys.exc_info()) )

    logger.debug( 'getFeedContent from third interface, id=%s', contId )

    # cache没有发现，则调用内容获取接口
    if isinstance( contId, unicode ):
        contId = contId.encode( 'utf8' )
    
    p = contId.find( '_' )
    if p < 0 :
        logger.error( "getFeedContent, id is invalid, id=%s", contId )
        return {}

    cat = contId[0:p]
    srcContId = contId[p+1:]

    status = 0
    msg = ''
    content = {}

    if cat == 'news':
        content = news_interface.getNewsContent( srcContId )
    elif cat == 'video' :
        (status,msg,content) = video_interface.video_interface( {'id':srcContId, 'info_type':2} )
    elif cat == 'music' :
        content = music_interface.Music_interface.Get_music_detail( srcContId )
    elif cat == 'story' :
        novel_reader_obj = novel_reader.NovelReader()
        (status,msg,content) = novel_reader_obj.fetch_novel_info( {'id':srcContId, 'info_type':1} )
        
    if content == None or len(content) == 0 :
        logger.error( "getFeedContent faild, id=%s", contId )
        return {}

    updateFeedContent_ToCache( contId, json.dumps(content) )
    return content
    
# 获取小说章节内容
def getStoryChapterContent ( contId ):
    # 章节内容有可能会有更新，所以我们本地不做缓存
    logger.debug( 'getStoryChapterContent from third interface, id=%s', contId )

    if isinstance( contId, unicode ):
        contId = contId.encode( 'utf8' )

    novel_reader_obj = novel_reader.NovelReader()
    (ret, content) = novel_reader_obj.get_chapter_content( contId )
    if ret != '2' :
        logger.error( "getStoryChapterContent faild, id=%s, err=%s", contId, ret )
        return ''
        
    return content

#######################################################################
# 以下为feed内容获取的通用接口。

# 从cache 获取feed 的详细内容信息等。
def getFeedInfo_FromCache ( key ):
    logger.debug( 'getFeedInfo_FromCache, key=%s', key )

    redis = db_cache.get_redis_feed_content()
    if redis == None: # error logging in db_cache
        return None

    key = key + '_fc'
    content = redis.Get( key )
    if content == None or content == '' :
        logger.error( "getFeedInfo_FromCache, key=%s, err=%d", key, redis.GetLastErrNo() )
        return None
        
    return content

# 保持feed 的详细内容到cache
def updateFeedInfo_ToCache ( key, content ):
    redis = db_cache.get_redis_feed_content()
    if redis == None: # error logging in db_cache
        return False

    key = key + '_fc'
    if not redis.Set( key, content ) :
        logger.error( 'updateFeedInfo_ToCache faild, key=%s, errno=%d', key, redis.GetLastErrNo() )
        return False
        
    return True

# 根据feed参数得到feed info的cache key
def getFeedInfoCacheKey( feedPars ):
    type = feedPars.get('type')
    id = feedPars.get('id')
    info_type = feedPars.get('info_type')
    key = str(type)+'_'+str(id)+'_'+str(info_type)
    return hashlib.new("md5", key).hexdigest()

# 获取feed 的详细内容
def getFeedInfo ( type, feedPars, nocache = False ):
    status = 0
    msg = ''
    content = None 

    #首先从cache获取内容
#    cache_key = getFeedInfoCacheKey( feedPars )
#    if not nocache :
#        content = getFeedInfo_FromCache( cache_key )

#    if content != None:
#        try:
#            return (0, '', json.loads( content, strict=False ))
#        except:
#            logger.error( 'getFeedInfo, json load faild, key=%s, feedPars=%s, err=%s', cache_key, str(feedPars), str(sys.exc_info()) )

    logger.debug( 'getFeedInfo from third interface, feedPars=%s', str(feedPars) )

    # cache没有发现，则调用内容获取接口
    if type == 'news':
        # 新闻不用做ID转换
        content = news_interface.getNewsContent( feedPars['id'] )
        if content == None or len(content) <=0 :
            (status,msg,content) =  ( -1, 'get new content faild', None )
    elif type == 'video' :
        # 视频不用做ID转换
        (status,msg,content) = video_interface.video_interface( feedPars )
#    elif type == 'music' :
        #(status,msg,content) = music_interface.Music_interface.Get_music_detail( srcContId )
#        pass
    elif type == 'story' :
        if str(feedPars['info_type']) != '2':
            # 需要取得源ID
            srcid = getMiniFeedDataSrcId( feedPars['id'] )
        else:
            srcid = feedPars['id']
        
        if srcid == None or srcid == '' :
            (status,msg,content) =  ( -1, 'id is invalid', None )
        else:
            feedPars['id'] = srcid
            novel_reader_obj = novel_reader.NovelReader()
            (status,msg,content) = novel_reader_obj.fetch_novel_info( feedPars )
    else:
        (status,msg,content) = ( -1,'input type invalid', None)
        
    if status == 0:
        pass
#        updateFeedInfo_ToCache( cache_key, json.dumps(content) )
    else:
        logger.error( 'getFeedInfo from third interface faild, msg=%s' % msg )

    return (status, msg, content)

if __name__ == '__main__':
    #print getFeedContent( 'music_130762' )
    #print getFeedContent( 'video_130762' )
    #print getFeedContent( 'novel_meta/.紫风铃./春天真的来了' )
    print getFeedContent( 'news_http://psv.tgbus.com/news/201303/20130326143520.shtml' )
