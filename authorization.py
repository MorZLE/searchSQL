import re
import sqlite3 as sl


class Identi():
    def __init__(self):
        self.con = sl.connect('data_user.db')
        self.cur = self.con.cursor()
        self.con.execute('CREATE TABLE IF NOT EXISTS USER ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, login text, password text, db_info text);')
        self.con.execute('CREATE TABLE IF NOT EXISTS history_rs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, request text, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, user_id int);')
        self.con.commit()

    def identification(self):
        try:
            self.login=input('Введите логин: ').strip()
            self.pswd = input('Введите пароль: ').strip()
            self.user_id_bd(self.login)
            with self.con:
                data = self.cur.execute('SELECT db_info FROM USER WHERE login = ? and password = ?', (str(self.login), str(self.pswd)))
                for row in data:
                    return "".join(row).split()
                    break
        except TypeError as err:
                print('Неверные данные')

    def registration(self):
        self.db_info=data_collection()
        self.login = input('Введите логин: ').strip()
        self.pswd = input('Введите пароль: ').strip()
        with self.con:
            data =  self.cur.execute('SELECT * FROM USER WHERE login = ?', (str(self.login),))
            for row in data:
               if not (row is None):
                  print('Этот логин уже занят')
                  self.registration()
            else:
                self.cur.execute('INSERT INTO USER (login, password, db_info) values(?, ?, ?)',
                                  (str(self.login), str(self.pswd), ' '.join(self.db_info)))
                self.user_id_bd(self.login)
        return self.db_info

    def user_id_bd(self,login):
        '''функция получения id пользователя'''
        data =  self.cur.execute('SELECT id FROM USER WHERE login = ?', (str(self.login),))
        for row in data:
            self.user_id = row[0]

    def hs_rs(self,req):
        '''функция заполнения истории запроса пользователя'''
        with self.con:
            self.cur.execute('INSERT INTO history_rs (request,user_id) values(?,?)',([req,str(self.user_id)]))

    def out_rs(self):
        '''функция получения истории запроса определенного пользователя'''
        with self.con:
            return self.cur.execute(f"SELECT request,time FROM history_rs WHERE user_id = {int(self.user_id)}")

    def last_rs(self):
        '''функция отправки последнего запроса определенного пользователя'''
        with self.con:
            data = self.cur.execute(f"SELECT request FROM history_rs  WHERE user_id = {int(self.user_id)} ORDER BY ID DESC LIMIT 1")
            for row in data:
                return "".join(row)

vendr={1:'PostgreSQL',2:'MySQL',3:'MSserver'}
def data_collection():
    print("Введите номер вендора: \n1-postgres \n2-MySQL \n3-MSserver")
    res=int(input())
    try:
        match vendr[res]:
            case 'PostgreSQL':
                print('Шаблон строки подключения для PostgreSQL: username:password@host:port/dbname')
                db_info=re.sub('[:|@|/]'," ",input()).split()
                db_info.append('1')

            case 'MySQL':
                print('Шаблон строки подключения для MySQL:Server=<server>;Database=<database>;UID=<user id>;PWD=<password>')
                db_info = re.sub('[;| =|]', " ", input()).split()
                db_info.append('2')

            case 'MSserver':
                db_info = [input('Введите драйвер:\n')]
                print('Шаблон строки подключения для MSserver: Server=serverName;UID=UserName;PWD=Password;Database=My_DW;')
                s = re.sub('[;| =|>|<|]', " ", input('Введите строку подключения\n')).split()
                for i in [1, 3, 5, 7]:
                    db_info.append(s[i])
                db_info.append('3')

            case _:
                print(
                    'Вендор в данный момент не поддерживается')
                data_collection()
        return db_info
    except UnboundLocalError:
        print("Некоректные данные")
