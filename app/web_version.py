from flask import Flask, request, render_template, session, flash, redirect, url_for,make_response
from logic.UserLogin import UserLogin
from flask_login import LoginManager, login_user, login_required, logout_user,current_user
from flask_classful import FlaskView, route
import os
import re
from DB.storage import Storage
from logic.usecase import UseCase, UniqueUsernameCheckFailed, UserNotFound, DbNotFound, DuplicateDB


DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

MAX_CONTENT_LENGTH = 1024 * 1024

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

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(FlaskApp, cls).__new__(cls)
        return cls.instance

    @login_manager.user_loader
    def load_user(self):
        return UserLogin().fromDB(session['username'])

    @route('/', methods=['POST', "GET"])
    def index(self):
        return redirect(url_for('FlaskApp:login'))

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
                return render_template('login.html')
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
                    return render_template('register.html')
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
            except DuplicateDB:
                flash("У вас уже есть база с этим именем")
                return render_template('createdb.html')
            self.logic.send_user_db(db_info, login, database)
            return redirect(url_for('FlaskApp:work_db'))
        return render_template('createdb.html')

    @route('/work_db', methods=['POST', "GET"])
    @login_required
    def work_db(self):
        username = session['username']
        if request.method == "POST":
            request_sql = request.form['message']
            if request_sql == '':
                flash("Запрос не может быть пустым!")
                return render_template('workdb.html')
            if not self.logic.check_active(username):
                flash("У вас нету активной бд!!!")
                return render_template('workdb.html')
            st, res, desc = self.logic.exec(request_sql, username)
            active = session['active']
            if st:
                self.logic.hs_rs(username, request_sql, 'True', active)
                if desc is None:
                    flash('Нету данных для вывода')
                    return render_template('workdb.html')
                return render_template('workdb.html', rows=res, des=desc)
            else:
                self.logic.hs_rs(username, request_sql, 'False', active)
                flash(f"Некорректный запрос!\n{res}")
        return render_template('workdb.html')

    @route('/table', methods=['POST', "GET"])
    @login_required
    def table(self):
        username = session['username']
        try:
            namedb = self.logic.print_table(session['username'], session['active'])
        except(IndexError, KeyError):
            flash('Выберите активную базу')
            return redirect(url_for('FlaskApp:dbname'))

        if request.method == 'POST':
            try:
                table = request.form['table']
            except KeyError:
                return render_template("table.html", namedb=namedb)
            _, res, desc = self.logic.exec(f'SELECT * FROM {table}', username)
            return render_template("table.html", rows=res, des=desc, namedb=namedb)
        return render_template("table.html", namedb=namedb)

    @route('/history', methods=['POST', "GET"])
    @login_required
    def history(self):
        if request.method == 'POST':
            self.logic.clear_hs_user(session['username'])
        res, desc = self.logic.out_rs(session['username'])
        return render_template('history.html', rows=res, des=desc)

    @route('/dbname', methods=['POST', "GET"])
    @login_required
    def dbname(self):
        if request.method == "POST":
            username = session['username']
            if request.form.get('submit') == 'Подключиться':
                if request.form.getlist('namedb') != []:
                    namedb = request.form.getlist('namedb')[0]
                    session['active'] = namedb
                    self.logic.connDB(username, namedb)
            elif request.form.get('delete') == 'Удалить':
                if request.form.getlist('namedb') != []:
                    self.logic.del_db_user(username, request.form.getlist('namedb')[0])
        try:
            return render_template('dbname.html', rows=self.logic.get_user_db(session['username']))
        except DbNotFound:
            return render_template('dbname.html', rows=[])


    @route('/profile', methods=['POST', "GET"])
    @login_required
    def profile(self):
        all, true, statistics = self.logic.get_statistics_user(session['username'])
        return render_template('profile.html', name=session['username'], statistics=statistics, tr=true, all=all)

    @route('/upload', methods=['POST', "GET"])
    @login_required
    def upload(self):
        if request.method == 'POST':
            file = request.files['file']
            if file and self.logic.verifyExt(file.filename):
                try:
                    img = file.read()
                    res = self.logic.updateUserAvatar(img,session['username'])
                    if not res:
                        flash("Ошибка обновления аватара", "error")
                        return redirect(url_for('profile'))
                    flash("Аватар обновлен", "success")
                except FileNotFoundError as e:
                    flash("Ошибка чтения файла", "error")
            else:
                flash("Ошибка обновления аватара", "error")
        return redirect(url_for('profile'))

    @route('/userava', methods=["POST", "GET"])
    @login_required
    def userava(self):
        img = self.logic.get_avatar(session['username'])
        if img == '':
            return ""
        h = make_response(img)
        h.headers['Content-Type'] = 'image/png'
        return h


    @route('/setpsw', methods=['POST', "GET"])
    @login_required
    def setpsw(self):
        if request.method == "POST":
            username = session['username']
            oldpasswd = request.form['oldpassword']
            passwd = request.form['password']
            confirm_password = request.form['confirm_password']
            if passwd == '' or oldpasswd =='' or confirm_password =='':
                flash("Пароль не может быть пустым")
                return render_template('setpsw.html')
            if not self.logic.check_psw_user(username,oldpasswd):
                flash("Старый пароль не верен!")
                return render_template('setpsw.html')
            if passwd != confirm_password:
                flash("Пароли не совпадают")
                return render_template('setpsw.html')
            self.logic.set_user_psw(username, passwd)
            flash("Пароль изменен")
            return redirect(url_for('FlaskApp:profile'))
        return render_template('setpsw.html')

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
    return render_template('error.html', err=404)

app.errorhandler(500)
def err(error):
    return render_template('error.html', err=500)

FlaskApp.register(app, route_base='/')


if __name__ == '__main__':
    app.run()
