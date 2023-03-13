from authorization import Storage
from DB import DB
from userdb import UserDB



class UniqueUsernameCheckFailed(Exception):
    pass


class DbNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass


class UseCase:
    storage = None
    userdb = None

    def __init__(self):
        self.storage = Storage()


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

    def connect(self, db_info):
        self.userdb = UserDB(db_info)




    def exes(self, query, *args):
        return self.db.exec(query, *args)
