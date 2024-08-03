from werkzeug.exceptions import HTTPException

from app import app
import flask

ERR_CONTENT_TYPE = 'Content type is not supported'

ERR_USER_NOT_FOUND = 'User not found'
ERR_USERS_NOT_FOUND = 'Users not found'
ERR_USER_EXISTS = 'User with this email already exists'

ERR_REQUIRED_FIELD = 'Required field is missing'

ERR_JWT_VERIFY = 'Could not Verify'

ERR_TOKEN_MISSING = 'Token is missing'
ERR_TOKEN_INVALID = 'Token is invalid/expired'

ERR_AUTH_METHOD_NOT_ALLOWED = 'Auth method is not allowed'


def New(message, code):
    return flask.jsonify({'message': message, 'status': False}), code


@app.errorhandler(HTTPException)
def handle_exception(e):
    return flask.jsonify({'error': e.name, 'message': e.description, 'status': False}), e.code

