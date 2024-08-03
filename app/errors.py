from werkzeug.exceptions import HTTPException

from app import app
import flask

ERR_CONTENT_TYPE = 'Content type is not supported'

ERR_USER_NOT_FOUND = 'User not found'
ERR_USERS_NOT_FOUND = 'Users not found'
ERR_USER_EXISTS = 'User with this email already exists'

ERR_REQUIRED_FIELD = 'Required field is missing'


def New(message, code):
    return flask.jsonify({'message': message, 'status': False}), code


@app.errorhandler(HTTPException)
def handle_exception(e):
    return flask.jsonify({'error': e.name, 'message': e.description, 'status': False}), e.code

