"""Routes for attempts"""

from flask import Blueprint, jsonify, request
from mastermind_be.database import db
from mastermind_be.games.helpers.general import return_serialized_game_and_message, handle_attempts, \
    check_spaces_vs_guessed_length, guessed_is_digit

from mastermind_be.games.models import Game
from werkzeug.exceptions import NotFound, abort

attempts_routes = Blueprint('attempts_routes', __name__)


# TODO: make an attempt
@attempts_routes.post("/<int:game_uid>")
def make_an_attempt(game_uid):
    """Makes an attempt on submitting a guess."""

    game = Game.query.get_or_404(game_uid)
    # number_to_guess = game.number_to_guess

    data = request.json
    guessed_number = data.get("guess")

    # check length
    check_spaces_vs_guessed_length(guessed_number, game.spaces)

    # validate guessed number is a valid number.
    guessed_is_digit(guessed_number)

    try:
        # check if guessed_number matches the game_number
        valid_guess = int(guessed_number)

        # TODO: CHECK attempts count.
        attempts_max = game.players_count * 10
        attempts_count = len(game.attempts)

        if attempts_count > attempts_max:
            return abort(200, "No winner. Looks like we have a draw!")

        player1 = {
            "number": 1,
            "name": game.player1_name
        }

        player2 = {
            "number": 2,
            "name": game.player2_name
        }

        [game_serialized, message] = handle_attempts(game, attempts_count, player1, player2, valid_guess)
        # TODO: NEED TO RETURN ACTIVE PLAYER, MIGHT NEED TO CREATE COLUMN.

        return jsonify(game=game_serialized, message=message), 201

    except ValueError:
        abort(500, description="Failed to make an attempt.")
