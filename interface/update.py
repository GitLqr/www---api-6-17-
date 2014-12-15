import web
import datetime
import logging
import logging.config
import conf
import mysql_util
import json
import bunch

logger = logging.getLogger() 
logger_info = logging.getLogger( 'info' )

class Main:        
    def __init__ ( self ):
        web.header( 'Content-Type', 'text/html;charset=utf-8' )
        self.mysql_util = mysql_util.MysqlUtil()

    def searchItem(self, question):
        sql = "select question, type, answer, familiar, last_modify_time from memdata where question like %s"
        return self.mysql_util.query(sql, "%"+question.strip()+"%")[1]

    def updateDB(self, data):
        sql = "update memdata set question=%s, answer=%s, type=%s, familiar=%s, last_modify_time=%s where question=%s"
        params = (data.question, data.answer, data.type, data.familiar, data.last_modify_time, data.question)
        return self.mysql_util.execute(sql, params)

    def b_Welcome(self, data):
        return len(data) == 0

    def b_Search(self, data):
#return data.question!='' and data.type=='' and data.answer=='' and data.familiar=='' and data.last_modify_time==''
        return data.has("search")

    def b_Update(self, data):
#return "" not in (data.question, data.type, data.answer, data.familiar, data.last_modify_time)
        return data.has("update")

    def GET(self, *args):
        args_dict = web.input()
        data = bunch.bunch(**args_dict)
        suggessions = ''
        if self.b_Welcome(data):
            data.question, data.type, data.answer, data.familiar, data.last_modify_time = '','','','',''
        elif self.b_Search(data):
            rt = self.searchItem(data.question)
            if len(rt) != 0:
                data.question, data.type, data.answer, data.familiar, data.last_modify_time = rt[0]
            for i in rt:
                other_sgst = i[0]
                suggessions+=other_sgst+'\n'
        elif self.b_Update(data):
            logger.debug("%s have been updated.",self.updateDB(data))

        render = web.template.render("templates")
        return render.update(data, suggessions)
