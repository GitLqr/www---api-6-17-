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

# 得到离线推过来的从0点到现在所有头条新闻
def getTodayHotFromOffline():

def getRecomNews(reason):

def getNewsListFromRead( paras ):
    try:
        apiUrl = 'http://rss.reader.s.aliyun.com/wsgi/online_service_new/req?app=read&method=getArticleList&topicid=%s&lastTime=%s' % ( paras['cid'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(paras['begin_time']))))
        res = json.load(urllib.urlopen(apiUrl), strict=False)
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
            cardData["source" = data[i]["rss_name"]
            cardData["cid"] = paras["cid"]
            cardData["imageDataList"] = data[i]["logo_pic_url_list"]
            cardData["desc"] = data[i]["summary"]
            cardData["id"] = news+hashlib.new("md5",itemids).hexdigest()
            card["data"].append( cardData )
            card["layout"] = "single"
            card["title"] = ""
            card["type"] = "news"
            card["visibility"] = 3
            card["feed_type"] = "add"
            card["updateTime"] = int(time.mktime(time.strptime(data[i]["publishdate"]), "%Y-%m-%d %H:%M:%S"))
            if firstUpdateTime > card["updateTime"]:
                firstUpdateTime = card["updateTime"]
            if lastUpdateTime < card["updateTime"]:
                lastUpdateTime = card["updateTime"]
            card["feedId"] = cardData["id"]
            cardList.append(card)
        return cardList, firstUpdateTime, lastUpdateTime
    except:
        logger.error( "Get news card list failed for topic id: %s", paras["cid"])
        logger.error( str(sys.exc_info() ) )
        return [], 0, 0

def vadilatePara( paras ):
    if 'cid' not in paras or 'begin_time' not in paras or 'before' not in paras:
        return False
    #本地
    if paras['cid'] == '0' and 'area' not in paras:
        return False
    #推荐
    if paras['cid'] == '500002' and 'reason' not in paras:
        return False

# 得到新闻的频道列表
def getNewsCards ( paras ):
    try:
        if paras['cid'] == '500001':
            return getTodayHotFromOffline()
        elif paras['cid'] == '500002':
            return getRecomNews(paras['reason'])
        else:
            return getNewsListFromRead( paras )
        
    except:
        logger.error( str(sys.exc_info() ) )
        return [],0,0
    
if __name__ == '__main__':
    print getNewsCards( {'cid':'676', 'begin_time':'1369970042','before':0 )
