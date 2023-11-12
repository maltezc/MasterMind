"""Check functions for attempts"""
from flask import jsonify
from werkzeug.exceptions import NotFound, abort


def guessed_is_digit(game, guessed_number):
    """Checks if guessed input is a digit and returns error if not."""

    if not guessed_number.isdigit():
        message = "Not a valid number"
        # return abort(400, "Not a valid number")
        return jsonify(game=game, message=message)


# TODO: ERROR IN BLOCK BELOW WHEN GUESSED NUMBER HAS MORE SPACES THAN GAME NUM.
def check_spaces_vs_guessed_length(game, guessed_number, spaces):
    """Checks if spaces match the length of the number guessed. Returns an error if they dont match."""

    if len(guessed_number) != spaces:
        message = f"Guess must be {spaces} numbers long!"
        return jsonify(game=game, message=message)


def check_is_draw(game, attempts_count, attempts_max):
    """Checks to see if we have reached a draw by the number of attempts reaching the max allowed."""

    if attempts_count > attempts_max:
        game_serialized = game.serialize()
        message = "Max number of attempts have been reached. Try another game!"
        return jsonify(game=game_serialized, message=message), 200



