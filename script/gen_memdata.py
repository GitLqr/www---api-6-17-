num = 8
type="common"

import sys
import getopt
import datetime
import MySQLdb as mysqldb
sys.path.append("interface")
import mysql_util

def gen_file(num, type):
    output = open("/Users/wudi/work/mymem/template", 'w')
    str = "question:\n\nanswer:\n"
    for i in range(num):
        print >> output, str

def push_data():
    data = open('/Users/wudi/work/mymem/template')
    formatdata = dict()
    temp = ""
    for line in data:
        if line.startswith(""):
            temp = line.strip("\n:")
            if not formatdata.__contains__(temp):
                formatdata[temp] = [""]
            else:
                formatdata[temp].append("")
        else:
            formatdata[temp][-1] += line
    dump_to_db(formatdata)

def dump_to_db(formatdata):
    mysql_obj = mysql_util.MysqlUtil()
    inst_num = len(formatdata["question"])
    sql = "insert memdata (question, answer, type, last_modify_time, insert_time, familiar) values (%s,%s,%s,%s,%s,%s)"
    now = datetime.datetime.now()
    for i in range(inst_num):
        params = (formatdata["question"][i].strip(), formatdata["answer"][i].strip(), type, now, now, 0)
        mysql_obj.execute(sql, params)

if __name__ == '__main__':
    options, args = getopt.getopt(sys.argv[1:], "gd")
    options = dict(options)
    if "-g" in options:
        print "gen file begin"
        gen_file(num, type)
        print "gen file end"
        exit()
    if "-d" in options:
        print "dump to db begin"
        push_data()
        print "dump to db end"
        exit()
    
