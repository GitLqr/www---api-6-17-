import MySQLdb as mysqldb
import logging
import datetime

logger = logging.getLogger()

class MysqlUtil:
    def __init__(self):
        try:
            self.db = mysqldb.connect(db='mymem', user='root', port=3306, host='localhost')
            self.db.set_character_set('utf8')
            self.cur = self.db.cursor()
        except mysqldb.Error, e:
            raise e

    def updatedb(self, answer):
        now = datetime.datetime.now()
        if answer["mem"] == "Yes":
            answer["familiar"] = int(answer["familiar"]) + 1
            answer["last_modify_time"] = now
            sql = "update memdata set familiar = %s, last_modify_time = %s, answer = %s where question = %s"
            self.cur.execute(sql, (answer["familiar"], answer["last_modify_time"], answer["answer"], answer["question"]))
            self.db.commit()
            logger.debug("updated")
        elif answer["mem"] == "No":
            answer["familiar"] = int(answer["familiar"])
            answer["last_modify_time"] = now
            sql = "update memdata set familiar = %s, last_modify_time = %s, answer = %s where question = %s"
            self.cur.execute(sql, (answer["familiar"], answer["last_modify_time"], answer["answer"], answer["question"]))
            self.db.commit()
            logger.debug("updated")
    
    def execute(self, sql, params):
        rt = self.cur.execute(sql, params)
        self.db.commit()
        return rt

    def query(self, sql, params):
        rt = self.cur.execute(sql, params)
        return rt, self.cur.fetchall()

    def getMemData(self):
        sql = "select question, answer, type, familiar, last_modify_time from memdata"
        self.cur.execute(sql)
        return self.cur.fetchall()
