import psycopg2
import mysql.connector
import pyodbc
import sqlite3
import logging
from app.config import Config


logging.basicConfig(level=logging.ERROR, filename="py_log.log",filemode="w")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

config = Config()

class DBerr(Exception):
    pass

class Info:
    Driver = ''
    Server = ''
    password = ''
    database = ''
    host = ''
    port = ''
    user = ''

    def __init__(self, data_db):
        self.data_db = data_db
        self.Vendor = data_db[-1]

        self.parse_connection_string()

    def parse_connection_string(self):
        try:
            match self.Vendor:
                case 'PostgreSQL':
                    self.database = self.data_db[4]
                    self.user = self.data_db[0]
                    self.password = self.data_db[1]
                    self.host = self.data_db[2]
                    self.port = self.data_db[3]
                case 'MySQL':
                    self.user =self.data_db[5]
                    self.password =self.data_db[-2]
                    self.host = self.data_db[1]
                    self.database = self.data_db[3]
                case 'MSserver':
                    self.Driver = self.data_db[0]
                    self.Server = self.data_db[1]
                    self.database = self.data_db[2]
                    self.user = self.data_db[3]
                    self.password = self.data_db[4]

                case 'SQLite':
                    self.database = self.data_db[0]
            self.isValid = True

        except (IndexError):
            self.isValid = False


class DB:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, data_db):
        self.info = Info(data_db)
        try:
            if not self.info.isValid:
                raise IndexError
            match self.info.Vendor:
                case 'PostgreSQL':
                    self.connection = psycopg2.connect(
                        database=self.info.database,
                        user=self.info.user,
                        password=self.info.password,
                        host=self.info.host,
                        port=self.info.port)
                    self.cursor = self.connection.cursor()
                case 'MySQL':
                    self.connection = mysql.connector.connect(
                        user=self.info.user,
                        password=self.info.password,
                        host=self.info.host,
                        database=self.info.database)
                    self.cursor = self.connection.cursor(buffered=True)
                case 'MSserver':
                    self.connection = pyodbc.connect(f"Driver={self.info.Driver};"
                                                     f"Server={self.info.Server};"
                                                     f"Database={self.info.database};"
                                                     f"uid={self.info.user};"
                                                     f"pwd={self.info.password}")
                    self.cursor = self.connection.cursor()
                case 'SQLite':
                    self.connection = sqlite3.connect(f'{config.DB_PATH}{self.info.database}', check_same_thread=False)
                    self.cursor = self.connection.cursor()
            return self.connection
        except (psycopg2.OperationalError, mysql.connector.errors.DatabaseError, pyodbc.InterfaceError, sqlite3.OperationalError):
            raise DBerr

    def con_db_app(self):
        self.connection = sqlite3.connect(config.MAIN_DB_CON_NAME, check_same_thread=False)
        self.cursor = self.connection.cursor()


    def exec(self, query, *args):
        """Функция отправки запроса"""
        try:
            self.cursor.execute(query, args)
            self.connection.commit()
            result = self.cursor.fetchall()
            return result, self.cursor.description
        except (psycopg2.errors.InFailedSqlTransaction, mysql.connector.errors.ProgrammingError):
            self.connection.rollback()
        except TypeError as te:
            logging.error(te)
        except (psycopg2.ProgrammingError, mysql.connector.errors.DataError, mysql.connector.errors.DatabaseError,
                mysql.connector.errors.ProgrammingError, sqlite3.OperationalError, UnboundLocalError) as err:
            if 'no results to fetch' in str(err):
                print('Нету данных для вывода!')
            else:
                logging.error(err)

    def userExec(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except (psycopg2.errors.InFailedSqlTransaction, mysql.connector.errors.ProgrammingError):
            connection.rollback()
        except (psycopg2.ProgrammingError, mysql.connector.errors.DataError, mysql.connector.errors.DatabaseError,
                mysql.connector.errors.ProgrammingError, sqlite3.OperationalError, UnboundLocalError, sqlite3.Warning,
                TypeError) as err:
            logging.error(err)
            connection.rollback()
            return False, err, False
        except Exception as err:
            logging.error(err)
            connection.rollback()
            return False, err, False

        connection.commit()
        result = cursor.fetchall()
        return True, result, cursor.description