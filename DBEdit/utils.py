__author__ = 'marcodiv'

#Simple utility module based on what i needed more often.
#Realized for Python 3.4.x

import sqlite3
import os
import sys


def killshit(status=None):
    if status is not None:
        sys.exit(status)
    sys.exit(42)


def isvowel(c):
    v=['a', 'e', 'i', 'o', 'u', 'à', 'è', 'é', 'ì', 'ù', 'å', 'ò','ø']
    return v.__contains__(c.lower())


def deletechr(stringa, char):
    return str(stringa).replace(char, '')


def nospace(stringa):
    return deletechr(stringa, ' ')


def getnamefrompath(path):
    pat=str(path)
    l=pat.split(os.sep)
    if len(l)>0:
        return l[len(l) -1]
    return ""


def indexofobj(lista, oggetto):
    for j in range(0, len(lista)):
        if lista[j] is oggetto:
            return j
    return -1


def upperlist(lista):
    res=[]
    for x in lista:
        res.append(str(x).upper())
    return res


class DBUtils():
    def __init__(self, db):
        self.db=sqlite3.connect(db)
        self.cursore=self.db.cursor()
        self.cursore.execute("pragma foreign_keys=ON")
        self.db.commit()
        self.orderby=""

    def getall(self, table):
        res=[]
        for x in self.cursore.execute("select * from " + str(table) + self.orderby):
            res.append(x)

        return res

    def getheaderfromquery(self, query):
        self.cursore.execute(query)
        res=[]
        for x in self.cursore.description:
            res.append(x[0])
        return res

    def getheaderfromtable(self, table):
        self.cursore.execute("select * from " + str(table))
        res=[]
        for x in self.cursore.description:
            res.append(x[0])
        return res

    def getsql(self, comando, params=[]):
        res=[]
        for x in self.cursore.execute(comando, params):
            res.append(x)
        return res

    def getsqlbyorder(self, comando, params=[]):
        comando+= self.orderby
        return self.getsql(comando, params)

    def exec(self, sql, params=[]):
        try:
            self.cursore.execute(sql, params)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    @staticmethod
    def getnamefromquery(query):
        x=str(query).upper()
        l=x.split(' ')
        i=0
        while l[i] != "FROM":
            i+=1
        res=""
        i+= 1
        if len(l)> i:
            while len(l)> i and l[i] != "WHERE" and l[i] != "ON":
                res+=l[i]
                res+=" "
                i+= 1
        else:
            res=l[i]
        return res

    def listtables(self):
        return self.getsql("select name from sqlite_master where type='table'")

    def close(self):
        self.db.commit()
        self.db.close()

    def droptable(self, table):
        self.exec("drop table " + str(table))

    def setorderby(self, string):
        self.orderby=" order by " + str(string)

    def clear(self, table):
        self.exec("delete from " + str(table))
