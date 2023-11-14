"""Check functions for attempts"""
from flask import jsonify
from werkzeug.exceptions import NotFound, abort


def guessed_is_digit(game, guessed_number):
    """Checks if guessed input is a digit and returns error if not."""

    try:
        parsed_value = int(guessed_number)
    except ValueError:
        message = "Not a valid number"
        return jsonify(game=game, message=message)


    # if not guessed_number.isdigit():
    #     message = "Not a valid number"
    #     # return abort(400, "Not a valid number")
    #     return jsonify(game=game, message=message)


def spaces_in_range(game, guessed_number, spaces):
    """Checks if spaces match the length of the number guessed. Returns an error if they dont match."""

    if len(guessed_number) != spaces:
        message = f"Guess must be {spaces} numbers long!"
        return message
        # serialized_game = game.serialize()
        # return jsonify(game=serialized_game, message=message)


def check_is_draw(game, attempts_count, attempts_max):
    """Checks to see if we have reached a draw by the number of attempts reaching the max allowed."""

    if attempts_count > attempts_max:
        game_serialized = game.serialize()
        message = "Max number of attempts have been reached. Try another game!"
        return jsonify(game=game_serialized, message=message), 200



