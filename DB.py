import psycopg2
import mysql.connector
import pyodbc
import logging
import sqlite3 as sl
from table import show_table



class DB:
  def __init__(self,data_db):
    self.data_db = data_db
    self.Vendor = data_db[-1]
    self.cursor=None
    self.connection = None

  def connect(self):
    try:
      match self.Vendor:
        case 'PostgreSQL':
          self.connection = psycopg2.connect(
            database=self.data_db[4],
            user=self.data_db[0],
            password=self.data_db[1],
            host=self.data_db[2],
            port=self.data_db[3])
          self.cursor = self.connection.cursor()
        case 'MySQL':
          try:
            self.connection = mysql.connector.connect(
              user=self.data_db[5],
              password=self.data_db[-2],
              host=self.data_db[1],
              database=self.data_db[3])
            self.cursor = self.connection.cursor(buffered=True)
          except Error as e:
            print(e)
        case 'MSserver':
          self.connection = pyodbc.connect(f"Driver={self.data_db[0]};"
                                           f"Server={self.data_db[1]};"
                                           f"Database={self.data_db[2]};"
                                           f"uid={self.data_db[3]};"
                                           f"pwd={self.data_db[4]}")

          self.cursor = self.connection.cursor()
      print("База подключена")

    except (psycopg2.OperationalError, mysql.connector.errors.DatabaseError, pyodbc.InterfaceError, IndexError):
      logging.error("Некорректные данные\nПрограмма закрыта")
      '''Перезапуск функции старта из main'''
      exit(0)

  def con_db_app(self):
    self.connection = sl.connect('data_user.db')
    self.cursor = self.connection.cursor()
    self.connection.execute(
      'CREATE TABLE IF NOT EXISTS USER ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, login text, password text, db_info text);')
    self.connection.execute(
      'CREATE TABLE IF NOT EXISTS history_rs (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, request text, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, user_id int);')
    self.connection.commit()

  def exec(self, query, *args):
    '''функция отправки запроса'''
    try:
      self.cursor.execute(query, args)  # тут сделать вывод истории
      self.connection.commit()
      result = self.cursor.fetchall()
      return result, self.cursor.description
    except (psycopg2.errors.InFailedSqlTransaction, mysql.connector.errors.ProgrammingError):
      self.connection.rollback()
    except TypeError as te:
      print(te)
    except (psycopg2.ProgrammingError, mysql.connector.errors.DataError, mysql.connector.errors.DatabaseError,
            mysql.connector.errors.ProgrammingError) as err:
      if 'no results to fetch' in str(err):
        print('Нету данных для вывода!')
      else:
        print(err)
