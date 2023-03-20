from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///D:/python/searchSQL/data_user_test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=True)


class Userdbs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_info = db.Column(db.Text, nullable=True)
    owner = db.Column(db.Text, db.ForeignKey('user.login'), nullable=True)
    dbName = db.Column(db.Text, nullable=True)
    vender = db.Column(db.Text, nullable=True)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request = db.Column(db.Text, nullable=True)
    time = db.Column(db.Text, nullable=True)
    condition = db.Column(db.Text, nullable=True)
    owner = db.Column(db.Text, db.ForeignKey('user.login'), nullable=True)

with app.app_context():
    db.create_all()
