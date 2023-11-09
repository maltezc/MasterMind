"""General helpers for games"""
from flask import jsonify

from mastermind_be.games.models import Game


def return_serialized_game_and_message(game, message):
    """returns serialized game and message"""

    Game.set_status_completed(game)
    game_serialized = game.serialize()

    return jsonify(game=game_serialized, message=message), 201
