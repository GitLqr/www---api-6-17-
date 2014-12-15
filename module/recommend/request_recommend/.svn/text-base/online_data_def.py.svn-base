#!/usr/bin/env python
# -*- coding: utf8 -*-
import traceback
import sys
sys.path.append('/usr/local/lib/python/')
sys.path.append('.')
from alinow_backend_proto.common_pb2 import VisitInfo,ItemFeature,UserFeature,ItemFeatureList,UserFeatureList
from alinow_backend_proto.item_pb2 import ItemIdList,FeatureNameItemIdList
from alinow_backend_proto.news_pb2 import FeatureNameLimit,FeatureNameLimitList,NewsItemFeatureInfo,NewsItemFeatureInfoList,NewsFeatureItemList
import module.recommend.data_manage.model_interface as model
import module.recommend.request_recommend
from module.recommend.request_recommend.util import is_valid_data

class ResourceType:
    RESOURCE_TYPE_LENTH = 4
    RESOURCE_TYPE_NEWS = u"news"
    RESOURCE_TYPE_MOVIE = u"movi"
    RESOURCE_TYPE_LIST = [
            RESOURCE_TYPE_NEWS,
            RESOURCE_TYPE_MOVIE
            ]

    @staticmethod
    def get_resource_type(item_id):
        if len(item_id) < ResourceType.RESOURCE_TYPE_LENTH:
            return None
        return item_id[0:ResourceType.RESOURCE_TYPE_LENTH]

class LogFeedBackKey:
    UID = "uid"
    ITEM_ID = "item_id"
    CARD_FEATURE = "card_feature"
    TYPE = "type"

class UserInfo:
    def __init__(self, uid, logger):
        self.uid = uid
        self.offline_resource_visit_info = {}
        self.recent_resource_visit_info = {}
        self.final_resource_visit_info = {}
        self.recent_push_item_id_list = set()
        self.recent_push_reason_info = {}
        self.user_feature_info = {}
        if uid:
            self.fetch(logger)

    def __str__(self):
        return "uid:%s, offline_resource_visit_info:%s, recent_resource_visit_info:%s, final_resource_visit_info:%s, recent_push_item_id_list:%s, recent_push_reason_info:%s" \
                % (self.uid, self.offline_resource_visit_info,
                        self.recent_resource_visit_info, 
                        self.final_resource_visit_info, 
                        self.recent_push_item_id_list, 
                        self.recent_push_reason_info)

    def fetch(self, logger):
        """update user info, return None"""
        uid = self.uid
        #offline_resource_visit_info
        try:
            errCode, kv_dict = model.get_offline_user_resource_visitinfo(uid, ResourceType.RESOURCE_TYPE_LIST)
            if not is_valid_data(errCode, kv_dict, "offline_user_resource_visitinfo", {"uid":uid, "resource_type_list":"..."}):
                pass
            for k, v in kv_dict.iteritems():
                self.offline_resource_visit_info[k] = VisitInfo()
                self.offline_resource_visit_info[k].ParseFromString(v)
        except:
            logger.error("bad offline_resource_visit_info:%s" % traceback.format_exc())
        #recent_resource_visit_info
        try:
            errCode, kv_dict = model.get_online_user_resource_visitinfo(uid, ResourceType.RESOURCE_TYPE_LIST)
            if not is_valid_data(errCode, kv_dict, "online_user_resource_visitinfo", {"uid":uid, "resource_type_list":"..."}):
                pass
            for k, v in kv_dict.iteritems():
                self.recent_resource_visit_info[k] = VisitInfo()
                self.recent_resource_visit_info[k].ParseFromString(v)
            #final_resource_visit_info
            self.final_resource_visit_info = UserInfo.merge_offline_recent_resource_visit_info(self.offline_resource_visit_info,
                    self.recent_resource_visit_info)
        except:
            logger.error("bad recent_resource_visit_info:%s" % traceback.format_exc())
            self.final_resource_visit_info = self.offline_resource_visit_info
        #pushed_item_id_list
        try:
            errCode, v = model.get_online_user_push_item_list(uid)
            if not is_valid_data(errCode, v, "online_user_push_item_list", {"uid":uid}):
                pass
            if v:
                item_id_list_proto = ItemIdList()
                item_id_list_proto.ParseFromString(v)
                self.recent_push_item_id_list = set()
                self.recent_push_item_id_list.update(item_id_list_proto.item_id)
        except:
            logger.error("bad pushed_item_id_list:%s" % traceback.format_exc())
        #pushed_feature_list
        try:
            errCode, v = model.get_online_user_feature_reason(uid)
            if not is_valid_data(errCode, v, "online_user_feature_reason", {"uid":uid}):
                pass
            if v:
                feature_list_proto = ItemFeatureList()
                feature_list_proto.ParseFromString(v)
                for u in feature_list_proto.feature:
                    self.recent_push_reason_info[u.feature_name] = u.weight
        except:
            logger.error("bad pushed_feature_list:%s" % traceback.format_exc())
        logger.debug("user_info:%s" % self)
        return None

    @staticmethod
    def merge_offline_recent_resource_visit_info(left, right):
        """ merge offline & recent resource visit_info, get summary info
            @return VisitInfo
        """
        result = {}
        for k,v in left.iteritems():
            result[k] = v
        for k,v in right.iteritems():
            result.setdefault(k, VisitInfo())
            result[k].pv_count += v.pv_count
            result[k].click_count += v.click_count
            result[k].weight = v.weight #@note: just overwrite with right weight
        return result

