#-*- coding: utf8 -*-
# created by hualai.deng , 2013-04-01
import sys
import os
import logging
import logging.config
import conf
import common.libredis as libredis
import common.mydb as mydb
import time

logger = logging.getLogger() 

#########################################################################
# global objects
#########################################################################
g_db = None
g_db_lct = 0 #记录DB上次连接的时间

g_redis_feed_list = None
g_redis_minifeed = None
g_redis_content = None
g_redis_req_recommend = None

#########################################################################
# get db connecting
#########################################################################
# get the db
def getdb ( ):
    global logger
    global g_db
    global g_db_lct

    ct = time.time()

    # 每5秒钟，重连一次DB
    if g_db != None and ct-g_db_lct <= 5 :
        return g_db

    try:
        g_db = None
        g_db = mydb.MyDB( conf.getConfig('db_net_assist') )
        g_db_lct = ct
        logger.debug( 'DB connect ok, [db_net_assist]' )
        return g_db
    except:
        logger.error( 'getdb[db_net_assist] faild, %s', str(sys.exc_info()) )
        g_db = None
        g_db_lct = 0
        return None
        
#########################################################################
# get cache connecting
#########################################################################
# get the cache for feed_list
def get_redis_feed_list ( ):
    global logger
    global g_redis_feed_list

    if g_redis_feed_list != None:
        return g_redis_feed_list

    try:
        g_redis_feed_list = libredis.libredis( conf.g_conf['redis_net_assist'], 'feed_list' )
        return g_redis_feed_list
    except:
        logger.error( 'get_redis_feed_list faild, %s', str(sys.exc_info()) )
        g_redis_feed_list = None
        return None
    
def get_redis_minifeed ( ):
    global logger
    global g_redis_minifeed

    if g_redis_minifeed != None:
        return g_redis_minifeed

    try:
        g_redis_minifeed = libredis.libredis( conf.g_conf['redis_net_assist'], 'minifeed' )
        return g_redis_minifeed
    except:
        logger.error( 'get_redis_minifeed faild, %s', str(sys.exc_info()) )
        g_redis_minifeed = None
        return None

def get_redis_feed_content ( ):
    global logger
    global g_redis_content

    if g_redis_content != None:
        return g_redis_content

    try:
        g_redis_content = libredis.libredis( conf.g_conf['redis_net_assist'], 'feed_content' )
        return g_redis_content
    except:
        logger.error( 'get_redis_content faild, %s', str(sys.exc_info()) )
        g_redis_content = None
        return None

def get_redis_req_recommend ( ):
    global logger
    global g_redis_req_recommend

    if g_redis_req_recommend != None:
        return g_redis_req_recommend

    try:
        g_redis_req_recommend = libredis.libredis( conf.g_conf['redis_net_assist'], 'req_recommend' )
        return g_redis_req_recommend
    except:
        logger.error( 'get_redis_content faild, %s', str(sys.exc_info()) )
        g_redis_req_recommend = None
        return None

########################################################################
# test
if __name__ == "__main__" :
    getdb()
