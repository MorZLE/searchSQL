import psycopg2


def main():
  print('Если хотите посмотреть название таблиц, то введите ключ -a после названия файла')
  input_data = input("Введите название файла: ").split()

  if len(input_data) > 1:
    file_name = input_data[0]
    key = input_data[1]
  else:
    file_name = input_data[0]
    key = ''

  try:
    with open(file_name, encoding='UTF-8') as file:
      try:
          connection = psycopg2.connect(
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

  if key=='-a':
    print('Cписок доступных таблиц:')
    execute_query(connection, "SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    request_sql = ''
    while True:
      request_sql += input()
      if request_sql[-1] == ';':
        execute_query(connection, request_sql)
        request_sql = ''
  else:
    request_sql =''
    while True:
      request_sql += input()
      if request_sql[-1] ==';':
        print(request_sql)
        execute_query(connection, request_sql)
        request_sql =''

def execute_query(connection, query):
  cursor = connection.cursor()
  try:
    cursor.execute(query)
    connection.commit()
    result=cursor.fetchall()
    for row in result:
      print(*row)
  except psycopg2.ProgrammingError:
    print('Нету данных для вывода!')
  #    exit(0)
if __name__ == '__main__':
  main()

  #INSERT into actor VALUES (6666,'max','fdsdd','acd');
