import logging
from authorization import Identi,last_rs,out_rs
from table import show_tb_name
from readfile import readfile


def sql_request(user,author):
  '''функция сбора запроса'''
  try:
    request_sql = ''
    while True:
      request_sql += input('SQL >> ') + '\n'
      if len(request_sql.rstrip()) != 0:
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
        elif request_sql.rstrip().upper()[:8] =="\HISTORY":
          print("Вывод всех запросов пользователя")
          show_tb_name(author.out_rs())
          request_sql = ''
        elif request_sql.rstrip().upper()[:7] =="\REPEAT":
          print("Повторение последнего запроса")
          txt=author.last_rs()
          user.exec(txt)
          request_sql = ''
        elif request_sql.rstrip()[-1] == ';':
          author.hs_rs(request_sql.strip())
          user.exec(request_sql)
          request_sql = ''

  except KeyboardInterrupt:
    logging.warning('\nПрограмма закрыта\nБаза отключена')
    user.connection.close()




