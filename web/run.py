from decouple import config
from market.config import config_dict
from market import create_app
import psycopg2


""".env file setup launches certain config mode
DEBUG=TRUE development mode
TESTING=TRUE along with DEBUG launch testing mode
both set to FALSE only for production!
inspired by https://pypi.org/project/python-decouple/"""


DEBUG = config('DEBUG', default=True, cast=bool)
TESTING = config('TESTING', default=False, cast=bool)


def config_msg(config_mode):
    return f'now you are in "{config_mode.upper()}" mode'


if TESTING:
    config_mode = 'testing'
    print(config_msg(config_mode))
elif DEBUG:
    config_mode = 'debug'
    print(config_msg(config_mode))
else:
    config_mode = 'production'
    print(config_msg(config_mode))


try:
    # Load the configuration using the default values
    app_config = config_dict[config_mode]

except KeyError:
    exit(
        'Error: Invalid <config_mode>. Expected values [Development,Testing or Production] ')


# loads decouple config into app object creation
app = create_app(app_config)


if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
