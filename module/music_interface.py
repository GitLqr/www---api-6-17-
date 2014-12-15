#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

import os
import sys
sys.path.append('.')

import hashlib
import oauth2 as oauth
import time
import urllib
import logging
import json
import chardet
import datetime

from HTMLParser import HTMLParser
import re
reload(sys)
sys.setdefaultencoding("utf-8")

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
    text = text.replace('\t',' ')
    result, number = re.subn('  +', ' ', text)
    return result

class Xiami_interface_base:
    def __init__(self):
        self.API_KEY = 'ee65dd518951006e7cc89bd190e94fc9'
        self.API_SECRET = '76f2635f99d9a1be38118b8f41ce23cd'
        self.API_URI = 'http://api.xiami.com/api/'
        self.consumer = oauth.Consumer(key = self.API_KEY, secret=self.API_SECRET)
        self.client = oauth.Client(self.consumer, None)
        
    def Sig(self, params):
        res = ''
        key_list = []
        for k,v in params.items():
            key_list.append(k)
            key_list.sort()
        for key in key_list:
            res += key+str(params[key])
        res += self.API_SECRET
        return hashlib.md5(res).hexdigest()

    def Get_api(self, method, arrays):
        params = arrays
        params['api_key'] = self.API_KEY;
        params['method'] = method;
        params['call_id'] = time.time();
        params['api_sig'] = self.Sig(params);
        
        body = urllib.urlencode(params)
        url = "%s?%s" % (self.API_URI, body)
        ##logger.debug('get api, url: %s' % url)
        resp, content = self.client.request(url, "GET")
        return resp, content

class Xiami_interface:
    def __init__(self):
        self.interface_base = Xiami_interface_base()

    def Fetch(self, method, arrays):
        resp_str, content_str = self.interface_base.Get_api(method, arrays)
        try:
            content = json.loads(content_str.strip())
            if not content.has_key('status') or 'ok' != content['status'] or not content.has_key('data'):
                error_str = 'err'
                if content.has_key('err'):
                    error_str = content['err']
                #logger.error('get data failed; error: %s' % error_str)
                return None
            return content['data']
        except:
            #logger.error('json to dict error; content: %s' % (content_str))
            return None

    def Get_rank(self, type, item_id_index):
        #logger.debug('get %s rank' % type)
        arrays = {}
        arrays['type'] = type
        data_list = self.Fetch('Rank.getInfo', arrays);
        res = {}
        if None == data_list:
            #logger.error('Get %s rank, get data is null!' % type)
            return res
        for data in data_list:
            #print data
            if not isinstance(data, dict) or not data.has_key('lang'):
                #logger.info('get %s rank, has no attribute lang, %s' %(type, data))
                continue
            ind = Util.Encode_str(data['lang'])
            res[ind] = list()
            lst = data['list']
            for song_dct in lst:
                if not isinstance(song_dct, dict) or not song_dct.has_key(item_id_index):
                    #logger.info('get %s rank, has no attribute %s: %s' %(type, item_id_index, song_dct))
                    continue
                res[ind].append(song_dct[item_id_index])
        return res

    def Get_song_rank(self):
        return self.Get_rank('song', 'song_id')

    def Get_album_rank(self):
        return self.Get_rank('album', 'album_id')

    def Get_artist_rank(self):
        return self.Get_rank('artist', 'artist_id')

    def Get_item_rank(self, type):
        if 'song' == type:
            return self.Get_song_rank()
        elif 'album' == type:
            return self.Get_album_rank()
        elif 'artist' == type:
            return self.Get_artist_rank()

    def get_collects(self, tag):
        data = self.Fetch(tag, {})
        res = list()
        #print data
        if None == data or not isinstance(data, dict) or not data.has_key('collects'):
            #logger.error('get %s, get data is null' % tag)
            return res
        for collect in data['collects']:
            if not isinstance(collect, dict) or not collect.has_key('list_id'):
                #logger.info('get %s, has no attribute list_id: %s' % (tag, collect['list_id']))
                continue
            res.append(collect['list_id'])
        return res

    def Get_collects_orinew(self):
        return self.get_collects('Collects.orinew')

    def Get_collects_recommend(self):
        return self.get_collects('Collects.recommend')

    def Get_song_detail(self, song_id):
        data = self.Fetch('Songs.detail', {'id': song_id})
        #logger.debug('get song detail, id:%s' % song_id)
        #print data
        if None == data or not isinstance(data, dict) or not data.has_key('song'):
            #logger.error('get song detail, get data is null, id[%s]' % song_id)
            return None
        return data['song']

    def Get_album_detail(self, album_id):
        arrays = {}
        arrays['id'] = album_id
        data = self.Fetch('Albums.detail', arrays);
        #logger.debug('get album detail, id:%s' % album_id)
        #print data
        if None == data:
            #logger.error('get album detail, get data is null, album_id[%s]' % album_id)
            return None
        #data['songs'] = Extract_songs_id_list(data)
        return data

    def Get_artist_detail(self, artist_id):
        arrays = {}
        arrays['id'] = artist_id
        data = self.Fetch('Artists.detail', arrays);
        #logger.debug('get artist detail, id:%s' % artist_id)
        #print data
        if None == data:
            #logger.error('get artist detail, get data is null, artist_id[%s]' % artist_id)
            return None
        return data

    def Get_collect_detail(self, collect_id):
        arrays = {}
        arrays['id'] = collect_id
        data = self.Fetch('Collects.detail', arrays);
        #logger.debug('get collect detail, id:%s' % collect_id)
        #print data
        if None == data:
           #logger.error('get collect detail, get data is null, collect_id[%s]' % collect_id) 
           return None
        #data['songs'] = Extract_songs_id_list(data)
        return data

