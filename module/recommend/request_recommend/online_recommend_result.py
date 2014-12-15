#!/usr/bin/env python
# -*- coding: utf8 -*-
import logging, logging.config
import traceback
import sys
sys.path.append('/usr/local/lib/python/')
sys.path.append('.')
from alinow_backend_proto.common_pb2 import VisitInfo,ItemFeature,UserFeature,ItemFeatureList,UserFeatureList
from alinow_backend_proto.item_pb2 import ItemIdList,FeatureNameItemIdList
from alinow_backend_proto.news_pb2 import FeatureNameLimit,FeatureNameLimitList,NewsItemFeatureInfo,NewsItemFeatureInfoList,NewsFeatureItemList
from online_data_def import ResourceType, UserInfo, LogFeedBackKey
import module.recommend.data_manage.model_interface as model
import module.recommend.request_recommend
from module.recommend.request_recommend.util import is_valid_data
import module.recommend.request_recommend.translate_reason as translate_reason

logger = logging.getLogger("recommend.online")   

class RecommendItem:
    def __init__(self, item_id=None, feature_name_list=None, item_info_json=None):
        self.item_id = item_id
        self.feature_name_list = feature_name_list
        self.item_info_json = item_info_json 

    def __eq__(self, other):
        if other is None:
            return False
        return self.item_id == other.item_id

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "item_id:%s\titem_info_json:%s" % (self.item_id,
                self.item_info_json)

class RecommendItemContainer:
    def __init__(self):
        self.reason2itemidlist = {}
        self.reason_list = []
        pass

    def __str__(self):
        return "reason_list:%s reason2itemidlist:%s" % (self.reason_list, self.reason2itemidlist)

    def size(self):
        #@note:CHANGE FROM item count to reason count
        #return get_reason2itemlist_dict_size(self.reason2itemidlist)
        return len(self.reason_list)

    def add(self, reason, item_id_list):
        self.reason_list.append(reason)
        if reason in self.reason2itemidlist:
            logger.debug("ignore existing reason:%s" % reason)
        #logger.info("reason:%s, size:%s" % (reason, len(item_id_list)))
        self.reason2itemidlist[reason] = item_id_list

    def update(self, other):
        self.reason_list.extend(other.reason_list)
        self.reason2itemidlist.update(other.reason2itemidlist)

    def merge_dedup(self, other, count):
        """ add other and dedup, remove the extra more item
            @return None
        """
        for k in  other.reason_list:
            if self.size() >= count:
                break
            if k not in other.reason2itemidlist:
                logger.error("reason not existing in dict:%s" % reason)
                continue
            if k in self.reason2itemidlist:
                logger.debug("ignore existing reason result:%s" % (k))
                continue
            v = other.reason2itemidlist[k]
            #@note: note care item list size, current we use @reason count but not @item count
            #if len(v) + self.size() > count:
            #    self.add(k, v[0:count-self.size()])
            #    break
            self.add(k, v)
        return None

    def to_list(self, user_info):
        result = []
        for resource_type, user_feature_list in user_info.user_feature_info.iteritems():
            logger.debug("resource_type:%s, user_info:%s" % (resource_type, user_feature_list))
        for k in self.reason_list:
            if k not in self.reason2itemidlist:
                logger.error("reason not existing:%s" % k)
                continue
            reason1, reason2 = translate_reason.translate_reason(k)
            resouce_type = ResourceType.get_resource_type(k)
            default_reason = reason2
            if resouce_type in user_info.user_feature_info:
                user_feature_list_proto = user_info.user_feature_info[resouce_type]
                for u in user_feature_list_proto.feature:
                    if u.feature_name == k and u.visit_info.click_count > 0:
                        default_reason = reason1
                        break
            reason = default_reason
            logger.debug("reason_old:%s,reason_new:%s,cur:%s" % (reason1, reason2, reason))
            result.append(((k, reason), self.reason2itemidlist[k]))
        return result

    def get_summary_str(self, final_result):
        result = []
        for k in final_result:
            itemidlist_str = "[%s]" % ",".join([i.item_id for i in k[1]])
            result.append("%s::%s::%s" % (k[0][0], k[0][1], itemidlist_str))
        return " | ".join(result)

