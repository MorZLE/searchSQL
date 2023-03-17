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
        try:
            cur = db.connect(info.data_db)
        except IndexError:
            raise IndexError
        self.active = cur
        self.dbs[info.database] = cur

    def get_active(self):
        return self.active

    def get_new_active(self, namedb, db_info):
        if self.dbs.get(namedb) is None:
            db = DB()
            try:
                cur = db.connect(db_info)
            except IndexError:
                raise IndexError
            self.active = cur
            self.dbs[namedb] = cur
        else:
            self.active = self.dbs[namedb]

class UserDBs:
    dbs: typing.Dict[str, ConnStorage] = {}

    def __init__(self):
        self.dbs: typing.Dict[str, ConnStorage] = {}

    def getUserDbs(self, user):
        if self.dbs.get(user) is None:
            self.dbs[user] = ConnStorage()
        return self.dbs[user]



