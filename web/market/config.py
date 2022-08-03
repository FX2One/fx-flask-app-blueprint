import os
from decouple import config
basedir = os.path.abspath(os.path.dirname(__file__))

#needs import to establish connection with db
import psycopg2

class Config(object):
    # Set up the App SECRET_KEY
    # generate really secure secret key here!
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_021!')
    APP_NAME = config('APP_NAME')
    FLASK_APP = config('FLASK_APP')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration
    EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX')
    EMAIL_SENDER = config('EMAIL_SENDER')
    MAIL_SERVER = config('MAIL_SERVER')
    MAIL_PORT = config('MAIL_PORT')
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    MAIL_USE_SSL = config('MAIL_USE_SSL')



class TestingConfig(Config):

class DebugConfig(Config):

class ProductionConfig(Config):


# Load all possible configurations
config_dict = {
    'testing': TestingConfig,
    'production': ProductionConfig,
    'debug': DebugConfig
}