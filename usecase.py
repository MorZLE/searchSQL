from authorization import Storage
from userdb import UserDBs
from DB import Info, DB

class UniqueUsernameCheckFailed(Exception):
    pass


class DbNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass


class UseCase:
    storage = None
    userDBs = None


    def __init__(self):
        self.storage = Storage()
        self.userDBs = UserDBs()



    def create_user(self, username, password):
        try:
            self.storage.registration(username, password)
        except Exception:
            raise UniqueUsernameCheckFailed

    def identification(self, username, password):
        try:
            return self.storage.identification(username, password)
        except Exception:
            raise UserNotFound

    def get_user_db(self, username):
        try:
            return self.storage.get_user_db(username)
        except Exception:
            raise DbNotFound

    def get_user_data_db(self, username):
        try:
            return self.storage.get_user_data_db(username)
        except Exception:
            raise DbNotFound

    def send_user_db(self, db_info, login, database):
        return self.storage.send_user_db(db_info, login, database)

    def addDB(self, db_info, username):
        info = Info(db_info)
        info.parse_connection_string()
        cs = self.userDBs.getUserDbs(username)
        try:
            cs.record(info)
        except IndexError:
            raise IndexError

    def connDB(self, username, namedb):
        cs = self.userDBs.getUserDbs(username)
        db = cs.check_db(namedb)
        if db:
            cs.get_new_active(namedb)
        else:
            db_info = self.storage.get_user_data_con_db(username, namedb)[0]
            db_info = ''.join(db_info).split()
            self.addDB(db_info, username)


    def hs_rs(self, user, req, cond):
        return self.storage.hs_rs(user, req, cond)

    def out_rs(self, user):
        return self.storage.out_rs(user)

    def exec(self, query, username):
        db = DB()
        cs = self.userDBs.getUserDbs(username)
        con = cs.get_active()
        return db.userExec(con, query)
