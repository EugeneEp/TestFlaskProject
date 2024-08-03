import functools
import flask
from app import app, db, errors as err
from app.models import User
from flask import request, render_template
from http import HTTPStatus
import sqlalchemy as sa


@app.get('/')
@app.get('/index')
def index():
    return render_template('index.html', title='Home')


def json_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            return func(*args, **kwargs)
        else:
            return err.New(err.ERR_CONTENT_TYPE, HTTPStatus.BAD_REQUEST)

    return wrapper


@app.post('/api/users')
@json_required
def create_user():
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
    return flask.jsonify({'message': 'User created', 'status': True, 'body': [user.to_dict()]}), HTTPStatus.CREATED


@app.get('/api/users/<user_id>')
def get_user(user_id):
    user = db.session.scalar(sa.select(User).where(User.id == user_id))
    if user is None:
        return err.New(err.ERR_USER_NOT_FOUND, HTTPStatus.NOT_FOUND)

    return flask.jsonify({'message': 'User found', 'status': True, 'body': [user.to_dict()]}), HTTPStatus.OK


@app.get('/api/users')
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 1000, type=int)
    query = sa.select(User).order_by(User.timestamp.desc())
    users = db.paginate(query, page=page, per_page=per_page, error_out=False)
    body = []
    for user in users.items:
        body.append(user.to_dict())

    if not len(body):
        return err.New(err.ERR_USERS_NOT_FOUND, HTTPStatus.NOT_FOUND)

    return flask.jsonify({'message': 'Users found', 'status': True, 'body': body}), HTTPStatus.OK


@app.patch('/api/users/<user_id>')
@json_required
def update_user(user_id):
    data = request.get_json()
    user = db.session.scalar(sa.select(User).where(User.id == user_id))
    if user is None:
        return err.New(err.ERR_USER_NOT_FOUND, HTTPStatus.NOT_FOUND)
    if 'username' in data and data['username'] != '':
        user.username = data['username']
    if 'password' in data and data['password'] != '':
        user.set_password(data['password'])

    db.session.commit()
    return flask.jsonify({'message': 'User updated', 'status': True, 'body': [user.to_dict()]}), HTTPStatus.OK


@app.delete('/api/users/<user_id>')
def delete_user(user_id):
    user = db.session.scalar(sa.select(User).where(User.id == user_id))
    if user is None:
        return err.New(err.ERR_USER_NOT_FOUND, HTTPStatus.NOT_FOUND)

    db.session.delete(user)
    db.session.commit()
    return flask.jsonify({'message': 'User deleted', 'status': True}), HTTPStatus.OK
