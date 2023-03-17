from data_coll import data_collection
from table import show_table
from DB import DB
import math
import time
import datetime


class Storage(DB):
    def __init__(self):
        self.con_db_app()
        self.login = None
        self.passwd = None
        self.db_info = None
        self.user_id = None

    def identification(self, login, passwd):
         res, desc = self.exec('SELECT id FROM USER WHERE login = ? and password = ?',login, passwd)
         return res[0]

    def registration(self, login, passwd):
        res, desc = self.exec('INSERT INTO USER (login, password) values(?, ?)', login, passwd)

    def get_user_db(self, login):
        """Функция получения баз пользователя"""
        res, desc = self.exec('SELECT dbname FROM userDBs WHERE owner =?', login)
        return res

    def get_user_data_db(self, login):
        """Функция получения данных баз пользователя"""
        res, desc = self.exec('SELECT db_info FROM userDBs WHERE owner =?', login)
        return res


    def get_user_data_con_db(self, login, namedb):
        """Функция получения данных баз пользователя"""
        res, desc = self.exec('SELECT db_info FROM userDBs WHERE owner =? and dbname =?', login, namedb)
        return res


    def send_user_data(self, login, passwd, db_info):
        """Функция заполнения данных пользователя в бд"""
        res, desc = self.exec('INSERT INTO USER (login, password, db_info) values(?, ?, ?)',
                              login, passwd, ' '.join(db_info))
        self.get_user_id()

    def send_user_db(self, db_info, login, dbname):
        """Функция добавления новой базы пользователя в бд"""
        res, desc = self.exec('INSERT INTO userDBs (db_info, owner, dbname) values(?, ?, ?)',
                              ' '.join(db_info), login, dbname)
        self.get_user_id()



    def get_user_id(self):
        """Функция получения id пользователя"""
        res, desc = self.exec('SELECT id FROM USER WHERE login = ?', self.login)
        for row in res:
            return row[0]

    def hs_rs(self, user, req, cond):
        """Функция заполнения истории запроса пользователя"""
        tm = datetime.datetime.now()
        tm = tm.strftime("%H:%M:%S %d-%m-%Y ")
        self.exec('INSERT INTO history_rs (request,owner ,time,condition) values (?,?,?,?)', req, user,tm,cond)

    def out_rs(self, user):
        """Функция получения истории запроса определенного пользователя"""
        res, desc = self.exec('SELECT request,condition,time FROM history_rs WHERE owner  =?',user)
        return res, desc

    def last_rs(self):
        """Функция отправки последнего запроса определенного пользователя."""
        res, desc = self.exec("SELECT request FROM history_rs  "
                              "WHERE user_id = ? ORDER BY ID DESC LIMIT 1", self.user_id)
        for row in res:
            return "".join(row)