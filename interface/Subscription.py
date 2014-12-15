#-*- coding: utf8 -*-
###############################################################
# @file Subscription.py
# @author dhldeng
# @version 1.0.0
# @date 2013-05-16
###############################################################
import sys
import web
import logging
import logging.config
import json
import conf
import db_cache
import chardet
import MySQLdb


# getLogger
logger = logging.getLogger() 
        
class clsSubscription:        
    def __init__ ( self ):
        logger.debug( self.__class__.__name__ + ' begin...' )
        web.header( 'Content-Type', 'text/html;charset=utf-8' )

    def __del__ ( self ):
        logger.debug( self.__class__.__name__ + ' end!' )

    def faildOutput ( self, err, msg ):
        output = {'status': err, 'msg' : msg}
        return  json.dumps( output, ensure_ascii=False )

    def getInput (self):
        try:
            inPars = web.input(user_id = '', feedid = '', resid='', op = '') 
            logger.debug( str(inPars) )
            self.uid = inPars.get('user_id').encode("utf8")
            self.feedid = inPars.get('feedid').encode("utf8")
            self.resid = inPars.get('resid').encode("utf8")
            self.op = inPars.get('op').encode("utf8")

            if self.uid == '' or \
                self.feedid == '' or \
                (self.op.lower() != 'add' and self.op.lower() != 'del' ) :
                logger.error( "input invalid" )
                return False
            
            return True
        except:
            logger.error( "input invalid, %s, %s" ,sys.exc_info()[0] , sys.exc_info()[1] )
            return False

    def addSubscription ( self ):
        # 插入记录到数据库
        db = db_cache.getdb()
        if db == None :
            return ( 1, 'db error' )
        
        try:
            sql ="INSERT INTO subscription(`user_id`, `feed_id`, `resource_id`, `last_modify_time`, `insert_time`) VALUES(%s, %s, %s, NOW(), NOW());"
            db.execute(sql, (self.uid, self.feedid, self.resid))
        except MySQLdb.Error,e:
            if e.args[0] != 1062 :
                logger.error( "insert subscription faild, %s, %s" ,sys.exc_info()[0] , sys.exc_info()[1] )
                return ( 2, 'insert record faild')

        # 清除cache
        redis = db_cache.get_redis_feed_list()
        if redis == None: # error logging in db_cache
            return ( 3, 'cache error' )

        redis.Del( self.uid+'_fid' )
        return ( 0, 'ok' )

    def delSubscription ( self ):
        # 删除记录到数据库
        db = db_cache.getdb()
        if db == None :
            return ( 1, 'db error' )
        
        try:
            sql ="DELETE FROM subscription where user_id=%s and feed_id=%s and resource_id=%s"
            db.execute(sql, (self.uid, self.feedid, self.resid))
        except:
            logger.error( "del subscription faild, %s, %s" ,sys.exc_info()[0] , sys.exc_info()[1] )
            return ( 2, 'delete record faild' )

        # 清除cache
        redis = db_cache.get_redis_feed_list()
        if redis == None: # error logging in db_cache
            return ( 3, 'cache error' )

        redis.Del( self.uid+'_fid' )
        return ( 0, 'ok' )
         
    def GET(self, *args):
        # get input params
        if not self.getInput():
            return self.faildOutput( -1, 'params invalid')
           
        status = 0
        msg = ''
        if (self.op.lower() == "add"):
            ( status, msg ) = self.addSubscription()

        elif (self.op.lower() == "del"):
            ( status, msg ) = self.delSubscription() 

        output = {}
        output['status'] = status 
        output['msg'] = msg
        output['data'] = self.feedid
        return  json.dumps(output)


