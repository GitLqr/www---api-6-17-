#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-16
import sys
import os
sys.path.append('.')

proto_path = '/usr/local/lib/python/alinow_backend_proto/'
if not proto_path in sys.path:
    sys.path.append(proto_path)

import logging
import model_connect
import cache_models
import db_models
import db_models_update
import model_interface
import cache_update_process
from data_def import DataDef
from common_pb2 import VisitInfo, UserFeatureList
import unittest
import log_conf

from db_cache_conf import DB_CACHE_CONF
#DB_CACHE_CONF.DATABASE_CONF['db_name'] = 'test_' + DB_CACHE_CONF.DATABASE_CONF['db_name']
#DB_CACHE_CONF.REDIS_CONF['addrs'] = '127.0.0.1:9900'
#DB_CACHE_CONF.REDIS_PY_CONF['port'] = 9900

db_conf = {
         'db_name': 'test_alinow_zhijun',
         'host': '10.250.12.84',
         'passwd': '',
         'user': 'root',
         'port': 3306,
         'charset': 'utf8'
    }

cache_conf = {
         'host':'127.0.0.1',
         'port':9900,
    }

model_interface.db_cache_init(db_conf, cache_conf)

def create_database():
    if not 'DATABASE_CONF' in dir(DB_CACHE_CONF):
        print 'db conf has not been inited.'
        return None

    database_name = DB_CACHE_CONF.DATABASE_CONF['db_name']
    #os.system('sh ./module/recommend/data_manage/sql_script/sql_script.sh %s' % database_name)
    os.system('sh ./sql_script/sql_script.sh %s' % database_name)

def drop_database():
    if not 'DATABASE_CONF' in dir(DB_CACHE_CONF):
        print 'db conf has not been inited.'
        return None

    database_name = DB_CACHE_CONF.DATABASE_CONF['db_name']
    cmd = "echo 'drop database %s' | mysql -uroot" % database_name
    os.system(cmd)

def start_redis():
    pass

def clear_redis():
    redis_py = model_connect.get_redis_py() 
    if None == redis_py:
        print 'ERROR, get redis py failed.'
    del_keys = redis_py.keys()
    pipe = redis_py.pipeline()
    for key in del_keys:
        pipe.delete(key)
    if False == pipe.execute():
        print 'ERROR pipeline execute failed.'

