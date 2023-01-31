import re
import sqlite3 as sl


con = sl.connect('data_user.db')
def data_collection():
    print("Введите номер вендора: \n1-postgres \n2-MySQL \n3-MSserver")
    res=input().strip()
    match res:
        case '1':
            print('Шаблон строки подключения для PostgreSQL: username:password@host:port/dbname')
            db_info=re.sub('[:|@|/]'," ",input()).split()
            db_info.append('1')

        case '2':
            print('Шаблон строки подключения для MySQL:Server=<server>;Database=<database>;UID=<user id>;PWD=<password>')
            db_info = re.sub('[;| =|]', " ", input()).split()
            db_info.append('2')
        case '3':
            print('Шаблон строки подключения для MSserver: Server=Server,Port;Database=DatabaseName;User Id=userid;Password=Passwordмм')
            db_info = re.sub('[:|@|/]', " ", input()).split()
            db_info.append('3')
        case _:
            print(
                'Вендор в данный момент не поддерживается')
            data_collection()
    return db_info

def identification():
    log=input('Введите логин: ').strip()
    pswd = input('Введите пароль: ').strip()
    with con:
        data = con.execute('SELECT db_info FROM USER WHERE login = ? and password = ?', (str(log), str(pswd)))
        for row in data:
            return "".join(row).split()
            break




def registration():
    db_info=data_collection()
    log = input('Введите логин: ').strip()
    pswd = input('Введите пароль: ').strip()
    with con:
        data = con.execute('SELECT * FROM USER WHERE login = ?', (str(log),))
        for row in data:
            if row != None:
                print('Этот логин уже занят')
                registration()
            else:
                con.execute('INSERT INTO USER (login, password, db_info) values(?, ?, ?)',
                            (str(log), str(pswd), ' '.join(db_info)))
                print('Пользователь создан')
        return db_info

