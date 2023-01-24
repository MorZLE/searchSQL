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
          if self.type_bd == '1':
            self.connection = psycopg2.connect(
              database=file.readline().strip(),
              user=file.readline().strip(),
              password=file.readline().strip(),
              host=file.readline().strip(),
              port=file.readline().strip())
            self.cursor = self.connection.cursor()
            print("База подключена")
          elif self.type_bd == '2':
            self.connection = mysql.connector.connect(
              host=file.readline().strip(),
              user=file.readline().strip(),
              passwd=file.readline().strip(),
              db=file.readline().strip())
            self.cursor = self.connection.cursor()
            print("База подключена")
          elif self.type_bd == '3':
            self.connection = pyodbc.connect(f"Driver={file.readline().strip()};"
                                             f"Server={file.readline().strip()};"
                                             f"Database={file.readline().strip()};"
                                             f"Trusted_Connection={file.readline().strip()};")
            self.cursor = self.connection.cursor()
            print("База подключена")
          else:
            print(
              'Вендор в данный момент не поддерживается. Список доступных вендоров: 1-postgres, 2-MySQL, 3-MSserver')
            exit(0)
        except (psycopg2.OperationalError, mysql.connector.errors.DatabaseError, pyodbc.InterfaceError):
          print("Некорректные данные\nПрограмма закрыта")
          exit(0)

    except FileNotFoundError:
      print("Файл не найден")
      exit(0)

  def sql_request(self):
    '''функция сбора запроса'''
    try:
      request_sql = ''
      while True:
        request_sql += input('SQL >> ')
        if request_sql[-1] == ';':
          self.execute_query(request_sql)  # я хуй знает че тут
          request_sql = ''
        elif request_sql[-2:] == '\q':
          print('\nПрограмма закрыта')
          self.connection.close()
          print("База отключена")
          exit(0)
        elif request_sql[-6:] == '\clear' or request_sql[-2:] == '\c':
          request_sql = ''
          print("Запрос стерся")

    except KeyboardInterrupt:
      print('\nПрограмма закрыта')
      self.connection.close()
      print("База отключена")

  def execute_query(self, query):
    '''функция отправки запроса'''
    try:
      self.cursor.execute(query)
      self.connection.commit()
      result = self.cursor.fetchall()
      show_table(result,self.cursor)
    except psycopg2.ProgrammingError as err:
      if 'no results to fetch' in str(err):
        print('Нету данных для вывода!')
      else:
        print(err)

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
    user.execute_query("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")

  user.sql_request()
def show_table(result,cursor):
  t = PrettyTable([description[0] for description in cursor.description])
  for row in result:
    t.add_row([*row])
  print(t)

if __name__ == '__main__':
  main()
