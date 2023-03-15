from flask import Flask, request, render_template, session, flash, redirect, url_for
from UserLogin import UserLogin
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
from flask_classful import FlaskView, route
import os
import re
from DB import DB
from authorization import Storage
from usecase import UseCase, UniqueUsernameCheckFailed, UserNotFound, DbNotFound



DATABASE = '/tmp/flsite.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager(app)
login_manager.login_view = 'FlaskApp:login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


class FlaskApp(FlaskView):
    author = Storage()
    logic = None

    def __init__(self):
        super().__init__()
        self.logic = UseCase()



    @login_manager.user_loader
    def load_user(self):
        print('load user', session['username'])
        return UserLogin().fromDB(session['username'])

    def index(self):
        if 'username' in session:
            return redirect(url_for('FlaskApp:work_db'))
        return render_template('index.html')

    @route('/login', methods=['POST', "GET"])
    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for('FlaskApp:work_db'))
        if request.method == "POST":
            session['username'] = request.form['username']
            login = request.form['username']
            passwd = request.form['password']
            rm = True if request.form.get('remainme') else False

            try:
                session['id'] = self.logic.identification(login, passwd)
            except UserNotFound:
                flash("Пользователь не найден")

            try:
                db_info = self.logic.get_user_db(login)[0]
            except DbNotFound:
                flash("Нету подключенных бд")

            self.logic.addDB(db_info)

            userlogin = UserLogin().create(login)
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('FlaskApp:work_db'))
        return render_template('login.html')

    @route('/register', methods=['POST', "GET"])
    def reg(self):
        if request.method == "POST":
            session['username'] = request.form['username']
            login = request.form['username']
            passwd = request.form['password']
            confirm_password = request.form['confirm_password']
            if login == '' or passwd == '':
                flash("Логин или пароль не могут быть пустыми")
                return render_template('register.html')
            if passwd == confirm_password:
                try:
                    self.logic.create_user(login, passwd)
                except UniqueUsernameCheckFailed:
                    flash("Имя пользователя занято")
                userlogin = UserLogin().create(session['username'])
                login_user(userlogin)
                return redirect(url_for('FlaskApp:creat_db'))
            else:
                flash("Пароли не совпадают")
        return render_template('register.html')


    @route('/createdb', methods=['POST', "GET"])
    @login_required
    def create_db(self):
        if request.method == "POST":
            vendr = request.form['vendor']
            info = request.form['info_db']
            if info:
                match vendr[1:-1]:
                    case "PostgreSQL":
                        db_info = re.sub('[:|@|/]', " ", info).split()
                        db_info.append('PostgreSQL')
                        database = db_info[4]
                    case "MySQL":
                        db_info = re.sub('[;| =|]', " ", info).split()
                        db_info.append('MySQL')
                        database = db_info[3]
                   #case "MSserver":
                   #    # добавить драйвер
                   #    s = re.sub('[;| =|>|<|]', " ", info).split()
                   #    for i in [1, 3, 5, 7]:
                   #        db_info.append(s[i])
                   #    db_info.append('MSserver')
                    case "SQLite":
                        db_info = info.strip().split()
                        db_info.append('SQLite')
                        database = db_info[0]

                self.user = DB(db_info)
                login = session['username']
                self.logic.send_user_db(db_info, login, database)
                return redirect(url_for('FlaskApp:work_db'))
            else:
                flash("Неверные данные подключения")
        return render_template('creatdb.html')

    @route('/work_db', methods=['POST', "GET"])
    @login_required
    def work_db(self):
        if request.method == "POST":
            request_sql = request.form['message']
            if request_sql != '':
                try:
                    res, desc = self.user.exec(request_sql)
                    self.author.hs_rs(request_sql, 'True')
                    return render_template('workdb.html', rows=res, des=desc)
                except TypeError:
                    self.author.hs_rs(request_sql, 'False')
                    flash("Некорректный запрос!")
            else:
                flash("Запрос не может быть пустым!")
        return render_template('workdb.html')



    @route('/history', methods=['POST', "GET"])
    @login_required
    def history(self):
        self.author.user_id = self.author.get_user_id()
        res, desc = self.author.out_rs()
        return render_template('history.html', rows=res, des=desc)



    @route('/dbname', methods=['POST', "GET"])
    @login_required
    def dbname(self):
        return render_template('dbname.html', rows=self.author.get_user_db())


    @route('/profile', methods=['POST', "GET"])
    @login_required
    def profile(self):
         return render_template('profile.html', name=session['username'])


    @route('/logout', methods=['POST', "GET"])
    @login_required
    def logout(self):
        logout_user()
        session.pop('username', None)
        return redirect('/')

    @route('/test')
    @login_required
    def test(self):
        return render_template('test.html')


@app.errorhandler(404)
def pageNot(error):
    return render_template('error.html'), 404

FlaskApp.register(app, route_base='/')


if __name__ == '__main__':
    app.run(debug=True)
