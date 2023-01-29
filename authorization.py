import re
import stdiomask



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
    with open('user_data.txt', 'r', encoding='utf-8') as f:
        for i in f:
            i = i.split()
            if i[0] == log and i[1] == pswd:
                return i[2:]
                break



def registration():
    db_info=data_collection()
    log = input('Введите логин: ').strip()
    pswd = input('Введите пароль: ').strip()
    with open('user_data.txt', 'a', encoding='utf-8') as f:
        print(f"{log} {pswd} {' '.join(db_info)}",file=f)
        print('Пользователь создан')
        return db_info

