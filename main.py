import psycopg2
def main():
  con = psycopg2.connect(
    database="demo",
    user="postgres",
    password="111111",
    host="127.0.0.1",
    port="5432"
  )

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
