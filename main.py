import psycopg2


file_name=input("Имя файла: ")
def main():
  try:
    with open(file_name, encoding='UTF-8') as file:
      try:
        con = psycopg2.connect(
          database=file.readline().strip(),
          user=file.readline().strip(),
          password=file.readline().strip(),
          host=file.readline().strip(),
          port=file.readline().strip()
        )
      except psycopg2.OperationalError:
        print("Некорректные данные")
        exit(0)
      else:
        print("База подключена")
  except FileNotFoundError:
    print("Файл не найден")
    exit(0)
  print('Cписок доступных таблиц:')
  cur = con.cursor()
  cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ")
  rows = cur.fetchall()

  for row in rows:
    print(*row)

  con.close()
  print("База отключена")

if __name__ == '__main__':
  main()