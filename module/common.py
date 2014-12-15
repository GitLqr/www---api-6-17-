#-*- coding: utf8 -*-
import sys
import web
import logging
import logging.config
import json
import chardet
import urllib
import urllib2
import urlparse
import string
import conf

# getLogger
logger = logging.getLogger() 

# 根据经纬度，得到地理信息
def getCityName ( la, lo ):
    apiUrl = 'http://gc.ditu.aliyun.com/regeocoding?l=%s,%s&type=100' % (la,lo)
    logger.debug( 'getCityName begin, %s', apiUrl )
    try:
        content = json.load(urllib2.urlopen(apiUrl, timeout=2.0))
        addrName = content['addrList'][0]['admName']

        cityName = ''
        for name in addrName.split(',') :
            if name.endswith( '省' ) or name.endswith( '市' ):
                if cityName != '' :
                    cityName += ','
                cityName += name
            
        logger.debug( 'getCityName end..' )
        return cityName

    except:
        logger.error( "getCityName faild, url=%s, %s", apiUrl, str(sys.exc_info())  )
        return ""
    
if __name__ == '__main__':
    print getCityName( '39.9','116.39' )
