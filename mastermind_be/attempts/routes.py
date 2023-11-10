"""Routes for attempts"""

from flask import Blueprint, jsonify, request

from mastermind_be.attempts.helpers.checks import check_is_draw, check_spaces_vs_guessed_length, guessed_is_digit
from mastermind_be.attempts.helpers.general import set_player_game_info, handle_attempts
from mastermind_be.database import db


from mastermind_be.games.models import Game
from werkzeug.exceptions import NotFound, abort

attempts_routes = Blueprint('attempts_routes', __name__)


# TODO: make an attempt
@attempts_routes.post("/<int:game_uid>")
def make_an_attempt(game_uid):
    """Makes an attempt on submitting a guess."""

    game = Game.query.get_or_404(game_uid)

    if game.status == "COMPLETED":
        game_serialized = game.serialize()
        message = f"This game is already completed. {game.winner} won! Please make a guess on another game."
        return jsonify(game=game_serialized, message=message), 201

    data = request.json
    guessed_number = data.get("guess")

    check_spaces_vs_guessed_length(guessed_number, game.spaces)

    guessed_is_digit(guessed_number)

    try:
        valid_guess = int(guessed_number)

        attempts_max = game.players_count * 10
        attempts_count = len(game.attempts)

        check_is_draw(attempts_count, attempts_max)

        [player1, player2] = set_player_game_info(game)

        [game_serialized, message] = handle_attempts(game, attempts_count, player1, player2, valid_guess)

        return jsonify(game=game_serialized, message=message), 201

    except ValueError:
        abort(500, description="Failed to make an attempt.")
