import web
import datetime
import logging
import logging.config
import conf
import mysql_util
import json

logger = logging.getLogger() 
logger_info = logging.getLogger( 'info' )
        
class Main:        
    def __init__ ( self ):
        web.header( 'Content-Type', 'text/html;charset=utf-8' )
        self.mysql_util = mysql_util.MysqlUtil()
        self.conf = json.load(open("conf/ebbinghaus.json"))

    def filterMemData(self, type):
        all_data = self.mysql_util.getMemData()
        output = []
        now = datetime.datetime.now()
        for i in all_data:
            question, answer, type_, familiar, last_modify_time = i
            delta_hour = now-last_modify_time
            delta_hour = delta_hour.total_seconds()/3600.0
            if self.conf[str(familiar)] < delta_hour and type == type_:
                output.append(i)
            else:
                continue
        return output

    def GET(self, *args):
        args_dict = web.input()
        if "question" in args_dict and "mem" in args_dict:
            self.mysql_util.updatedb(args_dict)

        render = web.template.render("templates")
        data = self.filterMemData(args_dict['type'])
        
        return render.mymem(data)
