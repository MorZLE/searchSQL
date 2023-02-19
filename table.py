from prettytable import PrettyTable


def show_table(result,desc):
    try:
        t = PrettyTable([description[0] for description in desc])
        for row in result:
            t.add_row([*row])
        print(t)
    except TypeError as err:
        if 'NoneType' in str(err):
            print('Данных для вывода нету!')
            start_new()
        else:
            print(err,'table')



