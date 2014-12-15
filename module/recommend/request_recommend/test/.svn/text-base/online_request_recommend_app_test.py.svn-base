# -*- coding: utf8 -*-
import sys
import logging
import unittest
sys.path.append('.')
from module.recommend.request_recommend.online_data_def import *
from module.recommend.request_recommend.online_request_recommend_app import *
sys.path.append('/usr/local/lib/python/')
from alinow_backend_proto.common_pb2 import VisitInfo,ItemFeature,UserFeature,ItemFeatureList,UserFeatureList
from alinow_backend_proto.item_pb2 import ItemIdList,FeatureNameItemIdList
from alinow_backend_proto.news_pb2 import FeatureNameLimit,FeatureNameLimitList,NewsItemFeatureInfo,NewsItemFeatureInfoList,NewsFeatureItemList

class OnlineRecommendTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        pass

    #TODO
    def test_merge_user_recent_feature(self):
        pass

    #TODO
    def test_get_request_recommend(self):
        errCode, reason2itemlist_dict = get_request_recommend(uid="uid", count=10)
        print errCode, reason2itemlist_dict
        pass

    #TODO
    def test_new_user_recommend(self):
        pass

    #TODO
    def test_old_user_recommend(self):
        pass

    #TODO
    def test_old_user_recommend_for_resource_type(self):
        pass

    #TODO
    def test_old_user_recommend_for_news_like(self):
        pass

    #TODO
    def test_old_user_recommend_for_item(self):
        pass

    #TODO
    def test_get_item_list_by_user(self):
        pass

    #TODO
    def test_get_item_list_by_user_feature(self):
        pass

    #TODO
    def test_get_item_list_by_item(self):
        pass

    #TODO
    def test_get_item_list_by_feature_list(self):
        pass

    #TODO
    def test_get_offline_user_feature_list(self):
        pass

    #TODO
    def test_get_recent_user_feature_list(self):
        pass

    #TODO
    def test_get_news_online_item_by_feature_list(self):
        pass

    #TODO
    def test_get_resource_hot_feature_list(self):
        pass

    #TODO
    def test_get_item_features(self):
        pass

    #TODO
    def test_get_item_features_for_news(self):
        pass

    #TODO
    def test_get_item_features_for_item(self):
        pass

    #TODO
    def test_update_user_info(self):
        pass

    def test_get_resource_type(self):
        self.assertEqual(get_resource_type("movixx"), "movi")

    def test_add_and_dedup_recommend_item(self):
        user_info = UserInfo("uid", logging)
        reason_item_list = {"movilike0000":[RecommendItem(item_id="movi0001"),
            RecommendItem(item_id="movi0002"), RecommendItem(item_id="movi0003")]}
        #empty result
        result = {}
        count = 2
        add_and_dedup_recommend_item(user_info, reason_item_list, result, count)
        self.assertEqual(result.keys(), ["movilike0000"])
        self.assertEqual(result["movilike0000"], [RecommendItem(item_id="movi0001"), RecommendItem(item_id="movi0002")])
        #TODO:existing reason
        #TODO:duplicated item id

    def test_get_resource_distribution_info(self):
        resource_distribution_info = get_resource_distribution_info(None, 5)
        self.assertEqual(resource_distribution_info,  {'news':3, 'movi':3})

    def test_filter_and_compose_recommend_item_list(self):
        uid = "1234"
        user_info = UserInfo(uid, logging)
        reason = "movitypevalue"
        item_id_list_proto = ItemIdList()
        result = {}
        item_id_list = ["movi0000", "movi0001", "movi0002", "movi0003", "movi0004"]
        #empty item_id_list_proto
        filter_and_compose_recommend_item_list(user_info, reason, item_id_list_proto, result)
        self.assertEqual(result, {})
        #all existing item_id_list_proto
        user_info.recent_push_item_id_list.add(item_id_list[0])
        user_info.recent_push_item_id_list.add(item_id_list[1])
        item_id_list_proto.item_id.append(item_id_list[0])
        item_id_list_proto.item_id.append(item_id_list[1])
        filter_and_compose_recommend_item_list(user_info, reason, item_id_list_proto, result)
        self.assertEqual(result, {})
        #partial existing item_id_list_proto
        user_info.recent_push_item_id_list.add(item_id_list[0])
        user_info.recent_push_item_id_list.add(item_id_list[1])
        item_id_list_proto.Clear()
        item_id_list_proto.item_id.append(item_id_list[0])
        item_id_list_proto.item_id.append(item_id_list[2])
        filter_and_compose_recommend_item_list(user_info, reason, item_id_list_proto, result)
        self.assertEqual(result, {reason:[RecommendItem(item_id=item_id_list[2])]})
        #existing reason, partial existing item_id_list_proto
        user_info.recent_push_feature_name_list.add(reason)
        result = {}
        filter_and_compose_recommend_item_list(user_info, reason, item_id_list_proto, result)
        self.assertEqual(result, {})

    def test_get_reason2itemlist_dict_size(self):
        data = {1:[2,3,4], 2:[3,4]}
        self.assertEqual(get_reason2itemlist_dict_size(data), 5)

    def test_get_filter_feature_list(self):
        pass

    def test_convert_user_feature_list(self):
        pass

if __name__ == '__main__':
    #errCode, reason2itemlist_dict = get_request_recommend(uid="uid", count=10)
    #sys.exit(1)
    errCode = merge_user_recent_feature({"uid":"uid2", "item_id":"moviDpJOzFLPtixGH_vf",
        "card_feature":"moviloca美国", "type":"click"})
    print errCode
    #errCode = merge_user_recent_feature({"uid":"uid", "item_id":"moviVNePB0YylmhZbhNZ",
    #    "card_feature":"moviloca美国", "type":"click"})
    #print errCode
    #print errCode, reason2itemlist_dict
    #OnlineRecommendTest().test_get_request_recommend()
    #unittest.main()
