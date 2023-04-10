from flask import Flask, request, render_template, session, flash, redirect, url_for,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)