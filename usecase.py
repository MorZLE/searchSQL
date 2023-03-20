from storage import Storage
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
    db = None

    def __init__(self):
        self.storage = Storage()
        self.userDBs = UserDBs()
        self.db = DB()


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
        isActive = cs.check_db(namedb)
        if isActive:
            cs.get_new_active(namedb)
        else:
            db_info = self.storage.get_user_data_con_db(username, namedb)[0]
            db_info = ''.join(db_info).split()
            self.addDB(db_info, username)



    def check_active(self, username):
        cs = self.userDBs.getUserDbs(username)
        if cs.active is None:
            return False
        else:
            return True

    def hs_rs(self, user, req, cond):
        return self.storage.hs_rs(user, req, cond)

    def out_rs(self, user):
        return self.storage.out_rs(user)

    def exec(self, query, username):
        cs = self.userDBs.getUserDbs(username)
        con = cs.get_active()
        return self.db.userExec(con, query)

    def clear_hs_user(self, username):
        self.storage.clear_hs_user(username)

    def print_table(self, username, active):
        vender = ' '.join(self.storage.vender_db(username, active)[0])
        match vender:
            case 'PostgreSQL':
                _, res, desc = self.exec("SELECT table_name FROM information_schema.tables WHERE table_schema='public'", username)
            case 'MySQL':
                _, res, desc = self.exec("SHOW TABLES")
            case 'MSserver':
                _, res, desc = self.exec("SELECT table_name FROM information_schema.tables WHERE table_schema='public'", username)
            case 'SQLite':
                _, res, desc = self.exec("SELECT name FROM sqlite_master WHERE type='table' and name != 'sqlite_sequence';", username)
        return res

    def get_statistics_user(self, username):
        return self.storage.get_statistics_user(username)

    def check_psw_user(self, username, psw):
        return self.storage.check_psw_user(username, psw)

    def set_user_psw(self, username, psw):
        self.storage.set_user_psw(username, psw)