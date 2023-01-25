import psycopg2
import mysql.connector
import pyodbc
from prettytable import PrettyTable


class DB:
  def __init__(self, file_name, type_bd):
    self.file_name = file_name
    self.type_bd = type_bd
    self.cursor=None
    self.connection = None

  def DB_connection(self):
    try:
      with open(self.file_name, encoding='UTF-8') as file:
        try:
          match self.type_bd:
            case '1':
              self.connection = psycopg2.connect(
                database=file.readline().strip(),
                user=file.readline().strip(),
                password=file.readline().strip(),
                host=file.readline().strip(),
                port=file.readline().strip())


              print("База подключена")
            case '2':
              self.connection = mysql.connector.connect(
                host=file.readline().strip(),
                user=file.readline().strip(),
                passwd=file.readline().strip(),
                db=file.readline().strip())

              print("База подключена")
            case  '3':
              self.connection = pyodbc.connect(f"Driver={file.readline().strip()};"
                                               f"Server={file.readline().strip()};"
                                               f"Database={file.readline().strip()};"
                                               f"Trusted_Connection={file.readline().strip()};")


              print("База подключена")
            case _:
              print(
                'Вендор в данный момент не поддерживается. Список доступных вендоров: 1-postgres, 2-MySQL, 3-MSserver')
              exit(0)
          self.cursor = self.connection.cursor()

        except (psycopg2.OperationalError, mysql.connector.errors.DatabaseError, pyodbc.InterfaceError):
            print("Некорректные данные\nПрограмма закрыта")
            exit(0)

    except FileNotFoundError:
      print("Файл не найден")
      exit(0)

def main():
  print('Если хотите посмотреть название таблиц, то введите ключ -a после названия файла, по умолчанию введите -p')
  print('Введите \q для выхода')

  try:
   print("Введите название файла, ключ и номер вендора 1-postgres, 2-MySQL, 3-MSserver:")
   input_data = input().split()
  except KeyboardInterrupt:
    print('\nПрограмма закрыта')
    exit(0)

  try:
    file_name = input_data[0]
    key = input_data[1]
    type_bd=input_data[2]
    user=DB(file_name,type_bd)
    user.DB_connection()
  except IndexError:
    print('Нехватает данных, программа закрыта')
    exit(0)

  if key == '-a':
    print('Cписок доступных таблиц:')
    execute_query(user,"SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
  sql_request(user)

def sql_request(user):
  '''функция сбора запроса'''
  try:
    request_sql = ''
    while True:
      request_sql += input('SQL >> ') + '\n'
      if len(request_sql.rstrip()) > 0:
        if request_sql.rstrip()[-1] == ';':
          execute_query(user, request_sql)
          request_sql = ''
        elif request_sql.rstrip()[-2:] == '\q':
          print('\nПрограмма закрыта')
          user.connection.close()
          print("База отключена")
          exit(0)
        elif request_sql.rstrip()[-2:] == '\c' or request_sql.rstrip()[-6:] == '\clear':
          request_sql = ''
          print("Запрос стерся")
  except KeyboardInterrupt:
    print('\nПрограмма закрыта')
    user.connection.close()
    print("База отключена")

def execute_query(user,query):
  '''функция отправки запроса'''
  try:
    user.cursor.execute(query)
    user.connection.commit()
    result = user.cursor.fetchall()
    show_table(result, user.cursor)
  except psycopg2.errors.InFailedSqlTransaction:
    user.connection.rollback()
  except psycopg2.ProgrammingError as err:
    if 'no results to fetch' in str(err):
      print('Нету данных для вывода!')
    else:
      print(err)

def show_table(result,cursor):
  t = PrettyTable([description[0] for description in cursor.description])
  for row in result:
    t.add_row([*row])
  print(t)

if __name__ == '__main__':
  main()
