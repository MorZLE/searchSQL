import unittest
from DB import DB
from table import show_table
from authorization import Storage


class sqliteTest(unittest.TestCase):
    def setUp(self):
        self.user = DB(['test', 'SQLite'])
        self.author = Storage()
    def test_connect_db(self):
        self.user.connect()

    def test_create_table(self):
        print("\nСоздание таблицы")
        self.user.connect()
        self.user.exec(
            'CREATE TABLE USER (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, login text, password text, db_info text)')
        res, desc = self.user.exec("SELECT name FROM sqlite_master WHERE type='table'")
        show_table(res, desc)

    def test_reg_user(self):
        print('\nРегистрация пользователя')
        self.user.connect()
        self.author.registration()
        self.author.send_user_data()
        res, desc = self.author.exec('select * from USER')
        show_table(res, desc)
        res, desc = self.author.exec("DROP TABLE USER")

    def test_del_table(self):
        print('\nУдаление таблицы')
        self.user.connect()
        self.user.exec("DROP TABLE USER;")

        res, desc = self.user.exec("SELECT name FROM sqlite_master WHERE type='table'")
        show_table(res, desc)

if __name__ == '__main__':
    unittest.main()