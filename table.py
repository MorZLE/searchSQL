from prettytable import PrettyTable
def show_table(result,cursor):
  t = PrettyTable([description[0] for description in cursor.description])
  for row in result:
    t.add_row([*row])
  print(t)