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
    json_obj = None
    try:
        json_str = urlopen(url).read()
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
            if value==None:
                value=""
        detail_dict[k]=value
    detail_url_host = 'http://10.230.230.49/getFeedInfo?'    
    if vtype == 'zongyi':
        detail_url=detail_url_host+'info_type=2&type=video&s_type=%s&classid=%s&push_type=%s&year=%s&id=%s&nocache=1'
        new_id=json_obj['r']['s_type']+'_'+json_obj['r']['classid']+'_'+json_obj['r']['push_type']
        detail_url=detail_url % (json_obj['r']['s_type'],json_obj['r']['classid'],json_obj['r']['push_type'],json_obj['r']['now_period'].split('-')[0],new_id)
    else:
        detail_url=detail_url_host+'info_type=2&type=video&s_type=%s&id=%s&push_type=%s&nocache=1'
        detail_url=detail_url%(str(json_obj['r']['s_type']),str(key_arr[1]),str(json_obj['r']['push_type'] ) )
    if vtype == 'dianying':
        detail_url = ''
    detail_dict['detailUrl'] = detail_url
        
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
    detail_dict['imageData'] = {'default':{'url':detail_dict['image'],'width':150,'height':202}}
    
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
    
def get_video_list(params):
    if params.get('s_type') is None:
        return {}
    if params.get('s_type') == '1':
        return {}
    
    if params['s_type'] == '4': #4 means zongyi
        if len(params) < 1+4:
            print 'key format error'
            return {}
        url = 'http://v.yisou.com/json/playurl.php?s_type=%s&classid=%s&push_type=%s&year=%s&month=&start=0' 
        url = url % (params['s_type'],params['classid'],params['push_type'],params['year'])
    else:
        if len(params) < 1+3:
            print 'key format error'
            return {}
        url = 'http://v.yisou.com/json/playurl.php?s_type=%s&id=%s&push_type=%s'
        url = url % (params['s_type'], params['id'],params['push_type'])
    json_obj = None
    try:
        json_str = urlopen(url).read()
        json_obj = json.loads(json_str.replace('\n', '').replace('});','}').replace('({','{') )
    except:
        print traceback.format_exc()
        return {}
    if json_obj['r'] == []:
        print 'http response from yisou  is []',key
        return {}
    data={}
    list = []
    data['data']=list
    if params['s_type'] == '4': #4 means zongyi
        for item in json_obj['r']['result']:
            new_item={}
            new_item['title']=item['title']
            new_item['episode']=item['period']
            new_item['playUrl']=item['playurl']
            new_item['image']=item['pic_path']
            list.append(new_item)
        return data
    
    if params['s_type'] != '4': #4 means zongyi
        for item in json_obj['r']['result']:
            for item2 in item:
                new_item={}
                new_item['title']=''
                new_item['episode']=str(item2['inx'])
                new_item['playUrl']=item2['url']
                new_item['image']=''
                list.append(new_item)
        return data

def video_interface(params):
    try:
        ret={}
        if str(params['info_type'])=='2':
            ret=get_video_list(params)
        if str(params['info_type'])=='1':
            ret=get_detail_dict(params['id']) 

        if ret=={}:
            return (11,'',{})
        else:
            return (0,'',ret)
    except:
        print traceback.format_exc()
        return (11,'except form video_interface',{})
        

if __name__ == "__main__":
    #input1:dianying_id_name
    #input2:zongyi_name
    for line in sys.stdin.readlines():
        if line[0]=='#':
            continue
        print line.strip('\n')
        params={} 
        for param in line.strip('\n').split('&'):
            params[param.split('=')[0]] = param.split('=')[1]
        card_dict=video_interface(params)
        if card_dict[0]!=0:
            continue
        print json.dumps(card_dict[2], ensure_ascii=False).encode('utf8')
        
        detail_url=card_dict[2]['detailUrl']
        if detail_url == '':
            continue
        print 'moses detail url',detail_url
        for param in detail_url.split('?')[1].split('&'):
            params[param.split('=')[0]] = param.split('=')[1]
        list_dict=video_interface(params)[2]
        print json.dumps(list_dict, ensure_ascii=False).encode('utf8')
