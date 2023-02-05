import re
import sqlite3 as sl


con = sl.connect('data_user.db')
cur = con.cursor()
log=None
user_id=None

def data_collection():
    print("Введите номер вендора: \n1-postgres \n2-MySQL \n3-MSserver")
    res=input().strip()
    try:
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
                db_info = re.sub('[;| =|>|<|]', " ", input()).split()
                db_info.append('3')

            case _:
                print(
                    'Вендор в данный момент не поддерживается')
                data_collection()
        return db_info
    except UnboundLocalError:
        print("Некоректные данные")



def identification():
    global log
    log=input('Введите логин: ').strip()
    pswd = input('Введите пароль: ').strip()
    user_id_bd(log)
    with con:
        data = cur.execute('SELECT db_info FROM USER WHERE login = ? and password = ?', (str(log), str(pswd)))
        for row in data:
            return "".join(row).split()
            break

def registration():
    global log
    db_info=data_collection()
    log = input('Введите логин: ').strip()
    pswd = input('Введите пароль: ').strip()
    with con:
        data = cur.execute('SELECT * FROM USER WHERE login = ?', (str(log),))
        for row in data:
           if not (row is None):
              print('Этот логин уже занят')
              registration()
        else:
            cur.execute('INSERT INTO USER (login, password, db_info) values(?, ?, ?)',
                              (str(log), str(pswd), ' '.join(db_info)))
            user_id_bd(log)
    return db_info

def user_id_bd(log):
    '''функция получения id пользователя'''
    global user_id
    data = cur.execute('SELECT id FROM USER WHERE login = ?', (str(log),))
    for row in data:
        user_id = row[0]

def hs_rs(req):
    '''функция заполнения истории запроса пользователя'''
    with con:
        cur.execute('INSERT INTO history_rs (request,user_id) values(?,?)',([req,str(user_id)]))

def out_rs(nm_tb):
    '''функция получения истории запроса определенного пользователя'''
    with con:
        return cur.execute(f"select request,time from {nm_tb} WHERE user_id = {int(user_id)}")

def last_rs():
    '''функция отправки последнего запроса определенного пользователя'''
    with con:
        data = cur.execute(f"SELECT request FROM history_rs  WHERE user_id = {int(user_id)} ORDER BY ID DESC LIMIT 1")
        for row in data:
            return "".join(row)

