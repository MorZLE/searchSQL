import psycopg2
import mysql.connector
import pyodbc
import logging
from collecting import sql_request
from prettytable import PrettyTable
from table import show_table


class DB:
  def __init__(self, file_name, type_bd):
    self.file_name = file_name
    self.type_bd = type_bd
    self.cursor=None
    self.connection = None

  def connect(self):
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

            case '2':
              self.connection = mysql.connector.connect(
                host=file.readline().strip(),
                user=file.readline().strip(),
                passwd=file.readline().strip(),
                db=file.readline().strip())

            case  '3':
              self.connection = pyodbc.connect(f"Driver={file.readline().strip()};"
                                               f"Server={file.readline().strip()};"
                                               f"Database={file.readline().strip()};"
                                               f"Trusted_Connection={file.readline().strip()};")

            case _:
              print(
                'Вендор в данный момент не поддерживается. Список доступных вендоров: 1-postgres, 2-MySQL, 3-MSserver')
              exit(0)

          self.cursor = self.connection.cursor()
          print("База подключена")

        except (psycopg2.OperationalError, mysql.connector.errors.DatabaseError, pyodbc.InterfaceError):
            logging.error("Некорректные данные\nПрограмма закрыта")
            exit(0)

    except FileNotFoundError:
      logging.error(f"Файл {file_name} не найден")
      exit(0)

  def exec(self, query):
    '''функция отправки запроса'''
    try:
      self.cursor.execute(query)
      self.connection.commit()
      result = self.cursor.fetchall()
      t = PrettyTable([description[0] for description in self.cursor.description])
      show_table(result,t)
    except psycopg2.errors.InFailedSqlTransaction:
      self.connection.rollback()
    except psycopg2.ProgrammingError as err:
      if 'no results to fetch' in str(err):
        print('Нету данных для вывода!')
      else:
        print(err)


def main():
  print('Если хотите посмотреть название таблиц, то введите ключ -a после названия файла')
  print('Введите \q для выхода')

  try:
   print("Введите название файла номер вендора 1-postgres, 2-MySQL, 3-MSserver и ключ")
   input_data = input().split()
  except KeyboardInterrupt:
    print('\nПрограмма закрыта')
    exit(0)

  try:
    key=''
    if len(input_data)>2:
      key = input_data[2]
    file_name = input_data[0]
    type_bd = input_data[1]
    user=DB(file_name,type_bd)
    user.connect()
  except IndexError:
    print('Нехватает данных, программа закрыта')
    exit(0)

  if key == '-a':
    print('Cписок доступных таблиц:')
    user.exec("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
  sql_request(user)

if __name__ == '__main__':
  main()
