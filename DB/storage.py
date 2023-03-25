from DB.DB import DB
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
        vender = db_info[-1]
        res, desc = self.exec('INSERT INTO userDBs (db_info, owner, dbname,vender) values(?, ?, ?, ?)',
                              ' '.join(db_info), login, dbname, vender)
        self.get_user_id()



    def get_user_id(self):
        """Функция получения id пользователя"""
        res, desc = self.exec('SELECT id FROM USER WHERE login = ?', self.login)
        for row in res:
            return row[0]

    def hs_rs(self, user, req, cond, namedb):
        """Функция заполнения истории запроса пользователя"""
        tm = datetime.datetime.now()
        tm = tm.strftime("%H:%M:%S %d-%m-%Y ")
        self.exec('INSERT INTO history_rs (request,owner ,time,condition,namedb) values (?,?,?,?,?)', req, user,tm,cond,namedb)

    def out_rs(self, user):
        """Функция получения истории запроса определенного пользователя"""
        res, desc = self.exec('SELECT request,namedb,condition,time FROM history_rs WHERE owner  =?', user)
        return res, desc

    def last_rs(self):
        """Функция отправки последнего запроса определенного пользователя."""
        res, desc = self.exec("SELECT request FROM history_rs  "
                              "WHERE user_id = ? ORDER BY ID DESC LIMIT 1", self.user_id)
        for row in res:
            return "".join(row)


    def clear_hs_user(self, user):
        res, desc = self.exec("delete from history_rs where owner =?", user)

    def vender_db(self, user, namedb):
        res, desc = self.exec("SELECT vender from userDBs where owner=? and dbname=?", user, namedb)
        return res

    def get_statistics_user(self, user):
        resT, desc = self.exec("SELECT count(*) from history_rs where owner=? and condition='True'", user)
        resF, desc = self.exec("SELECT count(*) from history_rs where owner=? and condition='False'", user)
        t = int(tuple(resT)[0][0])
        f = int(tuple(resF)[0][0])
        all = t+f
        cf = 0
        if t > 0 and f > 0:
            cf = int(t/((all)/100))
        return all, t, cf

    def check_psw_user(self, username, psw):
        res, desc = self.exec("SELECT count(*) from user where login=? and password=?", username, psw)
        res = int(tuple(res)[0][0])
        return True if res == 1 else False

    def set_user_psw(self, username, psw):
        res, desc = self.exec("UPDATE user SET password =? WHERE login=?", psw, username)

    def del_db_user(self, username, namedb):
        self.exec("DELETE FROM userdbs where owner =? and dbname =?", username, namedb)

    def check_db(self, username, database):
        res, desc = self.exec("SELECT count(*) from userdbs where owner =? and dbname =?", username, database)
        res = int(tuple(res)[0][0])
        return True if res == 0 else False

