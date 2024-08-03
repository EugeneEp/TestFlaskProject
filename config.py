import os

POSTGRES_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres", pw="11111", url="localhost:5432",
                                                                     db="test")


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or POSTGRES_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'INFO'
    LOGGING_DIR = os.environ.get('LOGGING_DIR') or 'logs'
    LOGGING_FILE = os.environ.get('LOGGING_FILE') or 'test_flask_pj.log'
    LOGGING_FORMAT = os.environ.get('LOGGING_FORMAT') or '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
