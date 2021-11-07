from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs

from .. import logger
from ..models import User
from ..schemas import UserSchema, AuthSchema


users = Blueprint('users', __name__)


@users.route('/login', methods=['POST'])
@use_kwargs(UserSchema(only=('login', 'password')))
@marshal_with(AuthSchema)
def login(**kwargs):
    try:
        user = User.authenticate(**kwargs)
        access_token = user.get_token()
    except Exception as error:
        logger.warning(
            f'Login failed with errors: {error}'
        )
        return {'message': str(error)}, 400
    return {'access_token': access_token}


@users.route('/signup', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def signup(**kwargs):
    try:
        user = User(**kwargs)
        user.save()
        access_token = user.get_token()
    except Exception as error:
        logger.warning(
            f'Signup failed with errors: {error}'
        )
        return {'message': str(error)}, 400
    return {'access_token': access_token}


@users.errorhandler(422)
def error_handler(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ['Invalid request'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
