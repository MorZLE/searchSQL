from flask import Flask, request, render_template, session, flash, redirect, url_for
import sqlite3 as sl
import os
import re
from DB import DB
from authorization import Storage
from table import show_table

DATABASE = '/tmp/flsite.db'
DEBUG = True


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
app.config['SECRET_KEY'] = '8b8b21bdebbf2c5cf5198e6d8f49b3c4a9eefe59'

user = None
author = Storage()
def web_con_db():
    connection = sl.connect(app.config['DATABASE'])
    connection.row_factory = sl.Row
    return connection


def web_create_db():
    db = web_con_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


@app.before_request
def before_request():
    pass



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', "GET"])
def login():
    global user
    if request.method == "POST":
        author.login = request.form['username']
        author.passwd = request.form['password']
        author.db_info = author.identification()
        if author.db_info:
            user = DB(author.db_info)
            author.user_id = author.get_user_id()
            if user.connect() == 'err':
                flash("Неверные данные подключения")
        else:
            flash("Пользователь не найден")
        return redirect(url_for('work_db'))
    return render_template('login.html')

@app.route('/test', methods=['POST', "GET"])
def test():
    return render_template('test.html')


@app.route('/register', methods=['POST', "GET"])
def register():
    if request.method == "POST":
        author.login = request.form['username']
        author.passwd = request.form['password']
        confirm_password = request.form['confirm_password']
        if author.passwd == confirm_password:
            if author.registration():
                return redirect(url_for('creat_db'))
            else:
                flash("Имя пользователя занято")
        else:
            flash("Пароли не совпадают")
    return render_template('register.html')


@app.route('/creatdb', methods=['POST', "GET"])
def creat_db():
    global user
    if request.method == "POST":
        vendr = request.form['vendor']
        info = request.form['info_db']
        if info:
            match vendr[1:-1]:
                case "PostgreSQL":
                    author.db_info = re.sub('[:|@|/]', " ", info).split()
                    author.db_info.append('PostgreSQL')
                case "MySQL":
                    author.db_info = re.sub('[;| =|]', " ", info).split()
                    author.db_info.append('MySQL')
                case "MSserver":
                    # добавить драйвер
                    s = re.sub('[;| =|>|<|]', " ", info).split()
                    for i in [1, 3, 5, 7]:
                        author.db_info.append(s[i])
                    author.db_info.append('MSserver')
                case "SQLite":
                    author.db_info = info.strip().split()
                    author.db_info.append('SQLite')
            user = DB(author.db_info)
            if user.connect():
                author.send_user_data()
                author.get_user_id()
                return redirect(url_for('work_db'))
            else:
                flash("Неверные данные подключения")
    return render_template('creatdb.html')

@app.route('/workdb', methods=['POST', "GET"])
def work_db():
    if user is None:
        return redirect(url_for('login'))
    if request.method == "POST":
        if 'req' in request.form:
            request_sql = request.form['message']
            author.hs_rs(request_sql)
            try:
                res, desc = user.exec(request_sql)
                return render_template('workdb.html', rows=res, des=desc)
            except TypeError:
                flash("Некорректный запрос!")
        elif 'exit' in request.form:
            return redirect(url_for('login'))
    return render_template('workdb.html')
@app.route('/history', methods=['POST', "GET"])
def history():
    if request.method == "POST":
        res, desc = author.out_rs()
        return render_template('history.html', rows=res, des=desc)
    return render_template('history.html')
if __name__ == '__main__':
    app.run(debug = True)
