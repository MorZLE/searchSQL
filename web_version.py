from flask import Flask, request, render_template, session, flash, redirect, url_for
from UserLogin import UserLogin
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
from flask_classful import FlaskView, route
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
login_manager.login_view = 'FlaskApp:login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


class FlaskApp(FlaskView):
    author = Storage()
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
            self.author.login = request.form['username']
            self.author.passwd = request.form['password']
            self.author.db_info = self.author.identification()
            print(self.author.login)
            rm = True if request.form.get('remainme') else False
            if self.author.db_info:
                self.user = DB(self.author.db_info)
                if self.user.connect() != 'err':
                    userlogin = UserLogin().create(self.author.login)
                    login_user(userlogin, remember=rm)
                    return redirect(request.args.get('next') or url_for('FlaskApp:work_db'))
                else:
                    flash("Ошибка подключения")
            else:
                flash("Пользователь не найден")
        return render_template('login.html')


    @route('/test')
    @login_required
    def test(self):
        return render_template('test.html')


    @route('/register', methods=['POST', "GET"])
    def reg(self):

        if request.method == "POST":
            session['username'] = request.form['username']
            self.author.login = request.form['username']
            self.author.passwd = request.form['password']
            self.confirm_password = request.form['confirm_password']
            if self.author.login == '' or self.author.passwd == '':
                flash("Логин или пароль не могут быть пустыми")
            else:
                if self.author.passwd == confirm_password:
                    if self.author.registration():
                        self.userlogin = UserLogin().create(self.author)
                        login_user(self.userlogin)
                        return redirect(url_for('FlaskApp:creat_db'))
                    else:
                        flash("Имя пользователя занято")
                else:
                    flash("Пароли не совпадают")
        return render_template('register.html')


    @route('/createdb', methods=['POST', "GET"])
    @login_required
    def create_db(self):
        if request.method == "POST":
            self.vendr = request.form['vendor']
            self.info = request.form['info_db']
            if self.info:
                match self.vendr[1:-1]:
                    case "PostgreSQL":
                        self.author.db_info = re.sub('[:|@|/]', " ", self.info).split()
                        self.author.db_info.append('PostgreSQL')
                    case "MySQL":
                        self.author.db_info = re.sub('[;| =|]', " ", self.info).split()
                        self.author.db_info.append('MySQL')
                    case "MSserver":
                        # добавить драйвер
                        s = re.sub('[;| =|>|<|]', " ", info).split()
                        for i in [1, 3, 5, 7]:
                            self.author.db_info.append(s[i])
                        self.author.db_info.append('MSserver')
                    case "SQLite":
                        self.author.db_info = self.info.strip().split()
                        self.author.db_info.append('SQLite')
                self.user = DB(self.author.db_info)
                if self.author.registration():
                    self.author.send_user_data(self.user.info.database)
                if self.user.connect():
                    self.author.send_user_db(self.user.info.database)
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

    def test(self):
        return render_template('test.html')
@app.errorhandler(404)
def pageNot(error):
    return render_template('error.html'), 404

FlaskApp.register(app, route_base='/')




if __name__ == '__main__':
    app.run(debug=True)
