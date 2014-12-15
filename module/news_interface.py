#-*- coding: utf8 -*-
import sys
import web
import logging
import logging.config
import json
import conf
import chardet
import urllib
import urllib2
import urlparse
import string
import time
import hashlib

# getLogger
logger = logging.getLogger() 

# 得到新闻的详细内容
def getNewsContent ( contId ):
    try:
        apiUrl = 'http://rss.reader.s.aliyun.com/wsgi/online_service_new/req?app=read&method=getArticle&_ran=0.60&topicid=1000&id=%s' % (contId)
        content = json.load(urllib2.urlopen(apiUrl))
        if content['status'] != "OK" :
            logger.error( 'getNewsContent faild, err=%s', content['status'] )
            return {}
        
        return content['data']

    except:
        logger.error( str(sys.exc_info() ) )
        return {}
 
# 根据topic的新闻列表    
def getNewsListFromRead( topicid, begin_time ):
    try:
        begin_time  = time.time() if int(begin_time) == 0 else begin_time
        apiUrl = 'http://rss.reader.s.aliyun.com/wsgi/online_service_new/req?app=read&method=getArticleList&topicid=%s&lastTime=%s'\
                 %\
                ( topicid, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(begin_time))) )

        logger.debug( apiUrl )
        res = json.load(urllib.urlopen(apiUrl), strict=False)
        logger.debug( str(res) )

        data = res['data']
        cardList = []
        firstUpdateTime = 10000000000
        lastUpdateTime = 0
        for i in xrange(len(data)):
            card = {}
            card["data"] = []
            cardData = {}
            cardData["url"] = data[i]["url"]
            cardData["title"] = data[i]["title"]
            cardData["favorite"] = 0
            cardData["source"] = data[i]["rss_name"]
            cardData["cid"] = topicid
            cardData["imageDataList"] = data[i]["logo_pic_url_list"]
            cardData["desc"] = data[i]["summary"]
            cardData["id"] = "news"+hashlib.new("md5",cardData["url"]).hexdigest()
            card["data"].append( cardData )
            card["layout"] = "single" if len(cardData["imageDataList"]) <= 0 else "singleRight1i"             
            card["title"] = ""
            card["type"] = "news"
            card["visibility"] = 3
            card["feed_type"] = "add"
            card["updateTime"] = int(time.mktime(time.strptime(data[i]["publishdate"], "%Y-%m-%d %H:%M:%S")))
            if firstUpdateTime > card["updateTime"]:
                firstUpdateTime = card["updateTime"]
            if lastUpdateTime < card["updateTime"]:
                lastUpdateTime = card["updateTime"]
            card["feedId"] = cardData["id"]
            cardList.append(card)
        return cardList, firstUpdateTime, lastUpdateTime
    except:
        logger.error( "Get news card list failed for topic id: %s", topicid )
        logger.error( str(sys.exc_info() ) )
        return [], 0, 0

if __name__ == '__main__':
    #print getFeedContent( 'music_130762' )
    #print getFeedContent( 'video_130762' )
    #print getFeedContent( 'novel_meta/.紫风铃./春天真的来了' )
    print getNewsContent( 'http://psv.tgbus.com/news/201303/20130326143520.shtml' )
