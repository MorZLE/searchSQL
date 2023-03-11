from flask_login import UserMixin

class UserLogin(UserMixin):
    def fromDB(self, author):
        self.user = author.login
        return self

    def create(self, author):
        self.user = author.login
        return self

    def get_id(self):
        return str(self.user)
