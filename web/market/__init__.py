from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

#setup flask-login
login_manager.login_view = "account.login_page"
login_manager.login_message_category = 'info'


def extension_register(app):
    db.init_app(app)
    flask_bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


def blueprint_register(app):
    from market.account.views import account_bp
    app.register_blueprint(account_bp)

    from market.items.views import item_bp
    app.register_blueprint(item_bp)

    from market.notes.views import note_bp
    app.register_blueprint(note_bp)

    from market.posts.views import post_bp
    app.register_blueprint(post_bp)

    from market.posts_review.views import post_review_bp
    app.register_blueprint(post_review_bp)


def database_config(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    extension_register(app)
    blueprint_register(app)
    database_config(app)

    return app