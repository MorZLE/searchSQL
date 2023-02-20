import logging
from collecting import sql_request
from DB import DB
from authorization import Storage 

def main():
  def reg(author):
      data_db = author.registration()
      user = DB(data_db)
      while user.connect() == 'err':
        print("Неверные данные подключения")
        reg(author)
      author.send_user_data()
      return user
  def ind(author):
      data_db = author.identification()
      user = DB(data_db)
      user.connect()
      return user

  def start_new():
    print("Продолжить последнюю сессию?(д/н): д - по умолчанию")
    res = input().strip()
    try:
      author=Storage()
      if res.lower() == 'д' or res == "":
        user = ind(author)
      elif res.lower() == 'н' or res.lower() == 'y':
        user = reg(author)
      else:
        start_new()

    except TypeError as err:
      print('Пользователь не найден')
      start_new()
    author.get_user_id()
    sql_request(user,author)

  try:
    start_new()
  except KeyboardInterrupt:
    logging.error("Программа закрыта")


if __name__ == '__main__':
  main()