class TestModel(unittest.TestCase):

    def setUp(self):
        create_database()
        start_redis()

    def tearDown(self):
        clear_redis()
        drop_database()

    def test_db_redis(self):
        uid = '1234567'
        resource_type_list = ['music', 'news', 'movie']
        visit_info = VisitInfo()
        visit_info.pv_count = 5
        visit_info.click_count = 1
        visit_info.weight = 0.2
        visit_info_data = visit_info.SerializeToString()
        for resource_type in resource_type_list:
            self.assertEqual( True, cache_models.set_cache_online_user_resource_visitinfo(uid, resource_type, visit_info_data))
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = visit_info
        res = cache_models.get_cache_online_user_resource_visitinfo(uid, resource_type_list)
        real_res = {}
        self.assertEqual(True, res[0])
        for k, v in res[1].items():
            res_visit_info = VisitInfo()
            res_visit_info.ParseFromString(v)
            real_res[k] = res_visit_info
        self.assertEqual(prefer_res, real_res)

    def test_db_user_resource_visitinfo(self):
        uid = '1234567'
        resource_type_list = ['music', 'news', 'movie']
        visit_info = VisitInfo()
        visit_info.pv_count = 5
        visit_info.click_count = 1
        visit_info.weight = 0.2
        visit_info_data = visit_info.SerializeToString()
        for resource_type in resource_type_list:
            self.assertEqual( True, db_models_update.set_db_offline_user_resource_visitinfo(uid, resource_type, visit_info_data))
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = visit_info
        res = db_models.get_db_offline_user_resource_visitinfo(uid, resource_type_list)
        real_res = {}
        self.assertEqual(True, res[0])
        for k, v in res[1].items():
            res_visit_info = VisitInfo()
            res_visit_info.ParseFromString(v)
            real_res[k] = res_visit_info
        self.assertEqual(prefer_res, real_res)

    def test_db_user_feature_list(self):
        uid = '1234567'
        resource_type_list = ['novl', 'news']
        for resource_type in resource_type_list:
            self.assertEqual( True, db_models_update.set_db_offline_user_feature_list(uid, resource_type, uid+'_'+resource_type))
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = uid + '_' + resource_type
        res = db_models.get_db_offline_user_feature_list(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])
            
    def test_db_user_recommend_item_list(self):
        uid = '1234567'
        resource_type_list = ['novl']
        for resource_type in resource_type_list:
            self.assertEqual( True, db_models_update.set_db_offline_user_recommend_item_list(uid, resource_type, uid+'_'+resource_type))
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = uid + '_' + resource_type
        res = db_models.get_db_offline_user_recommend_item_list(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

    def test_db_item_recommend_item_list(self):
        itemid_list = ['novl123456', 'novl32435', 'novlerewqerq', 'novl432342234']
        resource_type = 'novl'
        prefer_res = {}
        for itemid in itemid_list:
            self.assertEqual( True, db_models_update.set_db_offline_item_recommend_item_list(itemid, resource_type, itemid+'_'+resource_type))
            prefer_res[itemid] = itemid+'_'+resource_type
        res = db_models.get_db_offline_item_recommend_item_list(itemid_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

    def test_db_item_features(self):
        itemid_list = ['novl123456', 'novl32435', 'novlerewqerq', 'novl432342234']
        resource_type = 'novl'
        prefer_res = {}
        for itemid in itemid_list:
            self.assertEqual( True, db_models_update.set_db_offline_item_features(itemid, resource_type, itemid+'_'+resource_type))
            prefer_res[itemid] = itemid+'_'+resource_type
        res = db_models.get_db_offline_item_features(itemid_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

    def test_db_feature_hot_item_list(self):
        feature_names = ['novlf1','novlf2','novlf3','novl香港']
        prefer_res = {}
        for feature_name in feature_names:
            prefer_res[feature_name] = 'data_%s' % feature_name
            self.assertEqual( True, db_models_update.set_db_offline_feature_hot_item_list(feature_name, DataDef.get_resource_type_from_feature_name(feature_name), prefer_res[feature_name]))
        res = db_models.get_db_offline_feature_hot_item_list(feature_names)
        #print 'prefer_res:%s' % prefer_res
        #print 'real_res:%s' % res[1]
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

    def test_db_global_hot_feature_list(self):
        resource_type_list = ['music', 'movie', 'novl']
        prefer_res = {}
        for resource_type in resource_type_list:
            self.assertEqual( True, db_models_update.set_db_offline_global_hot_feature_list(resource_type, 'hot_resource_'+resource_type))
            prefer_res[resource_type] = 'hot_resource_'+resource_type
        res = db_models.get_db_offline_global_hot_feature_list(resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

    def test_db_item_id_new_to_old(self):
        itemid_list = ['novl123456', 'novl32435', 'novlerewqerq', 'novl432342234']
        prefer_res = {}
        for itemid in itemid_list:
            self.assertEqual( True, db_models_update.set_db_offline_item_id_new_to_old(DataDef.get_resource_type_from_item_id(itemid), itemid, 'old_'+itemid))
            prefer_res[itemid] = 'old_'+itemid
        res = db_models.get_db_offline_item_id_new_to_old(itemid_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

    def test_interface_online_user_resource_visitinfo(self):
        uid = 'tiv_online_1'
        self.assertEqual(False, model_interface.set_online_user_resource_visitinfo(uid, 'music', None))
        resource_type_list = ['music', 'novl', 'movie']
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = 'tif_visitinfo_%s_%s' % (uid, resource_type)
            self.assertEqual(True, model_interface.set_online_user_resource_visitinfo(uid, resource_type, prefer_res[resource_type]))
        res = model_interface.get_online_user_resource_visitinfo(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        uid = 'tiv_offline_1'
        prefer_res = {}
        db_resource_type_list = ['music', 'novl', 'movie']
        for resource_type in db_resource_type_list:
            prefer_res[resource_type] = 'db_visitinfo_%s_%s' % (uid, resource_type)
            self.assertEqual(True, db_models_update.set_db_offline_user_resource_visitinfo(uid, resource_type, prefer_res[resource_type]))

        cache_resource_type_list = ['music']
        for resource_type in cache_resource_type_list:
            prefer_res[resource_type] = 'cache_visitinfo_%s_%s' % (uid, resource_type)
            self.assertEqual(True, cache_models.set_cache_offline_user_resource_visitinfo(uid, resource_type, prefer_res[resource_type]))
        res = model_interface.get_offline_user_resource_visitinfo(uid, resource_type_list + ['imag'])
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        res = cache_models.get_cache_offline_user_resource_visitinfo(uid, resource_type_list + ['imag'])
        #print 'perfer_res: %s' % prefer_res
        #print 'real_res: %s' % res[1]
        self.assertEqual(True, res[0])
        for k,v in res[1].items():
            if v == DataDef.CACHE_DEFAULT_NONE_VALUE:
                res[1].pop(k)
        self.assertEqual(prefer_res, res[1])



    def test_interface_user_feature_list(self):
        uid = 'tif_online_1'
        self.assertEqual(False, model_interface.set_online_user_feature_list(uid, 'music', None))
        resource_type_list = ['news', 'novl']
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = 'tif_%s_%s' % (uid, resource_type)
            self.assertEqual(True, model_interface.set_online_user_feature_list(uid, resource_type, prefer_res[resource_type]))
        res = model_interface.get_online_user_feature_list(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        uid = 'tif_offline_1'
        prefer_res = {}
        db_resource_type_list = ['news', 'novl']
        for resource_type in db_resource_type_list:
            prefer_res[resource_type] = 'tif_db_%s_%s' % (uid, resource_type)
            self.assertEqual(True, db_models_update.set_db_offline_user_feature_list(uid, resource_type, prefer_res[resource_type]))

        cache_resource_type_list = ['novl']
        for resource_type in cache_resource_type_list:
            prefer_res[resource_type] = 'cache_visitinfo_%s_%s' % (uid, resource_type)
            self.assertEqual(True, cache_models.set_cache_offline_user_feature_list(uid, resource_type, prefer_res[resource_type]))
        res = model_interface.get_offline_user_feature_list(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])
        res = cache_models.get_cache_offline_user_feature_list(uid, resource_type_list)
        self.assertEqual(True, res[0])
        for k,v in res[1].items():
            if v == DataDef.CACHE_DEFAULT_NONE_VALUE:
                res[1].pop(k)
        self.assertEqual(prefer_res, res[1])

    def test_interface_user_feature_reason(self):
        uid = 'tiufr_online_1'
        self.assertEqual(False, model_interface.set_online_user_feature_reason(uid, None))
        item_feature_list_data = '%s_feature_list_data' % uid
        self.assertEqual(True, model_interface.set_online_user_feature_reason(uid, item_feature_list_data))
        res = model_interface.get_online_user_feature_reason(uid)
        self.assertEqual(True, res[0])
        self.assertEqual(item_feature_list_data, res[1])

    def test_interface_user_favor_item_list(self):
        uid = 'tiufi_online_1'
        self.assertEqual(False, model_interface.set_online_user_favor_item_list(uid, 'news', None))
        resource_type_list = ['music', 'novl', 'news']
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = 'tifufi_%s_%s' % (resource_type, uid)
            self.assertEqual(True, model_interface.set_online_user_favor_item_list(uid, resource_type, prefer_res[resource_type]))
        res = model_interface.get_online_user_favor_item_list(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

    def test_interface_user_push_item_list(self):
        uid = 'tiupil_online_1'
        self.assertEqual(False, model_interface.set_online_user_push_item_list(uid, None))
        item_id_list_data = 'data_%s' % uid
        self.assertEqual(True, model_interface.set_online_user_push_item_list(uid, item_id_list_data))
        res = model_interface.get_online_user_push_item_list(uid)
        self.assertEqual(True, res[0])
        self.assertEqual(item_id_list_data, res[1])

    def test_interface_offline_item_recommend_item_list(self):
        db_itemid_list = ['showtioi_item_1', 'movitioi_item_2', 'carttioi_item_3', 'teletioi_item_4']
        self.assertEqual(False, cache_models.set_cache_offline_item_recommend_item_list('showtioi_item_1', None))
        prefer_res = {}
        for itemid in db_itemid_list:
            prefer_res[itemid] = 'data_db_%s' % itemid
            self.assertEqual(True, db_models_update.set_db_offline_item_recommend_item_list(itemid, DataDef.get_resource_type_from_item_id(itemid),  prefer_res[itemid]))
        cache_itemid_list = ['showtioi_item_1', 'movitioi_item_2', 'novltioi_item_5', 'novltioi_item_6']
        prefer_res = {}
        for itemid in db_itemid_list:
            prefer_res[itemid] = 'data_cache_%s' % itemid
            self.assertEqual(True, cache_models.set_cache_offline_item_recommend_item_list(itemid,  prefer_res[itemid]))

        itemid_list = ['showtioi_item_1', 'movitioi_item_2', 'carttioi_item_3', 'teletioi_item_4', 'novltioi_item_5', 'novltioi_item_6']
        res = model_interface.get_offline_item_recommend_item_list(itemid_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])
        res = cache_models.get_cache_offline_item_recommend_item_list(itemid_list)
        self.assertEqual(True, res[0])
        for k,v in res[1].items():
            if v == DataDef.CACHE_DEFAULT_NONE_VALUE:
                res[1].pop(k)
        self.assertEqual(prefer_res, res[1])

    def test_interface_offline_item_features(self):
        db_itemid_list = ['teletiof_item_1', 'teletiof_item_喜剧', 'carttiof_item_3', 'teletiof_item_4']
        self.assertEqual(False, cache_models.set_cache_offline_item_features('teletiof_item_1', None))
        prefer_res = {}
        for itemid in db_itemid_list:
            prefer_res[itemid] = 'data_db_%s' % itemid
            self.assertEqual(True, db_models_update.set_db_offline_item_features(itemid, DataDef.get_resource_type_from_item_id(itemid),  prefer_res[itemid]))
        cache_itemid_list = ['teletiof_item_1', 'teletiof_item_喜剧', 'carttiof_item_5', 'teletiof_item_6']
        prefer_res = {}
        for itemid in db_itemid_list:
            prefer_res[itemid] = 'data_cache_%s' % itemid
            self.assertEqual(True, cache_models.set_cache_offline_item_features(itemid,  prefer_res[itemid]))

        itemid_list = ['teletiof_item_1', 'teletiof_item_喜剧', 'carttiof_item_3', 'teletiof_item_4', 'carttiof_item_5', 'teletiof_item_6']
        res = model_interface.get_offline_item_features(itemid_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])
        res = cache_models.get_cache_offline_item_features(itemid_list)
        self.assertEqual(True, res[0])
        for k,v in res[1].items():
            if v == DataDef.CACHE_DEFAULT_NONE_VALUE:
                res[1].pop(k)
        self.assertEqual(prefer_res, res[1])

    def test_interface_feature_hot_item_list(self):
        db_featurename_list = ['carttifh_feature_name_香港', 'carttifh_feature_name_喜剧', 'carttifh_feature_name_3', 'carttifh_feature_name_4']
        self.assertEqual(False, cache_models.set_cache_offline_feature_hot_item_list('tifh_feature_name_1', None))
        prefer_res = {}
        for featurename in db_featurename_list:
            #featurename = unicode(featurename, 'utf8')
            prefer_res[featurename] = 'data_db_%s' % featurename
            self.assertEqual(True, db_models_update.set_db_offline_feature_hot_item_list(featurename, DataDef.get_resource_type_from_feature_name(featurename),  prefer_res[featurename]))
        cache_featurename_list = ['carttifh_feature_name_香港', 'carttifh_feature_name_喜剧', 'carttifh_feature_name_5', 'carttifh_feature_name_6']
        for featurename in cache_featurename_list:
            #featurename = unicode(featurename, 'utf8')
            prefer_res[featurename] = 'data_cache_%s' % featurename
            self.assertEqual(True, cache_models.set_cache_offline_feature_hot_item_list(featurename,  prefer_res[featurename]))
        featurename_list = ['carttifh_feature_name_香港', 'carttifh_feature_name_喜剧', 'carttifh_feature_name_3', 'carttifh_feature_name_4', 'carttifh_feature_name_5', 'carttifh_feature_name_6', 'nvoltifh_feature_name_7']
        res = model_interface.get_offline_feature_hot_item_list(featurename_list)
        #print 'prefer_res: %s' % prefer_res
        #print 'real_res: %s' % res[1]
        self.assertEqual(False, res[0])
        self.assertEqual(prefer_res, res[1])
        res = cache_models.get_cache_offline_feature_hot_item_list(featurename_list)
        #print 'prefer_res: %s' % prefer_res
        #print 'real_res: %s' % res[1]
        self.assertEqual(True, res[0])
        #for k,v in res[1].items():
        #    if v == DataDef.CACHE_DEFAULT_NONE_VALUE:
        #        res[1].pop(k)
        self.assertEqual(prefer_res, res[1])

    def test_interface_global_hot_feature_list(self):
        db_resource_type_list = ['music', 'novl', 'movie']
        self.assertEqual(False, cache_models.set_cache_offline_global_hot_feature_list('music', None))
        prefer_res = {}
        for resource_type in db_resource_type_list:
            prefer_res[resource_type] = 'tigh_db_data_%s' % resource_type
            self.assertEqual(True, db_models_update.set_db_offline_global_hot_feature_list(resource_type, prefer_res[resource_type]))
        cache_resource_type_list = ['music', 'news']
        for resource_type in cache_resource_type_list:
            prefer_res[resource_type] = 'tigh_cache_data_%s' % resource_type
            self.assertEqual(True, cache_models.set_cache_offline_global_hot_feature_list(resource_type, prefer_res[resource_type]))
        resource_type_list = ['music', 'novl', 'movie', 'news']
        res = model_interface.get_offline_global_hot_feature_list(resource_type_list)
        #print 'prefer_res: %s' % prefer_res
        #print 'real_res: %s' % res[1]
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])
        res = cache_models.get_cache_offline_global_hot_feature_list(resource_type_list)
        #print 'prefer_res: %s' % prefer_res
        #print 'real_res: %s' % res[1]
        self.assertEqual(True, res[0])
        for k,v in res[1].items():
            if v == DataDef.CACHE_DEFAULT_NONE_VALUE:
                res[1].pop(k)
        self.assertEqual(prefer_res, res[1])

    def test_interface_item_id_new_to_old(self):
        resource_type = 'novl'
        self.assertEqual(False, cache_models.set_cache_offline_item_id_new_to_old('novltiino_new_item_1', None))
        db_new_item_id_list = ['novltiino_item_1', 'novltiino_item_2', 'novltiino_item_3', 'novltiino_item_4']
        prefer_res = {}
        for item_id in db_new_item_id_list:
            prefer_res[item_id] = 'data_db_old_%s' % item_id
            self.assertEqual(True, db_models_update.set_db_offline_item_id_new_to_old(DataDef.get_resource_type_from_item_id(item_id), item_id, prefer_res[item_id]))
        cache_new_item_id_list = ['novltiino_item_1', 'novltiino_item_2', 'novltiino_item_5', 'novltiino_item_6']
        for item_id in cache_new_item_id_list:
            prefer_res[item_id] = 'data_cache_old_%s' % item_id
            self.assertEqual(True, cache_models.set_cache_offline_item_id_new_to_old(item_id, prefer_res[item_id]))
        new_item_id_list = ['novltiino_item_1', 'novltiino_item_2', 'novltiino_item_3', 'novltiino_item_4',  'novltiino_item_5', 'novltiino_item_6', 'novltiino_item_7']
        res = model_interface.get_offline_item_id_new_to_old(new_item_id_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])
        res = cache_models.get_cache_offline_item_id_new_to_old(new_item_id_list)
        self.assertEqual(True, res[0])
        for k,v in res[1].items():
            if v == DataDef.CACHE_DEFAULT_NONE_VALUE:
                res[1].pop(k)
        self.assertEqual(prefer_res, res[1])

    def test_update_user_resource_visitinfo(self):
        resource_type = 'novl'
        uid = 'urv_007'
        visitinfo_data = 'visit_%s_%s' % (resource_type, uid)
        self.assertEqual(True, cache_models.set_cache_online_user_resource_visitinfo(uid, resource_type, visitinfo_data))
        res = cache_models.get_cache_online_user_resource_visitinfo(uid, [resource_type])
        self.assertEqual(True, res[0])
        self.assertEqual({resource_type: visitinfo_data}, res[1])
        self.assertEqual(True, cache_update_process.cache_clear_online_user_resource_visitinfo())
        res = cache_models.get_cache_online_user_resource_visitinfo(uid, [resource_type])
        self.assertEqual(True, res[0])
        self.assertEqual({}, res[1])

        uid = 'urv_006'
        resource_type_list = ['novl', 'news', 'musc']
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = 'visit_%s_%s_cache' % (uid, resource_type)
            self.assertEqual( True, cache_models.set_cache_offline_user_resource_visitinfo(uid, resource_type, prefer_res[resource_type]))
        res = cache_models.get_cache_offline_user_resource_visitinfo(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        db_resource_type_list = ['novl', 'movi']
        update_prefer_res = {}
        for resource_type in db_resource_type_list:
            prefer_res[resource_type] = 'visit_%s_%s_db' % (uid, resource_type)
            update_prefer_res[resource_type] = 'visit_%s_%s_db' % (uid, resource_type)
            self.assertEqual( True, db_models_update.set_db_offline_user_resource_visitinfo(uid, resource_type, prefer_res[resource_type]))
        self.assertEqual(True, cache_update_process.cache_update_offline_user_resource_visitinfo(['novl', 'news', 'movi', 'musc']))
        res = cache_models.get_cache_offline_user_resource_visitinfo(uid, ['novl', 'news', 'movi', 'musc'])
        self.assertEqual(True, res[0])
        self.assertEqual(update_prefer_res, res[1])

    def test_update_user_resource_feature_list(self):
        resource_type = 'novl'
        uid = 'urv_007'
        features_data = 'features_%s_%s' % (resource_type, uid)
        self.assertEqual(True, cache_models.set_cache_online_user_feature_list(uid, resource_type, features_data))
        res = cache_models.get_cache_online_user_feature_list(uid, [resource_type])
        self.assertEqual(True, res[0])
        self.assertEqual({resource_type: features_data}, res[1])
        self.assertEqual(True, cache_update_process.cache_clear_online_user_feature_list())
        res = cache_models.get_cache_online_user_feature_list(uid, [resource_type])
        self.assertEqual(True, res[0])
        self.assertEqual({}, res[1])

        uid = 'urv_006'
        resource_type_list = ['novl']
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = 'features_%s_%s_cache' % (uid, resource_type)
            self.assertEqual( True, cache_models.set_cache_offline_user_feature_list(uid, resource_type, prefer_res[resource_type]))
        res = cache_models.get_cache_offline_user_feature_list(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        db_resource_type_list = ['novl', 'news']
        for resource_type in db_resource_type_list:
            prefer_res[resource_type] = 'features_%s_%s_db' % (uid, resource_type)
            self.assertEqual( True, db_models_update.set_db_offline_user_feature_list(uid, resource_type, prefer_res[resource_type]))
        self.assertEqual(True, cache_update_process.cache_update_offline_user_feature_list(['novl', 'news']))
        res = cache_models.get_cache_offline_user_feature_list(uid, ['novl', 'news'])
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

    def test_update_user_feature_reason(self):
        uid = 'urv_007'
        item_feature_list_data = 'item_feature_list_data_%s' % uid
        self.assertEqual(True, cache_models.set_cache_online_user_feature_reason(uid, item_feature_list_data))
        res = cache_models.get_cache_online_user_feature_reason(uid)
        self.assertEqual(True, res[0])
        self.assertEqual(item_feature_list_data, res[1])
        self.assertEqual(True, cache_update_process.cache_clear_online_user_feature_reason())
        res = cache_models.get_cache_online_user_feature_reason(uid)
        self.assertEqual(True, res[0])
        self.assertEqual(None, res[1])

    def test_update_user_favor_item_list(self):
        uid = 'urv_007'
        resource_type_list = ['novl', 'news']
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = 'favor_item_list_%s_%s' % (uid, resource_type)
            self.assertEqual(True, cache_models.set_cache_online_user_favor_item_list(uid, resource_type, prefer_res[resource_type]))
        res = cache_models.get_cache_online_user_favor_item_list(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])
        self.assertEqual(True, cache_update_process.cache_clear_online_user_favor_item_list())
        res = cache_models.get_cache_online_user_favor_item_list(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual({}, res[1])

    def test_update_user_recommend_item_list(self):
        uid = 'urv_006'
        resource_type_list = ['novl']
        prefer_res = {}
        for resource_type in resource_type_list:
            prefer_res[resource_type] = 'recommend_item_list_%s_%s_cache' % (uid, resource_type)
            self.assertEqual( True, cache_models.set_cache_offline_user_recommend_item_list(uid, resource_type, prefer_res[resource_type]))
        res = cache_models.get_cache_offline_user_recommend_item_list(uid, resource_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        db_resource_type_list = ['novl']
        for resource_type in db_resource_type_list:
            prefer_res[resource_type] = 'recommend_item_list_%s_%s_db' % (uid, resource_type)
            self.assertEqual( True, db_models_update.set_db_offline_user_recommend_item_list(uid, resource_type, prefer_res[resource_type]))
        self.assertEqual(True, cache_update_process.cache_update_offline_user_recommend_item_list(['novl']))
        res = cache_models.get_cache_offline_user_recommend_item_list(uid, ['novl'])
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

    def test_update_user_push_item_list(self):
        uid = 'urv_007'
        user_push_item_list_data = 'user_push_item_list_data_%s' % uid
        self.assertEqual(True, cache_models.set_cache_online_user_push_item_list(uid, user_push_item_list_data))
        res = cache_models.get_cache_online_user_push_item_list(uid)
        self.assertEqual(True, res[0])
        self.assertEqual(user_push_item_list_data, res[1])
        self.assertEqual(True, cache_update_process.cache_clear_online_user_push_item_list())
        res = cache_models.get_cache_online_user_push_item_list(uid)
        self.assertEqual(True, res[0])
        self.assertEqual(None, res[1])

    def test_update_item_recommend_item_list(self):
        item_id_list = ['novl1', 'novl2', 'novl3']
        prefer_res = {}
        for item_id in item_id_list:
            prefer_res[item_id] = 'recommend_item_id_%s_cache' % item_id
            self.assertEqual( True, cache_models.set_cache_offline_item_recommend_item_list(item_id, prefer_res[item_id]))
        res = cache_models.get_cache_offline_item_recommend_item_list(item_id_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        db_item_id_list = ['novl3', 'novl4', 'novl5']
        update_prefer_res = {}
        for item_id in db_item_id_list:
            update_prefer_res[item_id] = 'recommend_item_id_%s_db' % item_id
            self.assertEqual( True, db_models_update.set_db_offline_item_recommend_item_list(item_id, DataDef.get_resource_type_from_item_id(item_id), update_prefer_res[item_id]))
        self.assertEqual(True, cache_update_process.cache_update_offline_item_recommend_item_list(['novl']))
        res = cache_models.get_cache_offline_item_recommend_item_list(db_item_id_list)
        self.assertEqual(True, res[0])
        self.assertEqual(update_prefer_res, res[1])

    def test_update_item_features(self):
        item_id_list = ['novl1', 'novl2', 'novl3']
        prefer_res = {}
        for item_id in item_id_list:
            prefer_res[item_id] = 'features_%s_cache' % item_id
            self.assertEqual( True, cache_models.set_cache_offline_item_features(item_id, prefer_res[item_id]))
        res = cache_models.get_cache_offline_item_features(item_id_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        db_item_id_list = ['novl3', 'novl4', 'novl5']
        update_prefer_res = {}
        for item_id in db_item_id_list:
            update_prefer_res[item_id] = 'old_feature_%s_db' % item_id
            self.assertEqual( True, db_models_update.set_db_offline_item_features(item_id, DataDef.get_resource_type_from_item_id(item_id), update_prefer_res[item_id]))
        self.assertEqual(True, cache_update_process.cache_update_offline_item_features(['novl']))
        res = cache_models.get_cache_offline_item_features(db_item_id_list)
        self.assertEqual(True, res[0])
        self.assertEqual(update_prefer_res, res[1])

    def test_update_feature_hot_item_list(self):
        features = ['novl1', 'novl2', 'novl3']
        prefer_res = {}
        for feature in features:
            prefer_res[feature] = 'hot_item_list_%s_cache' % feature
            self.assertEqual( True, cache_models.set_cache_offline_feature_hot_item_list(feature, prefer_res[feature]))
        res = cache_models.get_cache_offline_feature_hot_item_list(features)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        db_features = ['novl3', 'novl4', 'novl5']
        update_prefer_res = {}
        for feature in db_features:
            update_prefer_res[feature] = 'hot_item_list_%s_db' % feature
            self.assertEqual( True, db_models_update.set_db_offline_feature_hot_item_list(feature, DataDef.get_resource_type_from_feature_name(feature), update_prefer_res[feature]))
        self.assertEqual(True, cache_update_process.cache_update_offline_feature_hot_item_list(['novl']))
        res = cache_models.get_cache_offline_feature_hot_item_list(db_features)
        self.assertEqual(True, res[0])
        self.assertEqual(update_prefer_res, res[1])

    def test_update_global_hot_feature_list(self):
        resourece_type_list = ['novl', 'news']
        prefer_res = {}
        for resource_type in resourece_type_list:
            prefer_res[resource_type] = 'hot_features_%s_cache' % resource_type
            self.assertEqual( True, cache_models.set_cache_offline_global_hot_feature_list(resource_type, prefer_res[resource_type]))
        res = cache_models.get_cache_offline_global_hot_feature_list(resourece_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        db_resourece_type_list = ['novl']
        update_prefer_res = {}
        for resource_type in db_resourece_type_list:
            update_prefer_res[resource_type] = 'hot_features_%s_db' % resource_type
            self.assertEqual( True, db_models_update.set_db_offline_global_hot_feature_list(resource_type, update_prefer_res[resource_type]))
        self.assertEqual(True, cache_update_process.cache_update_offline_global_hot_feature_list())
        res = cache_models.get_cache_offline_global_hot_feature_list(db_resourece_type_list)
        self.assertEqual(True, res[0])
        self.assertEqual(update_prefer_res, res[1])

    def test_update_item_id_new_to_old(self):
        new_item_id_list = ['novl1', 'novl2', 'novl3']
        prefer_res = {}
        for item_id in new_item_id_list:
            prefer_res[item_id] = 'old_item_id_%s_cache' % item_id
            self.assertEqual( True, cache_models.set_cache_offline_item_id_new_to_old(item_id, prefer_res[item_id]))
        res = cache_models.get_cache_offline_item_id_new_to_old(new_item_id_list)
        self.assertEqual(True, res[0])
        self.assertEqual(prefer_res, res[1])

        db_new_item_id_list = ['novl3', 'novl4', 'novl5']
        update_prefer_res = {}
        for item_id in db_new_item_id_list:
            update_prefer_res[item_id] = 'old_item_id_%s_db' % item_id
            self.assertEqual( True, db_models_update.set_db_offline_item_id_new_to_old(DataDef.get_resource_type_from_item_id(item_id),item_id, update_prefer_res[item_id]))
        self.assertEqual(True, cache_update_process.cache_update_offline_item_id_new_to_old(['novl']))
        res = cache_models.get_cache_offline_item_id_new_to_old(db_new_item_id_list)
        self.assertEqual(True, res[0])
        self.assertEqual(update_prefer_res, res[1])

    def test_cache_update_all_together(self):
        uid = 'db_uid'
        resource_type = 'movi'
        item_id = 'db_item_id'
        feature_name = 'db_feature_name'
        self.assertEqual(True, db_models_update.set_db_offline_user_resource_visitinfo(uid, resource_type, 'db_visit_info_data'))
        self.assertEqual(True, db_models_update.set_db_offline_user_feature_list(uid, resource_type, 'db_feature_list_data'))
        self.assertEqual(True, db_models_update.set_db_offline_user_recommend_item_list(uid, resource_type, 'db_user_recommend_item_list'))
        self.assertEqual(True, db_models_update.set_db_offline_item_features(item_id, resource_type, 'db_item_features_data'))
        self.assertEqual(True, db_models_update.set_db_offline_item_recommend_item_list(item_id, resource_type, 'db_item_id_list_data'))
        self.assertEqual(True, db_models_update.set_db_offline_feature_hot_item_list(feature_name, resource_type, 'db_hot_item_list_data'))
        self.assertEqual(True, db_models_update.set_db_offline_global_hot_feature_list(resource_type, 'db_hot_feature_list_data'))
        self.assertEqual(True, db_models_update.set_db_offline_item_id_new_to_old(resource_type, item_id, 'db_old_item_id_data'))

        cache_uid = 'cache_uid'
        cache_item_id = 'cache_item_id'
        cache_feature_name = 'cache_feature_name'
        self.assertEqual(True, cache_models.set_cache_online_user_resource_visitinfo(cache_uid, resource_type, 'on_cache_visit_info_data'))
        self.assertEqual(True, cache_models.set_cache_offline_user_resource_visitinfo(cache_uid, resource_type, 'cache_visit_info_data'))
        self.assertEqual(True, cache_models.set_cache_online_user_feature_list(cache_uid, resource_type, 'on_cache_feature_list_data'))
        self.assertEqual(True, cache_models.set_cache_offline_user_feature_list(cache_uid, resource_type, 'cache_feature_list_data'))
        self.assertEqual(True, cache_models.set_cache_online_user_feature_reason(cache_uid, 'cache_feature_list_data'))
        self.assertEqual(True, cache_models.set_cache_online_user_favor_item_list(cache_uid, resource_type, 'cache_item_id_list_data'))
        self.assertEqual(True, cache_models.set_cache_offline_user_recommend_item_list(cache_uid, resource_type, 'cache_feature_name_item_id_list_data'))
        self.assertEqual(True, cache_models.set_cache_online_user_push_item_list(cache_uid, 'cache_item_id_list_data'))
        self.assertEqual(True, cache_models.set_cache_offline_item_recommend_item_list(cache_item_id, 'cache_item_id_list_data'))
        self.assertEqual(True, cache_models.set_cache_offline_item_features(cache_item_id, 'cache_item_feature_list_data'))
        self.assertEqual(True, cache_models.set_cache_offline_feature_hot_item_list(cache_feature_name, 'cache_item_id_list_data'))
        self.assertEqual(True, cache_models.set_cache_offline_global_hot_feature_list(resource_type, 'cache_item_feature_list_data'))
        self.assertEqual(True, cache_models.set_cache_offline_item_id_new_to_old(cache_item_id, 'cache_old_item_id_data'))
        import cache_update_process
        all_resource_type_list = ['movi', 'news']
        common_resource_type_list = ['movi']
        self.assertEqual(True, cache_update_process.cache_update_all_together(all_resource_type_list, common_resource_type_list))
        self.assertEqual((True, {}), cache_models.get_cache_online_user_resource_visitinfo(cache_uid, [resource_type]))
        self.assertEqual((True, {resource_type:'db_visit_info_data'}), cache_models.get_cache_offline_user_resource_visitinfo(uid, [resource_type]))
        self.assertEqual((True, {}), cache_models.get_cache_online_user_feature_list(cache_uid, [resource_type]))
        self.assertEqual((True, {resource_type:'db_feature_list_data'}), cache_models.get_cache_offline_user_feature_list(uid, [resource_type]))
        self.assertEqual((True, None), cache_models.get_cache_online_user_feature_reason(cache_uid))
        self.assertEqual((True, {}), cache_models.get_cache_online_user_favor_item_list(cache_uid, [resource_type]))
        self.assertEqual((True, 'cache_item_id_list_data'), cache_models.get_cache_online_user_push_item_list(cache_uid))
        self.assertEqual((True,{resource_type:'db_user_recommend_item_list'}), cache_models.get_cache_offline_user_recommend_item_list(uid, [resource_type]))
        self.assertEqual((True,{item_id:'db_item_id_list_data'}), cache_models.get_cache_offline_item_recommend_item_list([item_id]))
        self.assertEqual((True,{item_id:'db_item_features_data'}), cache_models.get_cache_offline_item_features([item_id]))
        self.assertEqual((True,{feature_name:'db_hot_item_list_data'}), cache_models.get_cache_offline_feature_hot_item_list([feature_name]))
        self.assertEqual((True,{resource_type:'db_hot_feature_list_data'}), cache_models.get_cache_offline_global_hot_feature_list([resource_type]))
        self.assertEqual((True,{item_id:'db_old_item_id_data'}), cache_models.get_cache_offline_item_id_new_to_old([item_id]))

    def test_cache_update_control(self):
        from cache_update_controller import get_day_index, OfflineCacheStatus, run
        import datetime
        date_time = datetime.datetime.now()
        day_index = get_day_index(date_time)
        now_hour = date_time.hour
        ocs = OfflineCacheStatus()
        ocs.day_index = day_index
        ocs.db_update_time = datetime.datetime.now()
        ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_OFFLINE_READY
        ocs.save()
        run(now_hour + 1)
        ocs = OfflineCacheStatus.Get(day_index)
        self.assertEqual(OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_SUCCESS, ocs.status)
        self.assertEqual(1, ocs.try_times)
        self.assertEqual( True, ocs.delete())

        ocs = OfflineCacheStatus()
        ocs.day_index = day_index
        ocs.db_update_time = datetime.datetime.now()
        ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_FAIL
        ocs.save()
        run(now_hour + 1)
        ocs = OfflineCacheStatus.Get(day_index)
        self.assertEqual(OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_SUCCESS, ocs.status)
        self.assertEqual(1, ocs.try_times)
        self.assertEqual( True, ocs.delete())
    
        run(now_hour + 1)
        self.assertEqual(False,  OfflineCacheStatus.exists(day_index))
    
        ocs = OfflineCacheStatus()
        ocs.day_index = day_index
        ocs.db_update_time = datetime.datetime.now()
        ocs.try_times = 2
        ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_SUCCESS
        ocs.save()
        run(now_hour + 1)
        ocs = OfflineCacheStatus.Get(day_index)
        self.assertEqual(OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_SUCCESS, ocs.status)
        self.assertEqual(2, ocs.try_times)
        self.assertEqual(True, ocs.delete())
    
        ocs = OfflineCacheStatus()
        ocs.day_index = day_index
        ocs.db_update_time = datetime.datetime.now()
        ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_FAIL
        ocs.save()
        run(now_hour - 1)
        ocs = OfflineCacheStatus.Get(day_index)
        self.assertEqual(OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_SUCCESS, ocs.status)
        self.assertEqual(1, ocs.try_times)
        self.assertEqual( True, ocs.delete())
    
        ocs = OfflineCacheStatus()
        ocs.day_index = day_index
        ocs.db_update_time = datetime.datetime.now()
        ocs.status = OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_ONLY_FAIL
        ocs.save()
        run(now_hour - 1)
        ocs = OfflineCacheStatus.Get(day_index)
        self.assertEqual(OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_ONLY_SUCCESS, ocs.status)
        self.assertEqual(1, ocs.try_times)
        self.assertEqual( True, ocs.delete())
    
        run(now_hour - 1)
        ocs = OfflineCacheStatus.Get(day_index)
        self.assertEqual(OfflineCacheStatus.OFFLINE_UPDATE_STATUS_ONLINE_ONLY_SUCCESS, ocs.status)
        self.assertEqual(1, ocs.try_times)
        self.assertEqual( True, ocs.delete())
    
    def test_clear_online_cache_by_user(self):
        uid = 'test_clear_uid'
        resource_type = 'show'
        data = 'data'
        self.assertEqual(True, cache_models.set_cache_online_user_resource_visitinfo(uid, resource_type, data))
        self.assertEqual(True, cache_models.set_cache_online_user_feature_list(uid, resource_type, data))
        self.assertEqual(True, cache_models.set_cache_online_user_feature_reason(uid, data))
        self.assertEqual(True, cache_models.set_cache_online_user_favor_item_list(uid, resource_type, data))
        self.assertEqual(True, cache_models.set_cache_online_user_push_item_list(uid, data))
        self.assertEqual(True, cache_update_process.cache_clear_online_by_user(uid))
        self.assertEqual((True, {}), cache_models.get_cache_online_user_resource_visitinfo(uid, [resource_type]))
        self.assertEqual((True, {}), cache_models.get_cache_online_user_feature_list(uid, [resource_type]))
        self.assertEqual((True, None), cache_models.get_cache_online_user_feature_reason(uid))
        self.assertEqual((True, {}), cache_models.get_cache_online_user_favor_item_list(uid, [resource_type]))
        self.assertEqual((True, None), cache_models.get_cache_online_user_push_item_list(uid))

if __name__ == '__main__':
    unittest.main()
