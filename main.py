import logging
from collecting import sql_request
from DB import DB
from authorization import Identi

def main():
  def start_new():
    print("Продолжить последнюю сессию?(д/н): д - по умолчанию")
    res = input().strip()
    try:
      author=Identi()
      if res.lower() == 'д' or res == "":
        data_bd = author.identification()
      elif res.lower() == 'н':
        data_bd = author.registration()
      else:
        start_new()
      user = DB(data_bd)
    except TypeError:
      print('Неверные данные')
      start_new()
    user.connect()
    sql_request(user,author)

  try:
    start_new()
  except KeyboardInterrupt:
    logging.error("Программа закрыта")
#postgres:111111@127.0.0.1:5432/demo
#Server=127.0.0.1;Database=test;UID=root;PWD=111111

if __name__ == '__main__':
  main()
