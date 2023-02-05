import logging
from authorization import hs_rs,out_rs,last_rs
from table import show_tb_name
from readfile import readfile

def sql_request(user):
  '''функция сбора запроса'''
  try:
    request_sql = ''
    while True:
      request_sql += input('SQL >> ') + '\n'
      if len(request_sql.rstrip()) > 0:
        if request_sql.rstrip()[:9].lower() == 'exec file' and request_sql.rstrip()[-1] == ';':
          user.exec(readfile(request_sql.split()[-1][:-1]))
          request_sql = ''
        elif request_sql.rstrip()[:3] == '\dt':
          user.exec("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
          request_sql = ''
        elif request_sql.rstrip()[:2] == '\q':
          logging.warning('\nПрограмма закрыта\nБаза отключена')
          user.connection.close()
          exit(0)
        elif request_sql.rstrip()[-2:] == '\c' or request_sql.rstrip()[-6:] == '\clear':
          request_sql = ''
          print("Запрос стерся")
        elif request_sql.rstrip()[:7] =="HISTORY":
          print("Вывод всех запросов пользователя")
          show_tb_name(out_rs('history_rs'))
          request_sql = ''
        elif request_sql.rstrip()[:11] =="REPEAT LAST":
          print("Повторение последнего запроса")
          txt=last_rs()
          user.exec(txt)
          request_sql = ''
        elif request_sql.rstrip()[-1] == ';':
          hs_rs(request_sql.strip())
          user.exec(request_sql)
          request_sql = ''

  except KeyboardInterrupt:
    logging.warning('\nПрограмма закрыта\nБаза отключена')
    user.connection.close()




