def readfile(name):
    try:
     with open(name, 'r', encoding='utf-8') as f:
        request_sql= f.read()
        return request_sql
     except FileNotFoundError:
        print("Файл не найден")
