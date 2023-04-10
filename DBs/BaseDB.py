from app.web_version import db,app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.BLOB, nullable=True)


class Userdbs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_info = db.Column(db.Text, nullable=True)
    owner = db.Column(db.Text, db.ForeignKey('user.login'), nullable=True)
    dbName = db.Column(db.Text, nullable=True)
    vender = db.Column(db.Text, nullable=True)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request = db.Column(db.Text, nullable=True)
    namedb = db.Column(db.Text, nullable=True)
    time = db.Column(db.Text, nullable=True)
    condition = db.Column(db.Text, nullable=True)
    owner = db.Column(db.Text, db.ForeignKey('user.login'), nullable=True)


with app.app_context():
    db.create_all()
