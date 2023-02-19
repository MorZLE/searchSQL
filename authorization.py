from data_coll import data_collection
from table import show_table
from DB import DB


class Storage(DB):
    def __init__(self):
        self.con_db_app()

    def identification(self):
        try:
            self.login=input('Введите логин: ').strip()
            self.pswd = input('Введите пароль: ').strip()
            if self.login=='' or self.pswd=='':
                print('Пароль или логин не должен быть пустым')
                return self.identification()
            self.get_user_id()
            res, desc = self.exec('SELECT db_info FROM USER WHERE login = ? and password = ?', self.login, self.pswd)
            for row in res:
                return "".join(row).split()
                break
        except TypeError as err:
                print(err)

    def registration(self):
        self.db_info=data_collection()
        self.login = input('Введите логин: ').strip()
        self.pswd = input('Введите пароль: ').strip()
        if self.login == '' or self.pswd == '':
            print('Пароль или логин не должен быть пустым')
            return self.registration()

        res, desc = self.exec('SELECT * FROM USER WHERE login = ?', self.login)
        for row in res:
            if not (row is None):
                print('Этот логин уже занят')
                self.registration()
        return self.db_info


    def rec_user_data(self):
          res, desc = self.exec('INSERT INTO USER (login, password, db_info) values(?, ?, ?)',
                                self.login, self.pswd, ' '.join(self.db_info))
          self.get_user_id()

    def get_user_id(self):
        '''функция получения id пользователя'''
        res, desc = self.exec('SELECT id FROM USER WHERE login = ?', self.login)
        for row in res:
            self.user_id = row[0]

    def hs_rs(self, req):
        '''функция заполнения истории запроса пользователя'''
        self.exec('INSERT INTO history_rs (request,user_id) values (?,?)', req, self.user_id)

    def out_rs(self):
        '''функция получения истории запроса определенного пользователя'''
        res, desc = self.exec('SELECT request,time FROM history_rs WHERE user_id =?', self.user_id)
        show_table(res, desc)

    def last_rs(self):
        '''функция отправки последнего запроса определенного пользователя'''
        res, desc = self.exec("SELECT request FROM history_rs  WHERE user_id = ? ORDER BY ID DESC LIMIT 1", self.user_id)
        for row in res:
            return "".join(row)

