from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs


from ..models import Game
from .schema import GameSchema
from .. import logger

games = Blueprint('games', __name__, url_prefix='/games')


@games.route('/', methods=['GET'])
@marshal_with(GameSchema(many=True))
def get_games():
    try:
        games = Game.get_games()
    except Exception as error:
        logger.warning(
            f'Read failed with errors: {error}'
        )
        return {'message': str(error)}, 400
    return games


@games.route('/', methods=['POST'])
@use_kwargs(GameSchema)
@marshal_with(GameSchema)
def create_game(**kwargs):
    try:
        new_game = Game(**kwargs)
        new_game.save()
    except Exception as error:
        logger.warning(
            f'Create failed with errors: {error}'
        )
        return {'message': str(error)}, 400
    return new_game


@games.route('/<int:game_id>', methods=['PUT'])
@use_kwargs(GameSchema)
@marshal_with(GameSchema)
def update_game(game_id, **kwargs):
    try:
        print('Inside put')
        item = Game.get(game_id)
        item.update(**kwargs)
    except Exception as error:
        logger.warning(
            f'Create failed with errors: {error}'
        )
        return {'message': str(error)}, 400
    return item


@games.route('/<int:game_id>', methods=['DELETE'])
@marshal_with(GameSchema)
def delete_game(game_id):
    try:
        item = Game.get(game_id)
        item.delete()
    except Exception as error:
        logger.warning(
            f'Delete failed with errors: {error}'
        )
        return {'message': str(error)}, 400
    return '', 204


@games.errorhandler(422)
def error_handler(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ['Invalid request'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400