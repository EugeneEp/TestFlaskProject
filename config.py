import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres", pw="11111", url="localhost:5432",
                                                               db="test")
    SQLALCHEMY_TRACK_MODIFICATIONS = False