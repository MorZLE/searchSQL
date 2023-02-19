import re
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
        else:
            res, desc = self.exec('INSERT INTO USER (login, password, db_info) values(?, ?, ?)',
                                  self.login, self.pswd, ' '.join(self.db_info))
            self.get_user_id()


        return self.db_info

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
        with self.connection:
            res, desc = self.exec("SELECT request FROM history_rs  WHERE user_id = ? ORDER BY ID DESC LIMIT 1",self.user_id)
            for row in res:
                return "".join(row)

vendr={1:'PostgreSQL',2:'MySQL',3:'MSserver'}
def data_collection():
    def vendor():
        try:
            global res
            print("Введите номер вендора: \n1-postgres \n2-MySQL \n3-MSserver")
            res = int(input())
            return res
        except (TypeError,ValueError):
            print('Напишите цифру')
            return vendor()
    res=vendor()

    try:
        match vendr[res]:
            case 'PostgreSQL':
                print('Шаблон строки подключения для PostgreSQL: username:password@host:port/dbname')
                db_info=re.sub('[:|@|/]'," ",input()).split()
                db_info.append('PostgreSQL')

            case 'MySQL':
                print('Шаблон строки подключения для MySQL:Server=<server>;Database=<database>;UID=<user id>;PWD=<password>')
                db_info = re.sub('[;| =|]', " ", input()).split()
                db_info.append('MySQL')

            case 'MSserver':
                db_info = [input('Введите драйвер:\n')]
                print('Шаблон строки подключения для MSserver: Server=serverName;UID=UserName;PWD=Password;Database=My_DW;')
                s = re.sub('[;| =|>|<|]', " ", input('Введите строку подключения\n')).split()
                for i in [1, 3, 5, 7]:
                    db_info.append(s[i])
                db_info.append('MySQL')

            case _:
                print(
                    'Вендор в данный момент не поддерживается')
                data_collection()
        return db_info
    except UnboundLocalError:
        print("Некоректные данные")
