from werkzeug.exceptions import HTTPException

from app import api

ERR_CONTENT_TYPE = 'Content type is not supported'

ERR_USER_NOT_FOUND = 'User not found'
ERR_USERS_NOT_FOUND = 'Users not found'
ERR_USER_EXISTS = 'User with this email already exists'

ERR_REQUIRED_FIELD = 'Required field is missing'

ERR_JWT_VERIFY = 'Could not Verify'

ERR_TOKEN_MISSING = 'Token is missing'
ERR_TOKEN_INVALID = 'Token is invalid/expired'

ERR_AUTH_METHOD_NOT_ALLOWED = 'Auth method is not allowed'


# Функция формирования тела ответа ошибок
def New(message, code):
    return {'message': message, 'status': False}, code


# Изменение тела ответа стандартного обработчика ошибок
@api.errorhandler(HTTPException)
def handle_exception(e):
    return {'error': e.name, 'message': e.description, 'status': False}, e.code
