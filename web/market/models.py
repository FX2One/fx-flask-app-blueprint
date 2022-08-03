from flask_login import UserMixin, AnonymousUserMixin, current_user
from flask import current_app
from market import db, create_app, flask_bcrypt, login_manager
from datetime import datetime, timezone, timedelta
import jwt

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(length=200), nullable=False)
    created_on = db.Column(db.DateTime(), index=True, default=datetime.now())
    budget = db.Column(db.Integer(), nullable=False, default=5000)
    items = db.relationship('Item',backref="users", lazy=True)
    authors = db.relationship('Post', backref="users", lazy=True)
    notes = db.relationship('Note', backref="users", lazy=True)
    reviews = db.relationship('Review', backref="users",lazy=True)
    cart = db.Column(db.Integer(),nullable=False, default=0)

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.Integer(), nullable=False, unique=True)
    description = db.Column(db.String(length=1000), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=60), nullable=False, unique=True)
    notation = db.Column(db.Text(), nullable=False)
    notation_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=60), nullable=False, unique=True)
    post = db.Column(db.Text(), nullable=False)
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    reviews = db.relationship('Review', backref="posts", lazy=True)

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer(), primary_key=True)
    review = db.Column(db.Text(), nullable=False)
    reviewer_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))



