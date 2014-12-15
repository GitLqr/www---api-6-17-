#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-24
import sys
sys.path.append('.')

import os
import logging
from data_def import DataDef
import model_connect
import cache_update_process
#import log_conf
#logger = logging.getLogger('alinow_data_manage.models')
logger = logging.getLogger('recommend.data_manage')

import model_interface

def db_cache_init(db_conf = None, cache_conf = None):
    if None != db_conf and None != cache_conf:
        model_interface.db_cache_init(db_conf = db_conf, cache_conf = cache_conf)
    elif None != cache_conf:
        model_interface.db_cache_init(cache_conf = cache_conf)
    elif None != db_conf:
        model_interface.db_cache_init(db_conf = db_conf)
    else:
        model_interface.db_cache_init()

def get_day_index(date_time):
    return date_time.strftime('%Y%m%d')

def get_day_index_online(date_time):
    return '%s_online' % get_day_index(date_time)

def get_day_index_offline(date_time):
    return '%s_offline' % get_day_index(date_time)

def date_to_string(date_time):
    return date_time.strftime('%Y-%m-%d %H:%M:%S')

class OfflineCacheStatus:
    def __init__(self):
        self.day_index = ''
        self.db_update_time = None
        self.status = ''
        self.try_times = 0
        self.cache_update_time = None
    
    @staticmethod
    def exists(day_index):
        sql = "select * from offline_update_status where day_index = '%s'" % day_index
        db = model_connect.getdb()
        if None == db:
            logger.error('get db connect error.')
            raise RuntimeError('get db connect error.')
        try:
            rs = db.query(sql)
            if 0 == len(rs):
                return False
            return True
        except:
            logger.error('OfflineCacheStatus.exists failed. error:%s' % str(sys.exc_info()))
            print str(sys.exc_info())
            raise RuntimeError('db query error.')

    def delete(self):
        if not OfflineCacheStatus.exists(self.day_index):
            return True
        sql = "delete from offline_update_status where day_index='%s'" % self.day_index
        db = model_connect.getdb()
        if None == db:
            logger.error('get db connect error.')
            raise RuntimeError('get db connect error.')
        try:
            if False == db.executeEx(sql):
                logger.error('do db execute error. sql:%s' % sql)
                return False
            return True
        except:
            logger.error('OfflineCacheStatus.delete failed. error:%s' % str(sys.exc_info()))
            print str(sys.exc_info())
            raise RuntimeError('db query error.')


    @staticmethod
    def Get(day_index):
        sql = "select day_index, db_update_time, status, try_times, cache_update_time from offline_update_status where day_index = '%s'" % day_index
        db = model_connect.getdb()
        if None == db:
            logger.error('get db connect error.')
            raise RuntimeError('get db connect error.') 
        try:
            rs = db.query(sql)
            if 0 == len(rs):
                return None
            ocs = OfflineCacheStatus()
            rd = rs[0]
            ocs.day_index = rd[0]
            ocs.db_update_time = rd[1]
            ocs.status = rd[2]
            ocs.try_times = rd[3]
            if None == ocs.try_times:
                ocs.try_times = 0
            ocs.cache_update_time = rd[4]
            return ocs
        except:
            logger.error('OfflineCacheStatus.load failed. error:%s' % str(sys.exc_info()))
            print str(sys.exc_info())
            raise RuntimeError('db query error.')
        return None

    def save(self):
        sql_list = []
        if not OfflineCacheStatus.exists(self.day_index):
            sql = "insert into offline_update_status(day_index) values('%s')" % self.day_index
            sql_list.append(sql)
        sql = "update offline_update_status set "
        if None != self.db_update_time:
            sql += "db_update_time = '%s'," % date_to_string(self.db_update_time)
        if '' != self.status:
            sql += "status = '%s'," % self.status
        sql += "try_times = %s," % self.try_times
        if None != self.cache_update_time:
            sql += "cache_update_time = '%s'," % date_to_string(self.cache_update_time)
        sql = sql[:-1] + " where day_index='%s'" % self.day_index
        sql_list.append(sql)
        db = model_connect.getdb()
        if None == db:
            logger.error('get db connect error.')
            raise RuntimeError('get db connect error.') 
        try:
            for sql in sql_list:
                #print 'sql: %s' % sql
                if False == db.executeEx(sql):
                    logger.error('do db execute error. sql:%s' % sql)
                    return False
            return True
        except:
            logger.error('OfflineCacheStatus.load failed. error:%s' % str(sys.exc_info()))
            print str(sys.exc_info())
            raise RuntimeError('db query error.')

    OFFLINE_UPDATE_STATUS_OFFLINE_READY = 'OFFLINE_READY'
    OFFLINE_UPDATE_STATUS_ONLINE_SUCCESS = 'ONLINE_SUCCESS'
    OFFLINE_UPDATE_STATUS_ONLINE_FAIL = 'ONLINE_FAILID'
    # 离线端数据未更新，仅做在线端的数据更新
    OFFLINE_UPDATE_STATUS_ONLINE_ONLY_SUCCESS = 'ONLY_ONLINE_SUC'
    OFFLINE_UPDATE_STATUS_ONLINE_ONLY_FAIL = 'ONLY_ONLINE_FAI'

