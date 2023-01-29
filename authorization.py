import re

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
            print(db_info)
        case '3':
            print('Шаблон строки подключения для MSserver: username:password@host:port/dbname')
            db_info = re.sub('[:|@|/]', " ", input()).split()
            db_info.append('3')
        case _:
            print(
                'Вендор в данный момент не поддерживается')
            data_collection()
    return db_info

