"""psycopg2 needs import to establish connection with postgres"""
import psycopg2
import os
from decouple import config
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Set up the App SECRET_KEY
    # generate really secure secret key here!
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_021!')
    APP_NAME = config('APP_NAME')
    FLASK_APP = config('FLASK_APP')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration
    EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX')
    EMAIL_SENDER = config('EMAIL_SENDER')
    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = config('MAIL_PORT')
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    MAIL_USE_SSL = config('MAIL_USE_SSL')


# Use while testing
class TestingConfig(Config):
    DEBUG = True
    TESTING = True

    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SQLALCHEMY_DATABASE_URI = config(
        'TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test_db.sqlite3')
    LOGIN_DISABLED = config('LOGIN_DISABLED')


# Use on development
class DebugConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config(
        'DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'dev_db.sqlite3')


# Use on production only
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3000
    FLASK_ENV = 'production'

    # PostgreSQL database
    # defaults does not work with docker-compose environment ,user only .env file vars or docker vars
    DB_ENGINE = config('DB_ENGINE', default='postgresql')
    DB_USERNAME = config('DB_USERNAME', default='testuser')
    DB_PASS = config('DB_PASS', default='testpass')
    DB_HOST = config('DB_HOST', default='localhost')
    DB_PORT = config('DB_PORT', default='5432')
    DB_NAME = config('DB_NAME', default='testdb')

    SQLALCHEMY_DATABASE_URI = f'{DB_ENGINE}://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# Load all possible configurations
config_dict = {
    'testing': TestingConfig,
    'production': ProductionConfig,
    'debug': DebugConfig
}
