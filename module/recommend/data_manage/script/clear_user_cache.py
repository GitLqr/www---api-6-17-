#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-16

import sys
sys.path.append('.')

import module.recommend.data_manage.cache_update_process as cache_update_process
import module.recommend.data_manage.log_conf
#cache_update_process.clear_online_cache()
import module.recommend.data_manage.model_interface as model_interface


if __name__ == '__main__':
    if 2 != len(sys.argv):
        print 'input error, cmd [uid]'
        sys.exit()
    uid = sys.argv[1]
    model_interface.db_cache_init()
    print cache_update_process.cache_clear_online_by_user(uid)
