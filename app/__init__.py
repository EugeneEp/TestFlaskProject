from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

if not app.debug:
    if not os.path.exists(Config.LOGGING_DIR):
        os.mkdir(Config.LOGGING_DIR)
    file_handler = RotatingFileHandler(Config.LOGGING_DIR + '/' + Config.LOGGING_FILE, maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(Config.LOGGING_FORMAT))
    file_handler.setLevel(Config.LOGGING_LEVEL)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(Config.LOGGING_LEVEL)
