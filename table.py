import sqlite3 as sl
from prettytable import from_db_cursor
def show_table(result,t):
    try:
        for row in result:
            t.add_row([*row])
        print(t)
    except TypeError as err:
        if 'NoneType' in str(err):
            print('Данных для вывода нету!')
            start_new()
        else:
            print(err)


def show_tb_name(result):
    print(from_db_cursor(result))
