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

    @property
    def budget_amount(self):
        return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}$"

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, plain_password):
        """password_hash is a String column which requires
        hashed password to be string not bytes in PostgreSQL"""
        self.password_hash = flask_bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, plain_password):
        return flask_bcrypt.check_password_hash(self.password_hash, plain_password)

    def generate_auth_token(self,expiration=36000):
        token = jwt.encode(
            {
                "confirm": self.id,
                "exp":datetime.now(timezone.utc) + timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return token

    def confirm(self, token):
        try:
            data = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=["HS256"])
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.email_confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.Integer(), nullable=False, unique=True)
    description = db.Column(db.String(length=1000), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __init__(self, name, price, barcode, description):
        self.name = name
        self.price = price
        self.barcode = barcode
        self.description = description

    def buy(self, user):
        self.user_id = user.id
        user.budget -= self.price
        user.cart += 1
        db.session.commit()

    def sell(self, user):
        self.user_id = None
        user.budget += self.price
        user.cart -= 1
        db.session.commit()

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=60), nullable=False)
    notation = db.Column(db.Text(), nullable=False)
    notation_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __init__(self, title, notation, notation_id):
        self.title = title
        self.notation = notation
        self.notation_id = notation_id

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=60), nullable=False)
    post = db.Column(db.Text(), nullable=False)
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    reviews = db.relationship('Review', backref="posts", lazy=True)

    def __init__(self,title,post, author_id):
        self.title = title
        self.post = post
        self.author_id = author_id

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer(), primary_key=True)
    review = db.Column(db.Text(), nullable=False)
    reviewer_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))

    def __init__(self,review,reviewer_id,post_id):
        self.review = review
        self.reviewer_id = reviewer_id
        self.post_id = post_id



