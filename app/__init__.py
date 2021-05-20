from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager(app)
db = SQLAlchemy(app)
from app.controller import default
