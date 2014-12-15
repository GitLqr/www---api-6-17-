#-*- coding: utf8 -*-
# created by hualai.deng , 2013-04-01
import sys
import os

# set coding to utf8
reload( sys )
sys.setdefaultencoding( "utf8" )

# set the cur path.
mydir = os.path.dirname(__file__)
if mydir != '':
    os.chdir( mydir )

# import other
import web
import logging
import logging.config
import conf
import urls

# view the paths
#print sys.path

# on/off debug mod
web.config.debug = True

# load the logger config file.
logging.config.fileConfig("logging.conf")
#logger = logging.getLogger( )

# get the application interface
app = web.application(urls.getUrlsMap(), globals())
application=app.wsgifunc()

if __name__ == "__main__":
    #conf.g_conf = conf.g_conf_test
    app.run()
