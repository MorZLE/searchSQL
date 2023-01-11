import psycopg2
file_name=input()
def main():
  with open(file_name, encoding='UTF-8') as file:
    try:
      con = psycopg2.connect(
        database=file.readline().strip(),
        user=file.readline().strip(),
        password=file.readline().strip(),
        host=file.readline().strip(),
        port=file.readline().strip()
      )
    except Exception:
      print("Некорректные данные")
    else:
      print("База подключена")
  cur = con.cursor()
  cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ")

  rows = cur.fetchall()
  for row in rows:
    print(*row)
  con.close()
  print("База отключена")
  pass

if __name__ == '__main__':
  main()