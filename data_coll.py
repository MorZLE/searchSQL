import re


def data_collection():
    vendr = {1: 'PostgreSQL', 2: 'MySQL', 3: 'MSserver', 4:'SQLite'}
    def vendor():
        try:
            global res
            print("Введите номер вендора: \n1-postgres \n2-MySQL \n3-MSserver \n4-SQLite")
            res = int(input())
            return res
        except (TypeError,ValueError):
            print('Напишите цифру')
            return vendor()
    res = vendor()

    try:
        match vendr[res]:
            case 'PostgreSQL':
                print('Шаблон строки подключения для PostgreSQL: username:password@host:port/dbname')
                db_info=re.sub('[:|@|/]'," ", input()).split()
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
                db_info.append('MSserver')
            case 'SQLite':
                print('Введите название базы')
                db_info = input().strip().split()
                db_info.append('SQLite')
            case _:
                print(
                    'Вендор в данный момент не поддерживается')
                data_collection()
        return db_info
    except KeyError:
        data_collection()
    except UnboundLocalError:
        print("Некоректные данные")