#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-16
import sys
sys.path.append('.')

import os
import logging
import common.libredis as libredis
import common.mydb as mydb
import time
from db_cache_conf import DB_CACHE_CONF
#import log_conf
import redis
import db_cache as out_db_cache

logger = logging.getLogger('recommend.data_manage') 

#########################################################################
# global objects
#########################################################################
g_db = None
g_db_lct = 0 #记录DB上次连接的时间

g_redis = None
g_redis_py = None

#########################################################################
# get db connecting
#########################################################################
def getdb():
    global g_db
    global g_db_lct

    ct = time.time()

    # 每5秒钟，重连一次DB
    if g_db != None and ct-g_db_lct <= DB_CACHE_CONF.DATABASE_RETRY_TIME :
        return g_db

    try:
        if not 'DATABASE_CONF' in dir(DB_CACHE_CONF):
            logger.error('db conf has not been inited.')
            return None
        g_db = None
        g_db = mydb.MyDB(DB_CACHE_CONF.DATABASE_CONF)
        g_db_lct = ct
        logger.debug( 'DB connect ok, conf[%s]' % DB_CACHE_CONF.DATABASE_CONF)
        return g_db
    except:
        logger.error( 'getdb[%s] failed, %s' %(DB_CACHE_CONF.DATABASE_CONF, str(sys.exc_info())) )
        g_db = None
        g_db_lct = 0
        return None
        
#########################################################################
# get cache connecting
#########################################################################
#def get_redis():
#    global g_redis
#    if g_redis != None:
#        return g_redis
#    try:
#        g_redis = libredis.libredis( {'redis_name': DB_CACHE_CONF.REDIS_CONF}, 'redis_name' )
#        logger.debug('get redis success, conf[%s]' % DB_CACHE_CONF.REDIS_CONF)
#        return g_redis
#    except:
#        logger.error( 'get_redis faild, %s' % str(sys.exc_info()) )
#        g_redis = None
#        return None
    #g_redis = out_db_cache.get_redis_req_recommend()
    #if None == g_redis:
    #    logger.error('ger redis failed.')
    #    return None
    #return g_redis
    
########################################################################

#########################################################################
# get redis py connecting
#########################################################################
def get_redis_py():
    global g_redis_py
    if None != g_redis_py:
        return g_redis_py
    try:
        if not 'REDIS_PY_CONF' in dir(DB_CACHE_CONF):
            logger.error('cache conf has not been inited.')
            return None
        g_redis_py = redis.StrictRedis(host=DB_CACHE_CONF.REDIS_PY_CONF['host'], port=DB_CACHE_CONF.REDIS_PY_CONF['port'], db=0)
        logger.debug('get redis py success.')
        return g_redis_py
    except:
        logger.error('get redis py failed, error:%s' % str(sys.exc_info()))
        return None
    
########################################################################
# test
# test
if __name__ == "__main__" :
    print 'get db: ' , getdb()
    print 'get redis: ', get_redis()
    
