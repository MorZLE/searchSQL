def show_table(result,t):
  for row in result:
    t.add_row([*row])
  print(t)