#-*- coding: utf8 -*-
# created by hualai.deng , 2013-04-15

from ctypes import *
import shutil
import os
import sys
import string 

#define
MUTLI_VALUE_SPEACTOR_CHAR = '\1\2'

#libredis dll
g_libredis_dll = None 
g_libredis_path = './lib/libredis_py.so'

#简化DB操作
class libredis:
    redis_handle = 0 
    charset = None

    def __init__ (self, redis_conf, redis_name):
        global g_libredis_dll
        self.loadLibRedisDll()
        self.redis_handle = g_libredis_dll.CreateRedisWrapper( c_char_p(redis_conf[redis_name]['addrs']), 
                                                               c_int(redis_conf[redis_name]['timeout']) ) ;
        self.charset = redis_conf[redis_name].get('charset')

    def __del__( self ):
        global g_libredis_dll
        if g_libredis_dll != None and self.redis_handle != 0 :
            g_libredis_dll.ReleaseRedisWrapper( c_long(self.redis_handle) ) ;
            self.redis_handle = 0

    def loadLibRedisDll ( self ):
        global g_libredis_dll
        global g_libredis_path
        if g_libredis_dll != None:
            return True

        try:
            g_libredis_dll = cdll.LoadLibrary(g_libredis_path)
            g_libredis_dll.GetLastErrNo.restype = c_int
            g_libredis_dll.GetErrMsg.restype = c_char_p
            g_libredis_dll.GetLastErrMsg.restype = c_char_p
            g_libredis_dll.CreateRedisWrapper.restype = c_long
            #g_libredis_dll.ReleaseRedisWrapper.restype = c_void
            g_libredis_dll.Del.restype = c_bool
            g_libredis_dll.Exists.restype = c_bool
            g_libredis_dll.Get.restype = c_char_p
            g_libredis_dll.Set.restype = c_bool
            g_libredis_dll.MGet.restype = c_char_p
            g_libredis_dll.RPush.restype = c_bool
            g_libredis_dll.RPop.restype = c_char_p
            g_libredis_dll.LLen.restype = c_int
            g_libredis_dll.LPush.restype = c_bool
            g_libredis_dll.LPop.restype = c_char_p
            g_libredis_dll.LRange.restype = c_char_p
            g_libredis_dll.LRem.restype = c_bool
            return True
        except:
            g_libredis_dll = None
            print "load redis lib faild" ,sys.exc_info()[0] , sys.exc_info()[1]
            return False

    def encode ( self, s ):
        if isinstance( s, unicode): 
            s = s.encode(self.charset)
        return s        
        
    def GetLastErrNo( self ) :
        global g_libredis_dll
        return g_libredis_dll.GetLastErrNo()

    def GetErrMsg( self, errNo ) :
        global g_libredis_dll
        return g_libredis_dll.GetErrMsg( c_int(errNo) )

    def GetLastErrMsg( self ) :
        global g_libredis_dll
        return g_libredis_dll.GetLastErrMsg()

    def Del( self, key ) :
        global g_libredis_dll
        return g_libredis_dll.Del( c_long(self.redis_handle), c_char_p(self.encode(key)) )

    def Exists( self, key ) :
        global g_libredis_dll
        return g_libredis_dll.Exists( c_long(self.redis_handle), c_char_p(self.encode(key)) )

    def Get( self, key ) :
        global g_libredis_dll
        return g_libredis_dll.Get( c_long(self.redis_handle), c_char_p(self.encode(key)) )
    
    def Set( self, key, value ) :
        global g_libredis_dll
        return g_libredis_dll.Set( c_long(self.redis_handle), c_char_p(self.encode(key)), c_char_p(self.encode(value)) )

    def MGet( self, keys ) :
        global g_libredis_dll
        if len(keys) <= 0 :
            return []
        
        strKeys = string.join( keys, MUTLI_VALUE_SPEACTOR_CHAR )
        strValues = g_libredis_dll.MGet( c_long(self.redis_handle), c_char_p(self.encode(strKeys)) )
        if strValues == None:
            return None
        
        return strValues.split( MUTLI_VALUE_SPEACTOR_CHAR )

    def MGet_X ( self, keys ):
        global g_libredis_dll
        if len(keys) <= 0 :
            return {}
        
        strKeys = string.join( keys, MUTLI_VALUE_SPEACTOR_CHAR )
        strValues = g_libredis_dll.MGet( c_long(self.redis_handle), c_char_p(self.encode(strKeys)) )
        if strValues == None:
            return None
        
        values = strValues.split( MUTLI_VALUE_SPEACTOR_CHAR )
        if len(keys) != len(values):
            return None

        result = {}
        index = 0 
        for key in keys:
            result[key] = values[index]
            index += 1
            
        return result        

    def RPush( self, key, values ) :
        global g_libredis_dll
        strValues = string.join( values, MUTLI_VALUE_SPEACTOR_CHAR )
        return g_libredis_dll.RPush( c_long(self.redis_handle), c_char_p(self.encode(key)), c_char_p(self.encode(strValues)) )

    def RPop( self, key ) :
        global g_libredis_dll
        return g_libredis_dll.RPop( c_long(self.redis_handle), c_char_p(self.encode(key)) )

    def LLen( self, key ) :
        global g_libredis_dll
        return g_libredis_dll.LLen( c_long(self.redis_handle), c_char_p(self.encode(key)) )

    def LPush( self, key, values ) :
        global g_libredis_dll
        strValues = string.join( values, MUTLI_VALUE_SPEACTOR_CHAR )
        return g_libredis_dll.LPush( c_long(self.redis_handle), c_char_p(self.encode(key)), c_char_p(self.encode(strValues)) )

    def LPop( self, key ) :
        global g_libredis_dll
        return g_libredis_dll.LPop( c_long(self.redis_handle), c_char_p(self.encode(key)) )

    def LRange( self, key, s, e ) :
        global g_libredis_dll
        strValues = g_libredis_dll.LRange( c_long(self.redis_handle), c_char_p(self.encode(key)), c_int(s), c_int(e) )
        if strValues == None:
            return None
            
        if strValues == "":
            return []
        
        return strValues.split( MUTLI_VALUE_SPEACTOR_CHAR )

    def LRem( self, key, value, count ) :
        global g_libredis_dll
        return g_libredis_dll.LRem( c_long(self.redis_handle), c_char_p(self.encode(key)), c_char_p(self.encode(value)), c_int(count) )

if __name__ == '__main__' :
    redis = libredis( {'redis': {'addrs':'127.0.0.1:8001', 'timeout':100} }, 'redis' )
    print redis.Get( "123" ) 
    print redis.GetLastErrNo()