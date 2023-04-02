import os

class Config(object):
    DEBUG = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///D:/python/searchSQL/instance/data_user'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIN_DB_CON_NAME = 'D:\\python\\searchSQL\\instance\\data_user'
    DB_PATH = 'D:\\python\\searchSQL\\app\\sqlitedb\\'
    MAX_CONTENT_LENGTH = 1024 * 1024
