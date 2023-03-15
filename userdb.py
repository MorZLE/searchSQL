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
        print(self.dbs, 'база' )

    def get_active(self):
        return self.active


class UserDBs:
    dbs: typing.Dict[str, ConnStorage] = {}

    def __init__(self):
        self.dbs: typing.Dict[str, ConnStorage] = {}

    def getUserDbs(self, user):
        if self.dbs.get(user) is None:
            self.dbs[user] = ConnStorage()
            print(self.dbs, 'контейнер')
        return self.dbs[user]


    def getConnStorage(self, user):
        print(self.dbs, '2 раз')
        return self.dbs[user]

