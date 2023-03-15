from DB import DB
import typing


class ConnStorage(DB):
    '''Класс хранения подключений пользователя'''

    dbs: typing.Dict[str, DB] = {}
    active: DB

    def __init__(self):
        self.dbs: typing.Dict[str, DB] = {}

    def record(self, info):
        db = DB()
        cur = db.connect(info.data_db)
        self.active = cur
        self.dbs[info.database] = cur

class UserDBs:
    dbs: typing.Dict[str, ConnStorage] = {}

    def __init__(self):
        self.dbs: typing.Dict[str, ConnStorage] = {}

    def getUserDbs(self, user):
        if self.dbs.get(user) is None:
            self.dbs[user] = ConnStorage()
        return self.dbs[user]




