from DB import DB
import typing


class UserDBs:
    dbs = None

    def __init__(self):
        self.dbs: typing.Dict[str, ConnStorage] = {}


class ConnStorage:
    dbs = None
    active = None
    def __init__(self):
        self.dbs: typing.Dict[str, DB] = {}
        self.active: typing.Dict[str, DB] = {}

