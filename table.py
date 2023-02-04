import sqlite3 as sl
from prettytable import from_db_cursor
def show_table(result,t):
  for row in result:
    t.add_row([*row])
  print(t)


def show_tb_name(result):
    print(from_db_cursor(result))
