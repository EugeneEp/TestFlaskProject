import flask
from http import HTTPStatus

ERR_CONTENT_TYPE = 'Content type is not supported'

ERR_USER_NOT_FOUND = 'User not found'
ERR_USERS_NOT_FOUND = 'Users not found'
ERR_USER_EXISTS = 'User with this email already exists'


def New(message, code):
    return flask.jsonify({'message': message, 'status': False}), code