from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, login):
        self.__user = login
        return self

    def create(self, login):
        self.__user = login
        return self

    def get_id(self):
        return str(self.__user)