def run(deadline_time):

    common_resource_type_list = ['movi', 'novl', 'tele', 'cart', 'show']
    all_resource_type_list = common_resource_type_list + ['news']

    import datetime
    date_time = datetime.datetime.now()
    day_index = get_day_index(date_time)
    now_hour = date_time.hour
    #是否落在3~5点
    print 'do cache update run, now_hour[%s] deadline_time[%s] at %s.' % (now_hour, deadline_time, date_time)
    if now_hour < deadline_time:
        if OfflineCacheStatus.exists(day_index):
            ocs = OfflineCacheStatus.Get(day_index)
            if None == ocs.status or OfflineCacheStatus.OFFLINE_UPDATE_STATUS_OFFLINE_READY == ocs.status or OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_FAIL == ocs.status:
                # do cache update
                # update to db
                if False == cache_update_process.cache_update_all_together(all_resource_type_list, common_resource_type_list):
                    ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_FAIL
                else:
                    ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_SUCCESS
                ocs.try_times += 1;
                ocs.cache_update_time = datetime.datetime.now()
                ocs.save()
                print 'update all cache together day_index[%s] status[%s], at %s.' % (day_index, ocs.status, date_time)
            else:
                print 'do nothing. day_index[%s] status[%s], at %s' % (day_index, ocs.status, date_time)
        else:
            print 'do nothing because offline data is null. at %s' % date_time
    elif now_hour >= deadline_time:
        if OfflineCacheStatus.exists(day_index):
            ocs = OfflineCacheStatus.Get(day_index)
        else:
            ocs = OfflineCacheStatus()
            ocs.day_index = day_index
            ocs.status = None
            ocs.try_times = 0
        # 如果离线端已近插入数据，但是由于更新失败，则重新更新
        if OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_FAIL == ocs.status:
            # do cache update
            # update to db
            if False == cache_update_process.cache_update_all_together(all_resource_type_list, common_resource_type_list):
                ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_FAIL
            else:
                ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_SUCCESS
            ocs.try_times += 1;
            ocs.cache_update_time = datetime.datetime.now()
            ocs.save()
            print 'update all cache together day_index[%s] status[%s], at %s.' % (day_index, ocs.status, date_time)
        # 仅进行online端更新 
        elif None == ocs.status or OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_ONLY_FAIL == ocs.status:
            # do online cache update
            if False == cache_update_process.cache_clear_online_user_feature_reason():
                ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_ONLY_FAIL
            else:
                ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_ONLY_SUCCESS
            ocs.try_times += 1;
            ocs.cache_update_time = datetime.datetime.now()
            ocs.save()
            print 'clear user feature reason only, day_index[%s] status[%s], at %s.' % (day_index, ocs.status, date_time)
        else:
            print 'do nothing. day_index[%s] status[%s], at %s' % (day_index, ocs.status, date_time)

if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print 'input error.' , 'cmd [deadline_time(1 ~ 23)]'
        sys.exit()
    import conf
    db_cache_init(conf.getConfig( 'db_recommend' ), conf.getConfig( 'cache_recommend' ))
    deadline_time = int(sys.argv[1])
    run(deadline_time)
    #import datetime
    #ocs = OfflineCacheStatus()
    #ocs.day_index = '20130525_online'
    #ocs.db_update_time = datetime.datetime.now()
    #ocs.cache_update_time = datetime.datetime.now()
    #ocs.save()
    #x = OfflineCacheStatus.Get('20130525_online')
    #print x.db_update_time
