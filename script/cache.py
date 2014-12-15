#-*- coding: utf8 -*-
# created by hualai.deng , 2013-04-01
import sys
import os
import json
import chardet
import urllib
from ctypes import *
import time

# set coding to utf8
reload( sys )
sys.setdefaultencoding( "utf8" )
sys.path.append('../')

# the global config
import conf
import db_cache
import common.libredis as libredis
libredis.g_libredis_path = '../lib/libredis_py.so'

#conf.g_conf = conf.g_conf_test

if __name__ == '__main__' :
    if len(sys.argv) < 4 :
        print 'Please useage: cache_name [exist/get/set/del/LRange/LPush/LRem] key value!'
        exit()

    if sys.argv[1] == '' or sys.argv[2] == '' or sys.argv[3] == '' :
        print 'Please useage: cache_name [exist/get/set/del/LRange/LPush/LRem] key value!'
        exit()

    cache_name = sys.argv[1]
    op = sys.argv[2]
    key = sys.argv[3]
    redis = None

    try:
        redis = libredis.libredis( conf.g_conf['redis_net_assist'], cache_name )
    except:
        print 'get cache [%s] faild, %s' % ( cache_name, str(sys.exc_info()) )
        redis = None
        exit()

    bt = time.time()
    if op.lower() == 'exist' :
        ret = redis.Exists( key )
        print 'errno: ' + str(redis.GetLastErrNo())
        print 'result:' + str(ret)

    elif op.lower() == 'get' :
        ret = redis.Get( key )
        print 'errno: ' + str(redis.GetLastErrNo())
        print 'result:' + str(ret)

    elif op.lower() == 'set' :
        value = sys.argv[4]
        ret = redis.Set( key, value )
        print 'errno: ' + str(redis.GetLastErrNo())
        print 'result:' + str(ret)
        
    elif op.lower() == 'del' :
        ret = redis.Del( key )
        print 'errno: ' + str(redis.GetLastErrNo())
        print 'result:' + str(ret)
        

    elif op.lower() == 'llen' :
        ret = redis.LLen( key )
        print 'errno: ' + str(redis.GetLastErrNo())
        print 'result:' + str(ret)
        

    elif op.lower() == 'lrange' :
        s = int(sys.argv[4])
        c = int(sys.argv[5])
        ret = redis.LRange( key, s, c )
        print 'errno: ' + str(redis.GetLastErrNo())
        print 'result:' + str(ret)
        

    elif op.lower() == 'lpush' :
        value = json.loads( sys.argv[4], strict=False )
        ret = redis.LPush( key, value )
        print 'errno: ' + str(redis.GetLastErrNo())
        print 'result:' + str(ret)
        
    elif op.lower() == 'lrem' :
        value = sys.argv[4]
        c = int(sys.argv[5])
        ret = redis.LRem( key, value, c )
        print 'errno: ' + str(redis.GetLastErrNo())
        print 'result:' + str(ret)
        
    else:
        print 'invalid op!'

    et = time.time()
    print 'spent: ' + str(et-bt)
