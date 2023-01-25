from send import execute_query
from readfile import readfile

def sql_request(user):
  '''функция сбора запроса'''
  try:
    request_sql = ''
    while True:
      request_sql += input('SQL >> ') + '\n'
      if len(request_sql.rstrip()) > 0:
        if request_sql.rstrip()[:9].lower() == 'exec file' and request_sql.rstrip()[-1] == ';':
          execute_query(user, readfile(request_sql.split()[-1][:-1]))
          request_sql = ''
        elif request_sql.rstrip()[-1] == ';':
          execute_query(user, request_sql)
          request_sql = ''
        elif request_sql.rstrip()[-2:] == '\q':
          print('\nПрограмма закрыта')
          user.connection.close()
          print("База отключена")
          exit(0)
        elif request_sql.rstrip()[-2:] == '\c' or request_sql.rstrip()[-6:] == '\clear':
          request_sql = ''
          print("Запрос стерся")
  except KeyboardInterrupt:
    print('\nПрограмма закрыта')
    user.connection.close()
    print("База отключена")



