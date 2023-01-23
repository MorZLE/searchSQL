import psycopg2
import mysql.connector
import pyodbc
from prettytable import PrettyTable


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
  except IndexError:
    print('Нехватает данных, программа закрыта')
    exit(0)

  if type_bd=='1':
    connection_postgres(file_name)
  elif type_bd=='2':
    connection_MySQL(file_name)
  elif type_bd=='3':
    connection_msserver(file_name)
  else:
    print('Вендор в данный момент не поддерживается. Список доступных вендоров: 1-postgres, 2-MySQL, 3-MSserver')
    exit(0)

  if key == '-a':
    print('Cписок доступных таблиц:')
    execute_query(connection, "SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    sql_request(connection)

  sql_request(connection)

def connection_postgres(file_name):
  try:
    with open(file_name, encoding='UTF-8') as file:
      try:
          global connection
          connection = psycopg2.connect(
          database=file.readline().strip(),
          user=file.readline().strip(),
          password=file.readline().strip(),
          host=file.readline().strip(),
          port=file.readline().strip()
        )
      except psycopg2.OperationalError:
        print("Некорректные данные\nПрограмма закрыта")
        exit(0)
      else:
        print("База подключена")
  except FileNotFoundError:
    print("Файл не найден")
    exit(0)

def connection_MySQL(file_name):
  try:
    with open(file_name, encoding='UTF-8') as file:
      try:
          global connection
          connection = mysql.connector.connect(
          host=file.readline().strip(),
          user=file.readline().strip(),
          passwd=file.readline().strip(),
          db=file.readline().strip()
        )
      except mysql.connector.errors.DatabaseError:
         print("Некорректные данные\nПрограмма закрыта")
         exit(0)
      else:
         print("База подключена")
  except FileNotFoundError:
    print("Файл не найден")
    exit(0)

def connection_msserver(file_name):
  try:
    with open(file_name, encoding='UTF-8') as file:
      try:
        global connection
        connection = pyodbc.connect(f"Driver={file.readline().strip()};"
                                    f"Server={file.readline().strip()};"
                                    f"Database={file.readline().strip()};"
                                    f"Trusted_Connection={file.readline().strip()};")

      except pyodbc.InterfaceError:
        print("Некорректные данные\nПрограмма закрыта")
        exit(0)
      else:
        print("База подключена")
  except FileNotFoundError:
    print("Файл не найден")
    exit(0)


def sql_request(connection):
  '''функция сбора запроса'''
  try:
    request_sql = ''
    while True:
      request_sql += input('SQL >> ')
      if request_sql[-1] == ';':
        execute_query(connection, request_sql)
        request_sql = ''
      elif request_sql[-2:] == '\q':
        print('\nПрограмма закрыта')
        connection.close()
        print("База отключена")
        exit(0)
  except KeyboardInterrupt:
    print('\nПрограмма закрыта')
    connection.close()
    print("База отключена")

def execute_query(connection, query):
  '''функция отправки запроса'''
  cursor = connection.cursor()
  try:
    cursor.execute(query)
    connection.commit()
    result=cursor.fetchall()
    t = PrettyTable([description[0] for description in cursor.description])
    for row in result:
      t.add_row([*row])
    print(t)
  except psycopg2.ProgrammingError as err:
    if 'no results to fetch' in str(err):
      print('Нету данных для вывода!')
    else:
      print(err)


if __name__ == '__main__':
  main()
