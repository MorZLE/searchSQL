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
        return UserLogin().fromDB(session['username'])

    def index(self):
        if 'username' in session:
            return redirect(url_for('FlaskApp:work_db'))
        return render_template('index.html')

    @route('/login', methods=['POST', "GET"])
    def login(self):
        print(self)
        if current_user.is_authenticated:
            return redirect(url_for('FlaskApp:work_db'))
        if request.method == "POST":
            session['username'] = request.form['username']
            login = request.form['username']
            passwd = request.form['password']
            rm = True if request.form.get('remainme') else False
            db_info = None
            try:
                session['id'] = self.logic.identification(login, passwd)
            except UserNotFound:
                flash("Пользователь не найден")
                return render_template('login.html')


            try:
                db_info = self.logic.get_user_data_db(login)[0]
                db_info = ''.join(db_info).split()
            except (IndexError, DbNotFound):
                flash("Нету подключенных бд")


            if db_info!=None:self.logic.addDB(db_info, session['username'])

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
                return redirect(url_for('FlaskApp:create_db'))
            else:
                flash("Пароли не совпадают")
        return render_template('register.html')


    @route('/createdb', methods=['POST', "GET"])
    @login_required
    def create_db(self):
        if request.method == "POST":
            vendr = request.form['vendor']
            info = request.form['info_db']
            try:
                match vendr[1:-1]:
                    case "PostgreSQL":
                        db_info = re.sub('[:|@|/]', " ", info).split()
                        db_info.append('PostgreSQL')
                        database = db_info[4]
                    case "MySQL":
                        db_info = re.sub('[;| =|]', " ", info).split()
                        db_info.append('MySQL')
                        database = db_info[3]
                    # case "MSserver":
                    #    # добавить драйвер
                    #    s = re.sub('[;| =|>|<|]', " ", info).split()
                    #    for i in [1, 3, 5, 7]:
                    #        db_info.append(s[i])
                    #    db_info.append('MSserver')
                    case "SQLite":
                        db_info = info.strip().split()
                        db_info.append('SQLite')
                        database = db_info[0]
            except IndexError:
                flash("Неверные данные подключения")
                return render_template('createdb.html')

            login = session['username']

            try:
                self.logic.addDB(db_info, login)
            except IndexError:
                flash("Неверные данные подключения")
                return render_template('createdb.html')

            self.logic.send_user_db(db_info, login, database)
            return redirect(url_for('FlaskApp:work_db'))


        return render_template('createdb.html')

    @route('/work_db', methods=['POST', "GET"])
    @login_required
    def work_db(self):
        print(self)
        if request.method == "POST":
            request_sql = request.form['message']
            if request_sql != '':
                try:
                    res, desc = self.logic.exec(request_sql, session['username'])
                    self.logic.hs_rs(session['username'], request_sql, 'True')
                    return render_template('workdb.html', rows=res, des=desc)
                except TypeError:
                    self.logic.hs_rs(session['username'], request_sql, 'False')
                    flash("Некорректный запрос!")
            else:
                flash("Запрос не может быть пустым!")
        return render_template('workdb.html')



    @route('/history', methods=['POST', "GET"])
    @login_required
    def history(self):
        res, desc = self.logic.out_rs(session['username'])
        return render_template('history.html', rows=res, des=desc)



    @route('/dbname', methods=['POST', "GET"])
    @login_required
    def dbname(self):
        try:
            return render_template('dbname.html', rows=self.logic.get_user_db(session['username']))
        except DbNotFound:
            return render_template('dbname.html', rows=[])

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
