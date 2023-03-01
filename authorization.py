from data_coll import data_collection
from table import show_table
from DB import DB


class Storage(DB):
    def __init__(self):
        self.con_db_app()
        self.login = None
        self.passwd = None
        self.db_info = None
        self.user_id = None

    def enter_pas_log(self):
        """Функция сбора логина и пароля"""
        self.login = input('Введите логин: ').strip()
        self.passwd = input('Введите пароль: ').strip()
        if self.login == '' or self.passwd == '':
            print('Пароль или логин не должен быть пустым')
            return self.enter_pas_log()

    def identification(self):
        try:
            if self.db_info is None:
                self.enter_pas_log()
            res, desc = self.exec('SELECT db_info FROM USER WHERE login = ? and password = ?', self.login, self.passwd)
            for row in res:
                return "".join(row).split()
        except TypeError as err:
                print(err)

    def registration(self):
        if self.db_info is None:
            self.db_info = data_collection()
            self.enter_pas_log()
        res, desc = self.exec('SELECT * FROM USER WHERE login = ?', self.login)
        for row in res:
            if not (row is None):
                print('Этот логин уже занят')
                self.registration()
        return self.db_info

    def send_user_data(self):
        """Функция заполнения данных пользователя в бд"""
        res, desc = self.exec('INSERT INTO USER (login, password, db_info) values(?, ?, ?)',
                              self.login, self.passwd, ' '.join(self.db_info))
        self.get_user_id()

    def get_user_id(self):
        """Функция получения id пользователя"""
        res, desc = self.exec('SELECT id FROM USER WHERE login = ?', self.login)
        for row in res:
            self.user_id = row[0]

    def hs_rs(self, req):
        """Функция заполнения истории запроса пользователя"""
        self.exec('INSERT INTO history_rs (request,user_id) values (?,?)', req, self.user_id)

    def out_rs(self):
        """Функция получения истории запроса определенного пользователя"""
        res, desc = self.exec('SELECT request,time FROM history_rs WHERE user_id =?', self.user_id)
        show_table(res, desc)

    def last_rs(self):
        """Функция отправки последнего запроса определенного пользователя."""
        res, desc = self.exec("SELECT request FROM history_rs  "
                              "WHERE user_id = ? ORDER BY ID DESC LIMIT 1", self.user_id)
        for row in res:
            return "".join(row)