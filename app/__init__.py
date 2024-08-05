from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_restx import Api

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

authorizations = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api = Api(
    app,
    authorizations=authorizations,
    security='api_key',
    title='TestFlaskProject',
    version='1.0',
    default='API',
)

from app.v1.routes import v1

api.add_namespace(v1)

if not app.debug:
    if not os.path.exists(Config.LOGGING_DIR):
        os.mkdir(Config.LOGGING_DIR)
    file_handler = RotatingFileHandler(Config.LOGGING_DIR + '/' + Config.LOGGING_FILE, maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(Config.LOGGING_FORMAT))
    file_handler.setLevel(Config.LOGGING_LEVEL)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(Config.LOGGING_LEVEL)
