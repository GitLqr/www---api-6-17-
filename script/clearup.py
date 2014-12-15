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


if __name__ == '__main__' :
    if len(sys.argv) < 3 :
        print 'Please useage: db/cache betin_time [end_time]!'
        exit()

    if sys.argv[1] == '' or sys.argv[2] == ''  :
        print 'Please useage: db/cache betin_time [end_time]!'
        exit()

    if sys.argv[1].lower() != 'db' and  sys.argv[1].lower() != 'cache' :
        print 'Please useage: db/cache betin_time [end_time]!'
        exit()

    clearup_type = sys.argv[1]
    begin_time = sys.argv[2]
    end_time = ''
    if len(sys.argv) >= 4 :
        end_time = sys.argv[3]

    if end_time == '':
        end_time = '2000-01-01 00:00:00'

    print 'Clear up feeds of [%s]-[%s]' % (begin_time, end_time)

    # 得到feed列表
    db = db_cache.getdb()
    rs = db.query( 'select feed_id, update_time from feed where update_time<=\'%s\' and update_time>=\'%s\'' % (begin_time, end_time) )

    for rd in rs :
        print rd[1] , rd[0]

    print 'Feeds of [%s]-[%s], count=%d' % (begin_time, end_time, len(rs))
    print 'Make sure clear up [%s] of the feeds?' % clearup_type

    sure = raw_input()
    if sure.lower() != 'y':
        print 'exit'
        exit()        

    # 先删除DB数据
    if clearup_type.lower() == 'db':
        print 'Clear up db...'
        #先做个备份
        print 'insert into feed_bak select * from feed where update_time<=\'%s\' and update_time>=\'%s\'' % (begin_time, end_time)
        db.execute( 'delete from feed_bak where update_time<=\'%s\' and update_time>=\'%s\'' % (begin_time, end_time) )
        db.execute( 'insert into feed_bak select * from feed where update_time<=\'%s\' and update_time>=\'%s\'' % (begin_time, end_time) )
        print 'delete from feed where update_time<=\'%s\' and update_time>=\'%s\'' % (begin_time, end_time)
        db.execute( 'delete from feed where update_time<=\'%s\' and update_time>=\'%s\'' % (begin_time, end_time) )
        print 'Clear up db ok!'

    print 'Clear up cache...'
    redis = db_cache.get_redis_minifeed()
    for rd in rs:
        print 'del %s' % rd[0]+'_mfeed'
        redis.Del( rd[0]+'_mfeed' )
    print 'Clear up cache ok!'

