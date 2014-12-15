# coding:utf-8
import sys,os
import subprocess
import tempfile
from urllib import urlopen, quote
from xml.etree import ElementTree
import json
import traceback
import base64
from HTMLParser import HTMLParser
import re


NAME_MAP={
        'alias':('alias',''),           #别名
        'actors':('actor','guest'),          #演员
        'director':('director','dir'),        #导演（主持人）
        'area':('area','tv'),            #地区
        'time':('datetime','now_period'),            #上映/播放时间
        'length':('playlength',''),          #时长
        'state':('',''),           #0|连载中，1|已完结, 2|未知
        'rate':('scores',''),            #评分（没有评分）
        'tags':('vtag_str','tag'),            #标签
        'desc':('brief','brief'),            #简介
        'image':('pic_path','pic_path'),           #图片
        'totalNumber':('total_num',''),     #总剧集数
        'latestId':('',''),        #最近更新剧集Id,默认给0
        'latestName':('now_num','title'),      #最近更新剧集名称
        'latestTime':('datetime','now_period'),      #最近更新剧集时间
        'playUrl':('url','url'),             #播放地址
        'source':('c_type','c_type'),             #播放地址
        'favorite':('','')

}

def transform_html_text(html):
    html=html.strip()
    html=html.strip("\n")
    result=[]
    parse=HTMLParser()
    parse.handle_data=result.append
    parse.feed(html)
    parse.close()
    text = " ".join(result)
    text = text.replace('\n',' ')
    text = text.replace('\r',' ')
    text = text.replace('\t',' ')
    text = text.replace(u'　',' ')
    result, number = re.subn('  +', ' ', text)
    return result

def get_detail_dict(key):
    key_arr = key.split('_')
    vtype = key_arr[0]
    title = ''
    tag = 0
    if vtype == 'zongyi':
        if len(key_arr) < 2:
            print 'key format error'
            return {}
        tag = 1
        title = "_".join(key_arr[1:])
        url = 'http://www.yisou.com/json/get_android.php?&type=shipin_xiangqing&&q=%s&stype=zy' % quote(title)
        soure_url = 'http://m.v.yisou.com/wap/?q=%s&stype=zy' % quote(title)
    else:
        if len(key_arr) < 3:
            print 'key format error'
            return {}
        tag = 0
        title = "_".join(key_arr[2:])
        url = 'http://www.yisou.com/json/get_android.php?&type=shipin_xiangqing&&q=%s&id=%s' % (quote(title), key_arr[1])
        soure_url = 'http://m.v.yisou.com/wap/?q=%s&id=%s' % (quote(title), key_arr[1])
    json_str = urlopen(url).read()
    json_obj = None
    try:
        json_obj = json.loads(json_str.replace('\n', ''))
    except:
        print traceback.format_exc()
        return {}
    if json_obj['r'] == []:
        print 'http response from yisou  is []',key
        return {}
    detail_dict = {}
    detail_dict['id'] = base64.b64encode(key)
    detail_dict['type'] = vtype
    detail_dict['title'] = title.decode('utf8')
    
    for k, v in NAME_MAP.items():
        value = "" 
        if v[tag] != "" and json_obj['r'].has_key(v[tag]):
            value = json_obj['r'][v[tag]]
        detail_dict[k]=value
        
    if vtype == 'zongyi':
        detail_dict['state'] = '0' 
    elif vtype == 'dianying':
        detail_dict['state'] = '1' 
    else:
        if detail_dict['latestName'] != "" and detail_dict['totalNumber'] != "":
            if detail_dict['latestName'] == detail_dict['totalNumber']:
                detail_dict['state'] = 1 
            else:
                detail_dict['state'] = 0 
        else:
            detail_dict['state'] = 2 
            
    detail_dict['actors'] = detail_dict['actors'].replace(',',' ')
    detail_dict['director'] = detail_dict['director'].replace(',',' ')
    detail_dict['latestId'] = '0'
    detail_dict['sourceUrl'] = soure_url
    detail_dict['desc'] = transform_html_text(detail_dict['desc'])
    detail_dict['favorite'] = '1'
    
    if detail_dict['rate'] == '':
        detail_dict['rate'] = 0
    if float(detail_dict['rate']) > 9.9:
        detail_dict['rate'] = 9.9
    detail_dict['rate'] = '%.1f'%(float(detail_dict['rate'])/2)
    
    if vtype == 'zongyi':
        detail_dict['tags'] = detail_dict['tags'].replace('/',' ')
    else:
        detail_dict['tags'] = detail_dict['tags'].replace(',',' ')
        
    return detail_dict
    

if __name__ == "__main__":
    #input1:dianying_id_name
    #input2:zongyi_name
    for line in sys.stdin.readlines():
        print line.strip('\n')
        print json.dumps(get_detail_dict(line.strip('\n')), ensure_ascii=False).encode('utf8')
