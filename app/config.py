import os


class Config(object):
    DEBUG = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///D:/python/searchSQL/instance/data_user'
    SQLALCHEMY_TRACK_MODIFICATIONS = False