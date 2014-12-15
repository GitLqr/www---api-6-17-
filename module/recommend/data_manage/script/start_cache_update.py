#-*- coding: utf8 -*-
# created by zhijun.sunzj , 2013-05-16
import sys
sys.path.append('.')

import module.recommend.data_manage.cache_update_process as cache_update_process
import module.recommend.data_manage.log_conf
import module.recommend.data_manage.model_interface as model_interface
model_interface.db_cache_init()
cache_update_process.do_cache_update()

