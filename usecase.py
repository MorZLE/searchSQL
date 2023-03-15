from authorization import Storage
from userdb import UserDBs
from DB import Info

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

    def send_user_db(self, db_info, login, database):
        return self.storage.send_user_db(db_info, login, database)

    def addDB(self, db_info):
        info = Info(db_info)
        info.parse_connection_string()
        cs = self.userDBs.getUserDbs(info.user)
        cs.record(info)



    def exes(self, query, *args):
        return self.db.exec(query, *args)
