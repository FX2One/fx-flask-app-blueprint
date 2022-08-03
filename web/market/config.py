import os
from decouple import config
basedir = os.path.abspath(os.path.dirname(__file__))

#needs import to establish connection with db
import psycopg2

class Config(object):

class DevelopmentConfig(Config):

class TestingConfig(Config):

class DebugConfig(Config):

class ProductionConfig(Config):


# Load all possible configurations
config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'debug': DebugConfig
}