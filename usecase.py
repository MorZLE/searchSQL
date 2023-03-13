from authorization import Storage


class UniqueUsernameCheckFailed(Exception):
    pass


class DbNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass


class UseCase:
    storage = None

    def __init__(self):
        self.storage = Storage()

    def create_user(self, username, password):
        try:
            self.storage.registration(username, password)
        except:
            raise UniqueUsernameCheckFailed

    def identification(self, username, password):
        try:
            return self.storage.identification(username, password)
        except:
            raise UserNotFound

    def get_user_db(self, username):
        try:
            return self.storage.get_user_db(username)
        except:
            raise DbNotFound

    def send_user_db(self,db_info, login, database):
        return self.storage.send_user_db(db_info, login, database)
