from authorization import Storage


class UniqueUsernameCheckFailed(Exception):
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


