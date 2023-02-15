import psycopg2
import mysql.connector
import pyodbc
import logging
from prettytable import PrettyTable
from table import show_table



class DB:
  def __init__(self, data_bd):
    self.data_bd = data_bd
    self.type_bd = data_bd[-1]
    self.cursor=None
    self.connection = None

  def connect(self):
        try:
          match self.data_bd[-1]:
            case '1':
              self.connection = psycopg2.connect(
                database=self.data_bd[4],
                user=self.data_bd[0],
                password=self.data_bd[1],
                host=self.data_bd[2],
                port=self.data_bd[3])
              self.cursor = self.connection.cursor()
            case '2':
              try:
                self.connection = mysql.connector.connect(
                  user=self.data_bd[5],
                  password=self.data_bd[-2],
                  host=self.data_bd[1],
                  database=self.data_bd[3])
                self.cursor = self.connection.cursor(buffered=True)
              except Error as e:
                print(e)
            case  '3':
              self.connection = pyodbc.connect(f"Driver={self.data_bd[0]};"
                                               f"Server={self.data_bd[1]};"
                                               f"Database={self.data_bd[2]};"
                                               f"uid={self.data_bd[3]};"
                                               f"pwd={self.data_bd[4]}")

              self.cursor = self.connection.cursor()
          print("База подключена")

        except (psycopg2.OperationalError, mysql.connector.errors.DatabaseError, pyodbc.InterfaceError,IndexError):
            logging.error("Некорректные данные\nПрограмма закрыта")
            exit(0)

  def exec(self, query):
    '''функция отправки запроса'''
    try:
      self.cursor.execute(query.rstrip())
      self.connection.commit() #не работает с mysql
      result = self.cursor.fetchall()

      t = PrettyTable([description[0] for description in self.cursor.description])
      show_table(result,t)
    except (psycopg2.errors.InFailedSqlTransaction,mysql.connector.errors.ProgrammingError):
      self.connection.rollback()
    except TypeError:
      pass
    except (psycopg2.ProgrammingError,mysql.connector.errors.DataError,mysql.connector.errors.DatabaseError,mysql.connector.errors.ProgrammingError) as err:
      if 'no results to fetch' in str(err):
        print('Нету данных для вывода!')
      else:
        print(err)