class Music_interface:

    xiami_interface = Xiami_interface()

    @staticmethod
    def Get_original_song_dct():
        song_info_dct = {}
        song_info_dct['id'] = ''
        song_info_dct['title'] = ''
        song_info_dct['image'] = ''
        song_info_dct['artist'] = ''
        song_info_dct['length'] = ''
        song_info_dct['rate'] = ''
        song_info_dct['popularity'] = ''
        song_info_dct['album'] = ''
        song_info_dct['company'] = ''
        song_info_dct['desc'] = ''
        song_info_dct['lyric'] = ''
        song_info_dct['publishTime'] = ''
        song_info_dct['sourceUrl'] = ''
        song_info_dct['playUrl'] = ''
        song_info_dct['source'] = unicode('虾米', 'utf8')
        song_info_dct['favorite'] = '1'
        return song_info_dct

    @staticmethod
    def Get_original_item_dct():
        item_dct = {}
        item_dct['id'] = ''
        item_dct['cid'] = ''
        item_dct['title'] = ''
        item_dct['image'] = ''
        item_dct['artist'] = ''
        item_dct['desc'] = ''
        item_dct['totalNumber'] = ''
        item_dct['type'] = ''
        item_dct['sourceUrl'] = ''
        item_dct['source'] = unicode('虾米', 'utf8')
        item_dct['favorite'] = '1'
        item_dct['lists'] = []
        return item_dct

    @staticmethod
    def Get_song_dct(song_id):
        song = Music_interface.xiami_interface.Get_song_detail(song_id)
        if None == song or not isinstance(song , dict):
            return None
        song_info_dct = Music_interface.Get_original_song_dct()
        if song.has_key('song_id'):
            song_info_dct['id'] = 'song_%s' % song['song_id']
            song_info_dct['sourceUrl'] = 'http://www.xiami.com/song/%s' % song['song_id']
        if song.has_key('song_name'):
            song_info_dct['title'] = transform_html_text(song['song_name'])
        if song.has_key('logo'):
            song_info_dct['image'] = song['logo']
        if song.has_key('artist_id'):
            artist = Music_interface.xiami_interface.Get_artist_detail(song['artist_id'])
            if None != artist and artist.has_key('artist_name'):
                song_info_dct['artist'] = artist['artist_name']
        if song.has_key('length'):
            song_info_dct['length'] = song['length']
        if song.has_key('album_id'):
            album = Music_interface.xiami_interface.Get_album_detail(song['album_id'])
            if None != album and album.has_key('album_name'):
                song_info_dct['album'] = album['album_name']
            if None != album and album.has_key('company'):
                song_info_dct['company'] = album['company']
            if None != album and album.has_key('publishtime'):
                song_info_dct['publishTime'] = album['publishtime']
        if song.has_key('lyric'):
            song_info_dct['lyric'] = song['lyric']
        if song.has_key('listen_file'):
            song_info_dct['playUrl'] = song['listen_file']
        if song.has_key('recommends'):
            try:
                song_info_dct['favorite'] = '%.1f' % (1 + float(song['recommends']) / 200)
            except:
                pass
        return song_info_dct

    @staticmethod
    def Transform_song_info(resource_song_dct):
        if None == resource_song_dct or not isinstance(resource_song_dct, dict):
            return None
        target_song_dct = Music_interface.Get_original_song_dct()
        if resource_song_dct.has_key('song_id'):
            target_song_dct['id'] = 'song_%s' % resource_song_dct['song_id']
            target_song_dct['sourceUrl'] = 'http://www.xiami.com/song/%s' % resource_song_dct['song_id']
        if resource_song_dct.has_key('song_name'):
            target_song_dct['title'] = transform_html_text(resource_song_dct['song_name'])
        if resource_song_dct.has_key('artist_name'):
            target_song_dct['artist'] = resource_song_dct['artist_name']
        if resource_song_dct.has_key('album_name'):
            target_song_dct['album'] = resource_song_dct['album_name']
        if resource_song_dct.has_key('length'):
            target_song_dct['length'] = resource_song_dct['length']
        if resource_song_dct.has_key('listen_file'):
            target_song_dct['playUrl'] = resource_song_dct['listen_file']
        if resource_song_dct.has_key('recommends'):
            try:
                target_song_dct['favorite'] = '%.1f' % (1 + float(resource_song_dct['recommends']) / 200)
            except:
                pass
        return target_song_dct
    
    @staticmethod
    def Extract_songs_info(resource_song_dct_list):
        song_list = list()
        MAX_SONG_NUM = 3
        song_num = 0
        for song_dct in resource_song_dct_list:
            if song_num >= MAX_SONG_NUM:
                continue
            if not isinstance(song_dct, dict) or not song_dct.has_key('song_id'):
                #logger.info('Transform_songs_list, has no attribute song_id: %s' % song_dct)
                continue
            target_song_dct = Music_interface.Transform_song_info(song_dct)
            if None == target_song_dct:
                continue
            song_list.append(target_song_dct)
            song_num += 1
        return song_list

    @staticmethod
    def Get_song_detail(song_id):
        song_info_dct = Music_interface.Get_original_item_dct()
        song = Music_interface.Get_song_dct(song_id)
        if None == song:
            return None
        song_info_dct['id'] = 'song_%s' % song_id
        song_info_dct['type'] = '0'
        song_info_dct['image'] = song['image']
        song_info_dct['totalNumber'] = '0'
        song_info_dct['lists'].append(song)
        return song_info_dct

    @staticmethod
    def Get_album_detail(album_id):
        album = Music_interface.xiami_interface.Get_album_detail(album_id)
        album_info_dct = Music_interface.Get_original_item_dct()
        if None == album or not isinstance(album, dict):
            return None
        album_info_dct['id'] = 'album_%s' % album_id
        album_info_dct['type'] = '2'
        if album.has_key('album_id'):
            album_info_dct['cid'] = album['album_id']
            album_info_dct['sourceUrl'] = 'http://www.xiami.com/album/%s' % album['album_id']
        if album.has_key('album_name'):
            album_info_dct['title'] = transform_html_text(album['album_name'])
        if album.has_key('logo'):
            album_info_dct['image'] = album['logo']
        if album.has_key('artist_name'):
            album_info_dct['artist'] = album['artist_name']
        if album.has_key('description'):
            album_info_dct['desc'] = transform_html_text(album['description'])
        if album.has_key('company'):
            album_info_dct['company'] = album['company']
        if album.has_key('recommends'):
            try:
                album_info_dct['favorite'] = '%.1f' % (1 + float(album['recommends']) / 100)
            except:
                pass
        #if album.has_key('song_count'):
        #    album_info_dct['totalNumber'] = album['song_count']
        if album.has_key('songs'):
            album_info_dct['lists'] = Music_interface.Extract_songs_info(album['songs'])
            if (None == album_info_dct['totalNumber'] or '' == album_info_dct['totalNumber'] or 0 == album_info_dct['totalNumber']) and isinstance(album['songs'], list):
                album_info_dct['totalNumber'] = str(len(album['songs']))
        return album_info_dct

    @staticmethod
    def Get_artist_detail(artist_id):
        artist = Music_interface.xiami_interface.Get_artist_detail(artist_id)
        artist_info_dct = Music_interface.Get_original_item_dct()
        if None == artist or not isinstance(artist, dict):
            return None
        artist_info_dct['id'] = 'artist_%s' % artist_id
        artist_info_dct['type'] = '1'
        if artist.has_key('artist_id'):
            artist_info_dct['cid'] = artist['artist_id']
            artist_info_dct['sourceUrl'] = 'http://www.xiami.com/artist/%s' % artist['artist_id']
        if artist.has_key('artist_name'):
            artist_info_dct['title'] = transform_html_text(artist['artist_name'])
        if artist.has_key('logo'):
            artist_info_dct['image'] = artist['logo']
        if artist.has_key('artist_name'):
            artist_info_dct['artist'] = artist['artist_name']
        if artist.has_key('description'):
            artist_info_dct['desc'] = transform_html_text(artist['description'])
        if artist.has_key('recommends'):
            try:
                artist_info_dct['favorite'] = '%.1f' % (1 + float(artist['recommends']) / 500)
            except:
                pass
        return artist_info_dct

    @staticmethod
    def Get_collect_detail(collect_id):
        collect = Music_interface.xiami_interface.Get_collect_detail(collect_id)
        collect_info_dct = Music_interface.Get_original_item_dct()
        if None == collect or not isinstance(collect, dict):
            return None
        collect_info_dct['id'] = 'collect_%s' % collect_id
        collect_info_dct['type'] = '3'
        if collect.has_key('list_id'):
            collect_info_dct['cid'] = collect['list_id']
            collect_info_dct['sourceUrl'] = 'http://www.xiami.com/song/showcollect/id/%s' % collect['list_id']
        if collect.has_key('collect_name'):
            collect_info_dct['title'] = transform_html_text(collect['collect_name'])
        if collect.has_key('logo'):
            collect_info_dct['image'] = collect['logo']
        if collect.has_key('user_name'):
            collect_info_dct['artist'] = collect['user_name']
        if collect.has_key('description'):
            collect_info_dct['desc'] = transform_html_text(collect['description'])
        #if collect.has_key('songs_count'):
        #    collect_info_dct['totalNumber'] = collect['songs_count']
        if collect.has_key('songs'):
            collect_info_dct['lists'] = Music_interface.Extract_songs_info(collect['songs'])
            if (None == collect_info_dct['totalNumber'] or '' == collect_info_dct['totalNumber'] or '0' == collect_info_dct['totalNumber']) and isinstance(collect['songs'], list):
                collect_info_dct['totalNumber'] = str(len(collect['songs']))
        if collect.has_key('favorites'):
            try:
                collect_info_dct['favorite'] = '%.1f' % (1 + float(collect['favorites']) / 50)
            except:
                pass
        return collect_info_dct

    @staticmethod
    def Get_ranksong_detail(ranksong_id, title):
        ranksong_dct = Music_interface.Get_original_item_dct()
        song_id_list = ranksong_id.strip().strip('&').split('&')
        #print song_id_list
        ranksong_dct['cid'] = ranksong_id
        ranksong_dct['id'] = '%s_%s' % ('ranksong', ranksong_id)
        ranksong_dct['type'] = '4'
        ranksong_dct['title'] = title
        for song_id in song_id_list:
            song = Music_interface.Get_song_dct(song_id)
            ranksong_dct['lists'].append(song)
        first_song = ranksong_dct['lists'][0]
        if None != first_song:
            ranksong_dct['image'] = first_song['image']
        ranksong_dct['totalNumber'] = str(len(ranksong_dct['lists']))
        return ranksong_dct

    @staticmethod
    def Get_music_detail(id):
        res = id.strip().split('_')
        if 3 != len(res):
            return None
        type = res[0]
        item_id = res[1]
        title = res[2]
        if 'song' == type:
            return Music_interface.Get_song_detail(item_id)
        elif 'album' == type:
            return Music_interface.Get_album_detail(item_id)
        elif 'artist' == type:
            return Music_interface.Get_artist_detail(item_id)
        elif 'collect' == type:
            return Music_interface.Get_collect_detail(item_id)
        elif 'ranksong' == type:
            return Music_interface.Get_ranksong_detail(item_id, title)
        return None

if __name__ == '__main__':
    print 'song detail:'
    print 'schedule start time:' , datetime.datetime.now()
    print Music_interface.Get_music_detail('song_130762_歌曲')
    print 'schedule end time:' , datetime.datetime.now()
    print ''
    print 'album detail:'
    print 'schedule start time:' , datetime.datetime.now()
    print Music_interface.Get_music_detail('album_961418276_专辑-华语专辑')
    print 'schedule end time:' , datetime.datetime.now()
    print ''
    print 'artist detail:'
    print 'schedule start time:' , datetime.datetime.now()
    print Music_interface.Get_music_detail('artist_55547_歌手')
    print 'schedule end time:' , datetime.datetime.now()
    print ''
    print 'collect detail'
    print 'schedule start time:' , datetime.datetime.now()
    print Music_interface.Get_music_detail('collect_18179853_精选集')
    print 'schedule end time:' , datetime.datetime.now()
    print 'ranksong detail'
    print 'schedule start time:' , datetime.datetime.now()
    print Music_interface.Get_music_detail('ranksong_1768995853&1771812713&1769819214&2079853&20526&_48小时热歌榜')
    print 'schedule end time:' , datetime.datetime.now()
