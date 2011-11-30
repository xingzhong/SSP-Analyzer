#!/usr/bin/env python

import MySQLdb
class SQL:
    def __init__(self, dname, tname=None):
        self.conn = MySQLdb.connect(host = "localhost", user = "ssp", \
                passwd = "ssp", db = dname)
        self.cursor = self.conn.cursor()
        self.tn = tname

    def free(self):
        self.cursor.close()
        self.conn.close()

    def tpl_sql(self, cmd = " ", tbc = "*"):
        command = "select " + tbc + " from " + self.tn + " " + cmd
        #print '[debug]:\t', command
        self.cursor.execute(command)
        result = []
        while(True):
            row = self.cursor.fetchone()
            if row == None:
                break
            result.append(row)
        return result
    
    def ls(self):
        return self.tpl_sql()

    def numbb(self):
        tbc = "MAX(block)"
        return self.tpl_sql(tbc = tbc)[0][0]

    def numnode(self):
        tbc = "MAX(id)"
        return self.tpl_sql(tbc = tbc)[0][0]
    
    def tls(self):
        command = "show tables"
        self.cursor.execute(command)
        result = []
        while(True):
            row = self.cursor.fetchone()
            if row == None:
                break
            result.append(row)
        return result

    def drop(self, db):
        command = "drop database if exists %s"%(db)
        self.cursor.execute(command)
