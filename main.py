import logging
from collecting import sql_request
from DB import DB
from authorization import Storage 

def main():
  def start_new():
    print("Продолжить последнюю сессию?(д/н): д - по умолчанию")
    res = input().strip()
    try:
      author=Storage()
      if res.lower() == 'д' or res == "":
        data_db = author.identification()
      elif res.lower() == 'н' or res.lower() == 'y':
        data_db = author.registration()
      else:
        start_new()

      user = DB(data_db)

    except TypeError as err:
      print(err)
      start_new()

    while user.connect()=='err':
      print("Неверные данные подключения")
      data_db = author.registration()
      user = DB(data_db)
        
    author.rec_user_data()
    sql_request(user,author)

  try:
    start_new()
  except KeyboardInterrupt:
    logging.error("Программа закрыта")

if __name__ == '__main__':
  main()
