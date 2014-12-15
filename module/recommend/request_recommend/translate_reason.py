#!/usr/bin/env python
# -*- coding: utf8 -*-
import logging, logging.config
import traceback
import sys
sys.path.append('/usr/local/lib/python/')
sys.path.append('.')
from online_data_def import ResourceType, UserInfo, LogFeedBackKey
import module.recommend.data_manage.model_interface as model
import reason_desc

logger = logging.getLogger("recommend.online")

def translate_reason(reason):
    reason_dict = {}
    logger.debug("try to translate reason:%s" % reason)
    for item in reason_desc.reason_desc:
        reason_dict[item[0]] = (item[3], item[5])
    FIELD_SEPERATEOR = "_"
    MULTI_FIELD_SEPERATOR = "、"
    resource_type = reason[0:4]
    reason_prefix = reason[0:8]
    reason_postfix = reason[8:]
    if resource_type in [u'movi'] and reason[4:8] == "like":
        in_e, in_kv = model.get_offline_item_id_new_to_old([reason_postfix])
        if in_e and in_kv:
            old_id = in_kv[reason_postfix]
            desc = reason_dict[reason_prefix]
            result = desc[0] % old_id.split("_", 2)[2]
            logger.debug("try to translate reason,reason:%s,result:%s" % (reason, result))
            return (result, result)
        else:
            logger.error("item id not existing:%s" % (reason_postfix))
            return (reason, reason)
    if reason_prefix not in reason_dict:
        logger.error("unknown tag:%s" % (reason_prefix))
        return (reason, reason)
    desc = reason_dict[reason_prefix]
    if '%s' in desc[0]:
        return (desc[0] % reason_postfix, desc[1] % reason_postfix)
    try:
        items = reason_postfix.split(FIELD_SEPERATEOR)
        param_dict = {}
        for i in range(0, len(items)):
            param_dict[str(i+1)] = items[i]
        return (desc[0] % param_dict, desc[1] % param_dict)
    except:
        logger.error("bad exception in translate_reason,reason_postfix:%s, items:%s, exception:%s" % (reason_postfix, items, traceback.format_exc()))
        return reason, reason

def test_get_reason():
    reasons = [
    "movivtnf1985",
    "movibtqt爱情",
    "movibtpm哈利波特",
    "moviyear1985",
    "movivtpm哈利波特",
    "movivtdq香港电影",
    "moviacto葛优",
    "movivtqt温情",
    "movibtlx科幻",
    "movivtyr汤姆·汉克斯",
    "movidire张艺谋",
    "movibtdq美国",
    "movibtnf1985",
    "moviloca美国",
    "movibtyr汤姆·汉克斯",
    "movivtlx科幻",
    "movicate科幻",
    "newssorc华龙网",
    "newsctgy体育",
    "newstopi互联网精选",
    "newsname姚明",
    "newsinst发改委",
    "newsaddr中关村",
    "newsngrm体育_小德_法网",
    "newsngrm体育_小德_法网_德国",
    #"newsngrm体育_小德",
    #"newsngrm体育",
    "newsttag科技_iphone",
    #"newsttag科技",
    "newsword我是歌手",
    "newsregn北京市",
    "movilikemoviI90ibmamO_f5birV",
    "newsctgy时尚",
    "newsctgy游戏",
    "newsctgy社会",
    "newsctgy国际",
    "newsctgy军事",
    "movibtqt搞笑",
    "movicate科幻",
    "movibtqt男女关系",
    "movicate战争",
    "movilikemoviI90ibmamO_f5birV",
    "movibtqt恋爱"
    ]
    for i in reasons:
        result = translate_reason(i)
        print result[0], result[1]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(name)s    %(filename)s +%(lineno)d    %(levelname)s   %(message)s")
    import module.recommend.data_manage.model_interface as model
    db_conf = {
             'db_name': 'alinow_zhijun',
             'host': '10.250.12.84',
             'passwd': '',
             'user': 'root',
             'port': 3306,
             'charset': 'utf8'
        }
    cache_conf = {
             'host':'10.250.12.84',
             'port':6379,
        }
    model.db_cache_init(db_conf, cache_conf)

    test_get_reason()
