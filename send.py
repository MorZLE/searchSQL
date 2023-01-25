import psycopg2
import mysql.connector
import pyodbc
from table import show_table
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
