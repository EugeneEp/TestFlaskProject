import datetime
import functools
from app import app, api, db
from app.v1 import errors as err
from app.v1.models import User, auth_fields, create_user, update_user
from flask import request
from http import HTTPStatus
import sqlalchemy as sa
import jwt
from flask_restx import Resource

v1 = api.namespace('api/v1', description='Api v1 operations')

# Декоратор для проверки api токена

def token_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.authorization
        if not access_token:
            return err.New(err.ERR_TOKEN_MISSING, HTTPStatus.FORBIDDEN)
        if 'Bearer' not in str(access_token):
            return err.New(err.ERR_AUTH_METHOD_NOT_ALLOWED, HTTPStatus.METHOD_NOT_ALLOWED)
        try:
            jwt.decode(access_token.token, app.config['SECRET_KEY'], algorithms="HS256")
        except Exception:
            return err.New(err.ERR_TOKEN_INVALID, HTTPStatus.FORBIDDEN)
        return func(*args, **kwargs)

    return wrapper


# Функция для генерации api токена
def token_generate(username, expired, secret_key):
    return jwt.encode(
        {
            'user': username,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=expired)
        }, secret_key
    )


@v1.route('/auth')
class Auth(Resource):
    # Метод создания api токена
    @v1.doc(description='Generate apiKey (username=admin / password=admin)', body=auth_fields)
    def post(self):
        data = request.get_json()
        if 'username' not in data or 'password' not in data:
            return err.New(err.ERR_REQUIRED_FIELD, HTTPStatus.BAD_REQUEST)
        if data['username'] == 'admin' and data['password'] == 'admin':
            access_token = token_generate(data['username'], app.config['JWT_EXPIRED_SECONDS'], app.config['SECRET_KEY'])
            return {'message': 'Authorized', 'status': True, 'body': [access_token]}, HTTPStatus.OK
        return err.New(err.ERR_JWT_VERIFY, HTTPStatus.UNAUTHORIZED)


@v1.route('/users')
class Users(Resource):
    # Метод создания User
    @v1.doc(description='Create a new user', body=create_user, security='api_key')
    @token_required
    def post(self):
        data = request.get_json()
        if 'username' not in data or 'password' not in data or 'email' not in data:
            return err.New(err.ERR_REQUIRED_FIELD, HTTPStatus.BAD_REQUEST)
        if data['username'] == '' or data['password'] == '' or data['email'] == '':
            return err.New(err.ERR_REQUIRED_FIELD, HTTPStatus.BAD_REQUEST)

        user = User(username=data['username'], email=data['email'], password=data['password'])
        if db.session.scalar(
                sa.select(User).where(User.email == user.email)
        ) is not None:
            return err.New(err.ERR_USER_EXISTS, HTTPStatus.BAD_REQUEST)

        db.session.add(user)
        db.session.commit()
        return {'message': 'User created', 'status': True, 'body': [user.to_dict()]}, HTTPStatus.CREATED

    # Метод получения всех существующих пользователей с пагинацией
    @v1.doc(description='Get Users List', security='api_key', params={
        'page': {'description': 'Page', 'in': 'query', 'type': 'int'},
        'per_page': {'description': 'Results per page', 'in': 'query', 'type': 'int'}
    })
    @token_required
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 1000, type=int)
        query = sa.select(User).order_by(User.timestamp.desc())
        users = db.paginate(query, page=page, per_page=per_page, error_out=False)
        body = []
        for user in users.items:
            body.append(user.to_dict())

        if not len(body):
            return err.New(err.ERR_USERS_NOT_FOUND, HTTPStatus.NOT_FOUND)

        return {'message': 'Users found', 'status': True, 'body': body}, HTTPStatus.OK


@v1.route('/users/<string:user_id>')
class OneUser(Resource):

    # Метод получения пользователя по id
    @v1.doc(description='Get User', security='api_key')
    @token_required
    def get(self, user_id):
        user = db.session.scalar(sa.select(User).where(User.id == user_id))
        if user is None:
            return err.New(err.ERR_USER_NOT_FOUND, HTTPStatus.NOT_FOUND)

        return {'message': 'User found', 'status': True, 'body': [user.to_dict()]}, HTTPStatus.OK

    # Метод обновления данных пользователя
    @v1.doc(description='Get User', body=update_user, security='api_key')
    @token_required
    def patch(self, user_id):
        data = request.get_json()
        user = db.session.scalar(sa.select(User).where(User.id == user_id))
        if user is None:
            return err.New(err.ERR_USER_NOT_FOUND, HTTPStatus.NOT_FOUND)
        if 'username' in data and data['username'] != '':
            user.username = data['username']
        if 'password' in data and data['password'] != '':
            user.set_password(data['password'])

        db.session.commit()
        return {'message': 'User updated', 'status': True, 'body': [user.to_dict()]}, HTTPStatus.OK

    # Метод удаления пользователя
    @v1.doc(description='Get User', security='api_key')
    @token_required
    def delete(self, user_id):
        user = db.session.scalar(sa.select(User).where(User.id == user_id))
        if user is None:
            return err.New(err.ERR_USER_NOT_FOUND, HTTPStatus.NOT_FOUND)

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted', 'status': True}, HTTPStatus.OK
