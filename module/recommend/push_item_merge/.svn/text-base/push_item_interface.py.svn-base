#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
sys.path.append('.')
proto_path = '/usr/local/lib/python/alinow_backend_proto/'
if not proto_path in sys.path:
    sys.path.append(proto_path)
import logging, logging.config
import module.recommend.data_manage.model_interface as model
from item_pb2 import ItemIdList
import copy

logger = logging.getLogger("recommend.push_item")

MAX_ITEM_ID_LIST_LENGTH = 1000

# return False or True
def push_item_id_list_merge(uid, raw_item_id_list):
    errorCode, push_item_list_data = model.get_online_user_push_item_list(uid)
    if False == errorCode:
        logger.error('get online user push item list Failed, uid[%s]' % uid)
        return False
    try:
        push_item_list = ItemIdList()
        if None != push_item_list_data:
            push_item_list.ParseFromString(push_item_list_data)
        else:
            logger.debug('add push item id list for new user. uid: %s' % uid)
        for item_id in raw_item_id_list:
            push_item_list.item_id.append(item_id)
        if len(push_item_list.item_id) > MAX_ITEM_ID_LIST_LENGTH:
            push_item_id_list = getattr(push_item_list, 'item_id')
            item_id_list_len = len(push_item_id_list)
            tmp_push_item_id_list = push_item_id_list[item_id_list_len - MAX_ITEM_ID_LIST_LENGTH:]
            push_item_list.ClearField('item_id')
            for item_id in tmp_push_item_id_list:
                push_item_list.item_id.append(item_id)
        if False == model.set_online_user_push_item_list(uid, push_item_list.SerializeToString()):
            logger.error('set online user push item list error.')
            return False
        return True
    except:
        logger.error('push_item_id_list_merge failed. error: %s' %  str(sys.exc_info()))
        print str(sys.exc_info())
        return False

if __name__ == '__main__':
    print push_item_id_list_merge('uid_1', ['movilitem12','newsitem2432','moviitem23'])
    print model.get_online_user_push_item_list('uid_1')
