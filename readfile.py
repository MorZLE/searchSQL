import logging
from authorization import hs_rs

def readfile(name):
    try:
        with open(name, 'r', encoding='utf-8') as f:
            request_sql= f.read()
        hs_rs(request_sql)
        return request_sql

    except FileNotFoundError:
          logging.error(f"Файл {name} не найден")
