from flask import Flask, request, render_template, session, flash, redirect, url_for
from UserLogin import UserLogin
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
import os
import re
from DB import DB
from authorization import Storage


DATABASE = '/tmp/flsite.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

@login_manager.user_loader
def load_user(user_id):
    print('load user', session['username'])
    return UserLogin().fromDB(author)


user = None
author = Storage()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('work_db'))
    return render_template('index.html')


@app.route('/login', methods=['POST', "GET"])
def login():
    global user
    if current_user.is_authenticated:
        return redirect(url_for('work_db'))
    if request.method == "POST":
        session['username'] = request.form['username']
        author.login = request.form['username']
        author.passwd = request.form['password']
        author.db_info = author.identification()
        rm = True if request.form.get('remainme') else False
        if author.db_info:
            user = DB(author.db_info)
            if user.connect() != 'err':
                userlogin = UserLogin().create(author)
                login_user(userlogin, remember=rm)
                return redirect(request.args.get('next') or url_for('work_db'))
            else:
                flash("Ошибка подключения")
        else:
            flash("Пользователь не найден")
    return render_template('login.html')


@app.route('/test', methods=['POST', "GET"])
@login_required
def test():
    return render_template('test.html')


@app.route('/register', methods=['POST', "GET"])
def register():
    if request.method == "POST":
        session['username'] = request.form['username']
        author.login = request.form['username']
        author.passwd = request.form['password']
        confirm_password = request.form['confirm_password']
        if author.login == '' or author.passwd == '':
            flash("Логин или пароль не могут быть пустыми")
        else:
            if author.passwd == confirm_password:
                if author.registration():
                    return redirect(url_for('creat_db'))
                else:
                    flash("Имя пользователя занято")
            else:
                flash("Пароли не совпадают")
    return render_template('register.html')


@app.route('/creatdb', methods=['POST', "GET"])
@login_required
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
            if author.registration():
                author.send_user_data(user.info.database)
            if user.connect():
                author.send_user_db(user.info.database)
                return redirect(url_for('work_db'))
            else:
                flash("Неверные данные подключения")
    return render_template('creatdb.html')




@app.route('/workdb', methods=['POST', "GET"])
@login_required
def work_db():
    if request.method == "POST":
        request_sql = request.form['message']
        if request_sql != '':
            try:
                res, desc = user.exec(request_sql)
                author.hs_rs(request_sql, 'True')
                return render_template('workdb.html', rows=res, des=desc)
            except TypeError:
                author.hs_rs(request_sql, 'False')
                flash("Некорректный запрос!")
        else:
            flash("Запрос не может быть пустым!")
    return render_template('workdb.html')



@app.route('/history', methods=['POST', "GET"])
@login_required
def history():
    author.user_id = author.get_user_id()
    res, desc = author.out_rs()
    return render_template('history.html', rows=res, des=desc)



@app.route('/dbname', methods=['POST', "GET"])
@login_required
def dbname():
    print(author.get_user_db())
    return render_template('dbname.html', rows=author.get_user_db())


@app.route('/profile', methods=['POST', "GET"])
@login_required
def profile():
     return render_template('profile.html', name=session['username'])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return redirect('/')

@app.errorhandler(404)
def pageNot(error):
    return render_template('error.html'), 404

def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug = True)
