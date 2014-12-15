#-*- coding: utf8 -*-
# created by hualai.deng , 2013-04-01
import sys
import os

##########################################################################
# the global config
g_conf = { 
    'user_db': {
        "host": "10.250.12.85", 
        "db_name": "recom_test", 
        "user": "root",
        "passwd": "", 
        "port": 3306,
        "charset":"utf8"
    } ,
    'fea_db': {
        "host": "flamingo3241.mysql.rds.aliyuncs.com", 
        "db_name": "flamingo", 
        "user": "root",
        "passwd": "LmIa2Hp3P", 
        "port": 3241,
        "charset":"utf8"
    } ,
    'recom_default_tag' : ['newsctgy财经', 'newsctgy科技', 'newsctgy国内', 'newsctgy趣味', 'newsctgy体育', 'newsctgy生活', 'newsctgy娱乐', 'newsctgy汽车', 'newsctgy文史', 'newsctgy时尚', 'newsctgy游戏', 'newsctgy社会', 'newsctgy国际', 'newsctgy军事', 'newsctgy美>图', 'newsctgy房产', 'newsctgy女人'],
    'redis_net_assist':
    {
        'feed_list': {
            "addrs": "10.230.230.49:6379",
            "timeout" : 100,
            "charset": "utf8"
         },
        'minifeed': {
            "addrs": "10.230.230.49:6379",
            "timeout" : 100,
            "charset": "utf8"
         },
        'feed_content': {
            "addrs": "10.230.230.49:6379",
            "timeout" : 100,
            "charset": "utf8"
         },
        'req_recommend':{
            "addrs": "10.230.230.49:6370",
            "timeout" : 100,
            "charset": "utf8"
         },
        'others': {
            "addrs": "10.230.230.49:6379",
            "timeout" : 100,
            "charset": "utf8"
         }
     },
     'db_recommend': {
         'db_name': 'alinow_zhijun',
         'host': '10.250.12.84',
         'passwd': '',
         'user': 'root',
         'port': 3306,
         'charset': 'utf8'
     },
     'cache_recommend': {
         'host':'10.250.12.84',
         'port':6379
     },
}

g_conf_test = { 
    'db_net_assist': {
        "host": "127.0.0.1", 
        "db_name": "assist_duhui", 
        "user": "root",
        "passwd": "", 
        "port": 3306,
        "charset":"utf8"
    } ,

    'redis_net_assist':
    {
        'feed_list': {
            "addrs": "10.230.230.49:6381",
            "timeout" : 100,
            "charset": "utf8"
         },
        'location_feed_list': {
            "addrs": "10.230.230.49:6381",
            "timeout" : 100,
            "charset": "utf8"
         },
        'minifeed': {
            "addrs": "10.230.230.49:6381",
            "timeout" : 100,
            "charset": "utf8"
         },
        'feed_content': {
            "addrs": "10.230.230.49:6381",
            "timeout" : 100,
            "charset": "utf8"
         },
        'req_recommend':{
            "addrs": "10.230.230.49:6370",
            "timeout" : 100,
            "charset": "utf8"
         },
        'others': {
            "addrs": "10.230.230.49:6381",
            "timeout" : 100,
            "charset": "utf8"
         }
     },
     'db_recommend': {
         'db_name': 'alinow_zhijun',
         'host': '10.250.12.84',
         'passwd': '',
         'user': 'root',
         'port': 3306,
         'charset': 'utf8'
     },
     'cache_recommend': {
         'host':'10.250.12.84',
         'port':6379
     },
}

#########################################################################
# methods
#########################################################################
# get the config object
def getConfig ( key = None ):
    global g_conf
    if key == None:
        return g_conf
    return g_conf.get( key )    
    

########################################################################
# test
if __name__ == "__main__" :
    print str(g_conf)
    print str(g_conf_test)
