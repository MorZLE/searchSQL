import psycopg2
import mysql.connector
import pyodbc
import sqlite3
from flask import flash


class Info:
    def __init__(self, data_db):
        self.data_db = data_db
        self.Vendor = data_db[-1]
        self.Driver = None
        self.Server = None
        self.password = None
        self.database = None
        self.host = None
        self.port = None
        self.user = None
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
        except (psycopg2.OperationalError, mysql.connector.errors.DatabaseError, pyodbc.InterfaceError, IndexError):
            self.isValid = False


class DB:
    def __init__(self, data_db):
        self.info = Info(data_db)
        self.connection = None
        self.cursor = None


    def connect(self):
        if self.info.isValid:
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
                    self.connection = sqlite3.connect(f'{self.info.database}', check_same_thread=False)
                    self.cursor = self.connection.cursor()
            return True
        else:
            return False

    def con_db_app(self):
        self.connection = sqlite3.connect('data_user', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.connection.execute('CREATE TABLE IF NOT EXISTS USER ('
                                ' id INTEGER PRIMARY KEY '
                                'AUTOINCREMENT NOT NULL, login text,'
                                'password text, db_info text);')

        self.connection.execute('CREATE TABLE IF NOT EXISTS history_rs '
                                '(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
                                'request text, '
                                'time INTEGER NOT NULL,'
                                'condition text'
                                'NOT NULL, user_id int);')

        self.connection.execute('CREATE TABLE IF NOT EXISTS userDBs( id INTEGER primary key,db_info TEXT not null,owner TEXT not null references USER (login),dbName  TEXT);')

        self.connection.commit()

    def web_con_db(self, app):
        self.connection = sqlite3.connect(app.config['DATABASE'])
        self.connection.row_factory = sqlite3.Row
        return self.connection
    def web_create_db(self, app):
        db = self.web_con_db(app)
        with app.open_resource('sq_db.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()

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
            print(te)
        except (psycopg2.ProgrammingError, mysql.connector.errors.DataError, mysql.connector.errors.DatabaseError,
                mysql.connector.errors.ProgrammingError,sqlite3.OperationalError,UnboundLocalError) as err:
            if 'no results to fetch' in str(err):
                print('Нету данных для вывода!')
            else:
                print(err)
                pass
