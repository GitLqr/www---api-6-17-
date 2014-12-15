#-*- coding: utf8 -*-
# created by hualai.deng , 2013-01-31

import MySQLdb

#简化DB操作
class MyDB:
    db = None

    def __init__ (self, dbconf=None):
        if dbconf != None:
            self.connect(dbconf)
        
    def connect (self, dbconf):
        if self.db != None:
            self.db.close()
            self.db = None
        
        db_name = dbconf['db_name']
        db_host = dbconf['host']
        db_passwd = dbconf['passwd']
        db_user = dbconf['user']
        db_port = dbconf['port']
        db_charset = dbconf['charset']
        self.db = MySQLdb.connect(host=db_host, port=db_port, db=db_name, user=db_user, passwd=db_passwd, charset=db_charset)
        return self.db

    def execute (self, sql, rd=None):
        cur=self.db.cursor()
        cur.execute(sql, rd)
        self.db.commit()
        cur.close()

    def executeEx (self, sql, rd=None):
        cur=self.db.cursor()
        result = cur.execute(sql, rd)
        self.db.commit()
        cur.close()
        return result


    def executemany (self, sql, rds):
        cur=self.db.cursor()
        cur.executemany(sql, rds)
        self.db.commit()
        cur.close()
        
    def query (self, sql):
        cur=self.db.cursor()
        cur.execute(sql)
        results=cur.fetchall()
        cur.close()
        return results
        
        
        
