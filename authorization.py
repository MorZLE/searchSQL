import re
import sqlite3 as sl


class Identi():
    def __init__(self):
        self.login = None
        self.pswd = None
        self.db_info = None
        self.con = sl.connect('data_user.db')
        self.cur = self.con.cursor()
    def identification(self):
        try:
            self.login=input('Введите логин: ').strip()
            self.pswd = input('Введите пароль: ').strip()
            user_id_bd(self.login)
            with con:
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
        with con:
            data =  self.cur.execute('SELECT * FROM USER WHERE login = ?', (str(self.login),))
            for row in data:
               if not (row is None):
                  print('Этот логин уже занят')
                  registration()
            else:
                self.cur.execute('INSERT INTO USER (login, password, db_info) values(?, ?, ?)',
                                  (str(self.login), str(self.pswd), ' '.join(self.db_info)))
                user_id_bd(self.ogin)
        return self.db_info
    def user_id_bd(self,login):
        '''функция получения id пользователя'''
        data =  self.cur.execute('SELECT id FROM USER WHERE loginin = ?', (str(login),))
        for row in data:
            self.user_id = row[0]

    def hs_rs(self,req):
        '''функция заполнения истории запроса пользователя'''
        with con:
            self.cur.execute('INSERT INTO history_rs (request,user_id) values(?,?)',([req,str(user_id)]))

    def out_rs(self):
        '''функция получения истории запроса определенного пользователя'''
        with con:
            return self.cur.execute(f"select request,time from history_rs WHERE user_id = {int(user_id)}")

    def last_rs(self):
        '''функция отправки последнего запроса определенного пользователя'''
        with con:
            data = self.cur.execute(f"SELECT request FROM history_rs  WHERE user_id = {int(user_id)} ORDER BY ID DESC LIMIT 1")
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
                print('Шаблон строки подключения для MSserver: Server=Server,Port;Database=DatabaseName;User Id=userid;Password=Passwordмм')
                db_info = re.sub('[;| =|>|<|]', " ", input()).split()
                db_info.append('3')

            case _:
                print(
                    'Вендор в данный момент не поддерживается')
                data_collection()
        return db_info
    except UnboundLocalError:
        print("Некоректные данные")
