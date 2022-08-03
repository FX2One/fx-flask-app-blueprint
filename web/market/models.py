from flask_login import UserMixin, AnonymousUserMixin, current_user
from flask import current_app
from market import db, create_app, flask_bcrypt, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

class Item(db.Model):
    __tablename__ = 'items'

class Note(db.Model):
    __tablename__ = 'notes'

class Post(db.Model):
    __tablename__ = 'posts'

class Review(db.Model):
    __tablename__ = 'reviews'



