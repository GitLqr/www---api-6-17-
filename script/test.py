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

import xml.dom.minidom as minidom

strXml = '''
<Root><general_info></general_info><qp><search><spellcheck><![CDATA[]]></spellcheck><rw><![CDATA[]]></rw><isurl><![CDATA[]]></isurl><reprocess><![CDATA[]]></reprocess><HA2news><![CDATA[config=filtermode:21,start:0,hit:10,kvpairs:sl#0;tl#0;ip#10.249.0.1;st#wap;title_summary_conf#1`10`1<em>`1</em>`1...;body_summary_conf#1`10`1<em>`1</em>`1...;search_type#wap;query_type#0;reservation_include#yes;norm_query#女&&cluster=news_inc,news_rt&&distinct=dist_key:webnameid,dist_count:1&&filter=V_WAP_YAHOO!=1 AND dupcount=1 AND time>=1366110953 AND time<=1368702953&&sort=-time&&query=title:"女"]]></HA2news></search><tp>0</tp></qp><engine><TotalTime>0.009</TotalTime><hits totalhits="0" numhits="0"></hits><AggregateResults></AggregateResults><agg_error><news><phase1></phase1><phase2></phase2></news></agg_error><Errors><phase1><news></news></phase1><phase2></phase2></Errors><TraceResults><![CDATA[]]></TraceResults><qrs_ids><news><cluster_id>1</cluster_id><qrs_id>1</qrs_id></news></qrs_ids><cache><read>noaccess</read><update>noaccess</update></cache></engine><filter><query_fi>0</query_fi><query_cus></query_cus><filtered_doc_num>0</filtered_doc_num><query_filter><agg_error>Success</agg_error></query_filter><result_filter></result_filter></filter><sifter_count><delete>0</delete><demote>0</demote></sifter_count><time_cost><![CDATA[AppName [news], Query [女], time: [ 0.009],qp:[0.002],news:phase1[0.005],phase2[0.000],query filter:[0.002],result filter:[0.000],sifter:[0.000]]]></time_cost></Root>
'''
#print strXml 

#dom = minidom.parseString( strXml )
#print dom



#print c_char_p( 'dsfsdfsd' )
print urllib.quote( '杭州市' )
exit()

redis_minifeed = db_cache.get_redis_minifeed()
#x = redis_minifeed.LRange( '11111123', 0,100 )
#redis_minifeed.Del( 'all_user_front_page_feed_fid' )
x = redis_minifeed.Del( 'all_user_front_page_feed_fid' )
print str(x)
print redis_minifeed.GetLastErrNo()
exit()

    
#redis.LRange('123_fid', 0, -1)
#print redis.GetLastErrNo()

#print redis.LRange( 'all_user_front_page_feed_feed_id', 0, -1 )
#print redis.GetLastErrNo()

#redis.Del('story_玖兰格/花魅天下_fc')
#exit()

db = db_cache.getdb()
rs = db.query( 'select feed_id, jsonstr from feed' )

for rd in rs:
    print rd[0]
    #print rd[1] 
    #redis_minifeed.Set( rd[0]+'_mfeed', rd[1] )
    redis_minifeed.Del( rd[0]+'_mfeed' )
    print redis_minifeed.Get( rd[0]+'_mfeed' )


exit()
