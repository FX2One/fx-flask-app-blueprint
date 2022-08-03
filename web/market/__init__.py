from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

