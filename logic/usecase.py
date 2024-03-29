from DBs.storages import Storage
from logic.userdb import UserDBs
from DBs.DB import Info, DB
from sqlite3 import Binary


class UniqueUsernameCheckFailed(Exception):
    pass


class DbNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass


class DuplicateDB(Exception):
    pass


class DBerr(Exception):
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
        if self.storage.check_db(username, info.database):
            cs = self.userDBs.getUserDbs(username)
            try:
                cs.record(info)
            except DBerr:
                raise DBerr
        else:
            raise DuplicateDB

    def connDB(self, username, namedb):
        cs = self.userDBs.getUserDbs(username)
        isActive = cs.check_db(namedb)
        if isActive:
            cs.get_new_active(namedb)
        else:
            self.updateConn(namedb, username)

    def updateConn(self, namedb, username):
        db_info = self.storage.get_user_data_con_db(username, namedb)[0]
        db_info = ''.join(db_info).split()
        info = Info(db_info)
        cs = self.userDBs.getUserDbs(username)
        cs.record(info)

    def check_active(self, username):
        cs = self.userDBs.getUserDbs(username)
        if cs.active is None:
            return False
        else:
            return True

    def hs_rs(self, user, req, cond,namedb):
        return self.storage.hs_rs(user, req, cond,namedb)

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

    def del_db_user(self, username, namedb):
        self.storage.del_db_user(username, namedb)
        cs = self.userDBs.getUserDbs(username)
        db = cs.check_db(namedb)
        if db:
            cs.del_db(namedb)

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == "png" or ext == "PNG":
            return True
        return False

    def updateUserAvatar(self, avatar, username):
        if not avatar:
            return False
        try:
            binary = Binary(avatar)
            self.storage.send_avatar(username, binary)
        except Exception:
            return False
        return True

    def get_avatar(self, username, app):
        img = self.storage.get_avatar(username)
        if img is None:
            try:
                with app.open_resource('static\\img\\avatar.png', mode="rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))

        return img