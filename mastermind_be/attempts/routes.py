"""Routes for attempts"""

from flask import Blueprint, jsonify, request

from mastermind_be.attempts.helpers.checks import check_is_draw, check_spaces_vs_guessed_length, guessed_is_digit
from mastermind_be.attempts.helpers.general import set_multiplayer_game_info, handle_attempts, return_other_games, \
    set_single_player_game_info, set_game_info
from mastermind_be.attempts.models import Attempt

from mastermind_be.games.models import Game
from werkzeug.exceptions import NotFound, abort

attempts_routes = Blueprint('attempts_routes', __name__)


@attempts_routes.post("/<int:game_uid>")
def make_an_attempt(game_uid):
    """Makes an attempt on submitting a guess."""

    data = request.json
    guessed_number = data.get("guess")

    try:
        int(guessed_number)
    except ValueError as error:
        return jsonify("The value you entered is not considered an integer. Please enter a value only containing "
                       "numbers.")

    game = Game.query.get(game_uid)
    if game is None:
        message = return_other_games(game_uid)
        return jsonify(message)

    if game.status == "COMPLETED":
        game_serialized = game.serialize()

        game_winner = "No one" if game.winner is None else game.winner
        message = f"{game_winner} won! Please make a guess on another game."
        return jsonify(game=game_serialized, message=message), 200

    check_spaces_vs_guessed_length(game, guessed_number, game.spaces)
    guessed_is_digit(game, guessed_number)

    attempts_max = game.players_count * 10
    attempts_count = len(game.attempts)

    check_is_draw(game, attempts_count, attempts_max)

    [player1, player2] = set_game_info(game)

    try:
        [game_serialized, message] = handle_attempts(game, attempts_count, attempts_max, player1, player2, guessed_number)
        return jsonify(game=game_serialized, message=message), 201

    except ValueError:
        abort(500, description="Failed to make an attempt.")


@attempts_routes.get("/<int:game_uid>")
def get_past_attempts(game_uid):
    """Gets past attempts hints for the game."""

    past_attempts = Attempt.query.filter(Attempt.game_id == game_uid).order_by(Attempt.datetime_created.desc()).all()
    hints_info = [[attempt.guess, attempt.hint] for attempt in past_attempts]

    game = Game.query.get(game_uid)
    attempts_max = game.players_count * 10

    attempts_remaining = attempts_max - len(game.attempts)

    return jsonify(hints=hints_info, attempts_remaining=attempts_remaining)
