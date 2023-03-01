import logging
from table import show_table
from readfile import readfile


def sql_request(user,author):
  """Функция сбора запроса."""
  try:
    request_sql = ''
    while True:
      request_sql += input('SQL >> ') + '\n'
      if len(request_sql.rstrip()) != 0:
        if request_sql.rstrip()[:9].lower() == 'exec file' and request_sql.rstrip()[-1] == ';':
          author.hs_rs(request_sql)
          res, desc = user.exec(readfile(request_sql.split()[-1][:-1]))
          show_table(res, desc)
        elif request_sql.startswith('\dt'):
          match user.Vendor:
            case 'PostgreSQL':
               res, desc = user.exec("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            case 'MySQL':
               res, desc = user.exec("SHOW TABLES")
            case 'MSserver':
               res, desc = user.exec("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            case 'SQLite':
               res, desc = user.exec("SELECT name FROM sqlite_master WHERE type='table';")
          show_table(res, desc)
        elif request_sql.startswith('\q'):
          logging.warning('\nПрограмма закрыта\nБаза отключена')
          user.connection.close()
          exit(0)
        elif request_sql.startswith('\c') or request_sql.startswith('\clear'):
          print("Запрос стерся")
        elif request_sql.upper().startswith("\HS") or request_sql.upper().startswith("\HISTORY"):
          print("Вывод всех запросов пользователя")
          author.out_rs()
        elif request_sql.upper().startswith("\REPEAT"):
          print("Повторение последнего запроса")
          txt = author.last_rs()
          res, desc = user.exec(txt)
          show_table(res, desc)
        elif request_sql.rstrip()[-1] == ';':
          author.hs_rs(request_sql.strip())
          res, desc = user.exec(request_sql)
          show_table(res, desc)
        request_sql = ''
  except TypeError:
    print("Ошибка в запросе")
    sql_request(user, author)

  except KeyboardInterrupt:
    logging.warning('\nПрограмма закрыта\nБаза отключена')
    user.connection.close()




