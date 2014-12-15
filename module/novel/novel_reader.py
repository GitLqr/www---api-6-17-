#!/usr/bin/env python
#coding=utf8
import time,sys
from hashlib import sha1 as sha 
import hmac
import base64
try:
    import json
except ImportError:
    import simplejson as json
from oss.oss_api import *
from oss.oss_xml_handler import *
from novel_proto.novel_pb2 import *
from novel_proto.novel_body_pb2 import *
from novel_proto.novel_offline_meta_pb2 import *

HOST="oss.aliyuncs.com"
ACCESS_ID = "3qNc4LpnJokQZsKa"
SECRET_ACCESS_KEY = "o8PZGoGexfGpFA2tq5zigTlk7Qzt2A"
meta_bucket = 'test-novel-meta0'
offline_bucket = 'novel-offline-meta'
content_bucket = 'test-novel-content0'
image_ap = 'novel'
image_tv = '120_160'
#ACCESS_ID and SECRET_ACCESS_KEY 默认是空，请填入您申请的正确的ID和KEY.

class NovelReader:
    def __init__(self):
        if len(ACCESS_ID) == 0 or len(SECRET_ACCESS_KEY) == 0:
            print 'Please make sure ACCESS_ID and SECRET_ACCESS_KEY are correct!'
            exit(1)
        self.oss = OssAPI(HOST, ACCESS_ID, SECRET_ACCESS_KEY)
    
    def parse_id_range(self, length, url_dict):
        #超出range的会按实际range大小返回
        start_id = 0
        end_id = length
        if url_dict.has_key('p'):
            start_id = int(url_dict['p']) - 1
            end_id = start_id + 1
            if url_dict.has_key('n'):
                end_id = start_id + int(url_dict['n'])
        start_id = max(0, start_id)
        end_id = min(length, end_id)
        return (start_id, end_id)
    
    def read_novel_body(self, bucket, object):
        headers = {}
        res = self.oss.get_object(bucket, object, headers)
        if res.status / 100 == 2:
            body = res.read()
            print "%s %s read object SUCCESS" % (bucket, object)
            return body
        else:
            print "%s %s read object ERROR" % (bucket, object)
            return ""
        
    def get_lastest_chapter_info(self, novel_chapter):
        # the last chapter is the latest chapter
        length = len(novel_chapter)
        if length == 0:
            return ('', '', 0)
        latestName = novel_chapter[length - 1].main_chapter.chapter_name
        latestTime = novel_chapter[length - 1].main_chapter.update_time
        latestId = novel_chapter[length - 1].main_chapter.chapter_id
        return (latestName, latestId, latestTime)
                
    def translate_novel_comment(self, novel_comments, result, start_id, end_id): 
        total_comments = len(novel_comments)
        result['comments'] = {}
        result['comments']['total_comments'] = total_comments
        result['comments']['body'] = []
        for i in range(start_id, end_id):
            cmt = novel_comments[i]
            temp_cmt = {}
            temp_cmt['cmtId'] = str(id)
            temp_cmt['author'] = cmt.comment_author
            temp_cmt['time'] = cmt.comment_time
            temp_cmt['content'] = cmt.comment
            result['comments']['body'].append(temp_cmt)
    
    def translate_novel_meta(self, novel, result):
        novel_meta = novel.main_meta
        result['title'] = novel_meta.title
        result['author'] = novel_meta.author
        result['imageData'] = {}
        result['imageData']['default'] = {}
        result['imageData']['default']['url'] = self.transform_image_url(novel_meta.image_url)
        result['imageData']['default']['width'] = 120
        result['imageData']['default']['height'] = 160
        result['state'] = 0
        if novel_meta.finished == 1:
            result['state'] = 1
        result['category'] = novel_meta.first_category
        result['totalNumber'] = len(novel.chapters)
        #result['latestName'] = novel_meta.latest_chapter
        (result['latestName'], result['latestId'], result['latestTime']) = self.get_lastest_chapter_info(novel.chapters)
        result['wordNumber'] = novel_meta.word_num
        result['rate'] = novel_meta.point
        if novel_meta.HasField('point') == False or novel_meta.point == 0:
            result['rate'] = 3
        result['desc'] = novel_meta.introduction
        tags = []
        for keyword in novel_meta.keywords:
            tags.append(keyword)
        result['tags'] = ' '.join(tags)
        result['source'] = novel_meta.hostname
        result['sourceUrl'] = novel_meta.topic_url
        result['cmtNumber'] = novel_meta.comment_num
    
    def translate_novel_offline_info(self, novel_id, result):
        novel_id = 'offline/' + novel_id
        offline_info_str = self.read_novel_body(offline_bucket, novel_id)
        if offline_info_str != '':
            offline_proto = NovelOfflineMeta()
            offline_proto.ParseFromString(offline_info_str)
            result['favorite'] = int(offline_proto.click_count + 9999) / 10000
            
    def translate_novel_chapter(self, novel_chapter, result, start_id, end_id):
        print start_id, end_id
        length = len(novel_chapter)
        result['chapters'] = {}
        result['chapters']['total_chapters'] = length 
        result['chapters']['body'] = []
        for i in range(start_id, end_id): 
            mcpt = novel_chapter[i].main_chapter
            id = mcpt.chapter_id
            #print '==================='
            #print cpt
            temp_cpt = {}
            temp_cpt['title'] = mcpt.chapter_name
            temp_cpt['subId'] = id
            temp_cpt['contentKey'] = mcpt.body_key
            temp_cpt['pages'] = 0
            temp_cpt['sourceUrl'] = mcpt.url
            if mcpt.body_key != '':
                temp_cpt['pages'] = 1
            result['chapters']['body'].append(temp_cpt)
        #print result['chapters']['body']
        for idx in range(0, end_id - start_id):
            preContentKey = ""
            nxtContentKey = ""
            if idx != 0: 
                preContentKey = novel_chapter[idx - 1].main_chapter.body_key
            if idx != length - 1:
                nxtContentKey = novel_chapter[idx + 1].main_chapter.body_key
            result['chapters']['body'][idx]['preContentKey'] = preContentKey
            result['chapters']['body'][idx]['nxtContentKey'] = nxtContentKey
    
    def transform_image_url(self, image_url):
        keyStr = base64.urlsafe_b64encode(image_url)
        result_url = 'http://s2.zimgs.cn/ims?kt=url&at=' + image_ap + '&key=' + keyStr + '&sign='
        h = hmac.new('20121225@ims', keyStr, sha)
        signature = 'yx' + ':' + base64.urlsafe_b64encode(h.digest())
        result_url += (signature + '&tv=' + image_tv + '&x.jpg')
        return result_url
                                        
    
    def translate_novel_info(self, novel, info_type, url_dict):
        result = {}
        msg = 'success'
        status = 0
        result['id'] = novel.novel_id
        if (info_type & 1) != 0:
            self.translate_novel_meta(novel, result)
            
        if (info_type & 2) != 0:
            total_chapters = len(novel.chapters)
            (start_id, end_id) = self.parse_id_range(total_chapters, url_dict)
            if start_id < 0 or end_id > total_chapters:
                status = 1
                msg = 'Given novel chapter parameters are out of range!'
                result = {}
            else:
                self.translate_novel_chapter(novel.chapters, result, start_id, end_id)
            
        if (info_type & 4) != 0:
            total_comments = len(novel.main_meta.novel_comments)
            (start_id, end_id) = self.parse_id_range(total_comments, url_dict)
            if start_id < 0 or end_id > total_comments:
                status = 1
                msg = 'Given novel comment parameters are out of range!'
                result = {}
            else:
                self.translate_novel_comment(novel.main_meta.novel_comments, result, start_id, end_id)
            
        if (info_type & 8) != 0:
            self.translate_novel_offline_info(novel.novel_id, result)
            
        if (info_type & 16) != 0:
            total_chapters = len(novel.chapters)
            (start_id, end_id) = self.parse_id_range(total_chapters, url_dict)
            if start_id < 0 or end_id > total_chapters:
                status = 1
                msg = 'Given novel main body parameters are out of range!'
                result = {}
            else:
                temp_result = {}
                self.translate_novel_chapter(novel.chapters, temp_result, start_id, end_id)
                result['chapters_content'] = {}
                result['chapters_content']['total_chapters'] = total_chapters
                result['chapters_content']['body'] = []
                for i in range(start_id, end_id):
                    temp_chapter = temp_result['chapters']['body'][i]
                    temp_chapter.pop('subId')
                    temp_chapter.pop('pages')
                    content_key = novel.chapters[i].main_chapter.body_key
                    if content_key == '':
                        temp_chapter['content'] = ''
                    else:
                        (status, msg, content) = self.get_chapter_content(content_key)
                        if status == 0:
                            temp_chapter['content'] = content['content']
                        else:
                            temp_chapter['content'] = ''
                    result['chapters_content']['body'].append(temp_chapter)
            
        return (status, msg, result)
        
    def get_novels(self, id, info_type, url_dict):
        result = {}
        msg = 'success'
        status = 0
        meta_key = 'meta/' + id
        novel_body = self.read_novel_body(meta_bucket, meta_key)
        #print novel_body
        if novel_body != '':
            novel_proto = Novel()
            novel_proto.ParseFromString(novel_body)
            (status, msg, result) = self.translate_novel_info(novel_proto, info_type, url_dict)
        else:
            status = 2
            msg = 'read novel(%s) ERROR or novel_id(%s) is illegal' % (id, id)
        #print result
        return (status, msg, result)
    
    def get_chapter_content(self, content_key):
        # content is the chapter's content
        result = {}
        content_str = self.read_novel_body(content_bucket, content_key)
        if content_str == '':
            return (2, 'read novel content error or content_key is illegal!', result)
        else:
            novel_content_proto = Body()
            novel_content_proto.ParseFromString(content_str)
            content = novel_content_proto.text
            result['content'] = content
            return (0, 'success', result)        
        
    def fetch_novel_info(self, url_dict):
        #info type : 1  详情页
        #info type : 2  阅读页1
        #info type ：3  目录页
        #info type : 4  卡片页
        #info type : 5  评论页
        #info type : 6  阅读页2
        #key 为对应的 (详情页：novel_id) (阅读页：content_key) (目录页：novel_id) (卡片页：novel_id)
        info_type = url_dict['info_type']
        key = url_dict['id']
        result = {}
        msg = 'success'
        status = 0
        if(key == ''):
            return (1, 'Parameter id is empty!', result)
        if info_type == 1:
            (status, msg, result) = self.get_novels(key, 15, url_dict)
        elif info_type == 2:
            (status, msg, result) = self.get_chapter_content(key)
        elif info_type == 3:
            (status, msg, result) = self.get_novels(key, 2, url_dict)
        elif info_type == 4:
            (status, msg, result) = self.get_novels(key, 9, url_dict)
        elif info_type == 5:
            (status, msg, result) = self.get_novels(key, 4, url_dict)
        elif info_type == 6:
            (status, msg, result) = self.get_novels(key, 16, url_dict)
        else:
            status = 1
            msg = 'Parameter info_type must in range [1,6]!'
        return (status, msg, result)
    
    def list_all_novel_ids(self):
        prefix = ""
        marker = ""
        delimiter = "/" 
        maxkeys = "100"
        headers = {}
        res = self.oss.get_bucket(meta_bucket, prefix, marker, delimiter, maxkeys, headers)
        if (res.status / 100) == 2:
            body = res.read()
            h = GetBucketXml(body)
            (file_list, common_list) = h.list()
            print "object list is:"
            for i in file_list:
                print i
            print "common list is:"
            for i in common_list:
                print i
                    
