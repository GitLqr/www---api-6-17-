#-*- coding: utf8 -*-
import sys
import web
import logging
import logging.config
import json
import urllib2

# getLogger
logger = logging.getLogger() 

# 根据经纬度，得到周边影院放映信息
def getLocalTheater ( la, lo ):
    try:
        apiUrl = 'http://www.yisou.com/json/hotmovie/api.php?method=gethotmoviearound&latitude=%s&longitude=%s' % (la,lo)
        logger.debug( apiUrl )
        doc = urllib2.urlopen(apiUrl, timeout=3.0)
        content = json.load(doc, strict = False)
        if (content["code"] is not 0) or ("result" not in content):
            logger.error('open url [%s] failed' % apiUrl)
            return {}
        return content["result"]

    except:
        logger.error( str(sys.exc_info() ) )
        return {}
    
if __name__ == '__main__':
    print getLocalTheater( '39.9','116.39' )
