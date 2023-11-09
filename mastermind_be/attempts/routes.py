"""Routes for attempts"""

from flask import Blueprint, jsonify, request
from mastermind_be.database import db
from mastermind_be.games.models import Game
from werkzeug.exceptions import NotFound, abort

attempts_routes = Blueprint('attempts_routes', __name__)


# TODO: make an attempt
@attempts_routes.post("/<int:game_uid")
def make_an_attempt(game_uid):
    """Makes an attempt on submitting a guess."""

    game = Game.query.get_or_404(game_uid)
    number_to_guess = game.number_to_guess

    data = request.json
    guessed_number = data.get("number")

    # check length
    if len(guessed_number) != game.spaces:
        return abort(400, f"Guess must be {game.spaces} numbers long!")

    # validate guessed number is a valid number.
    if not guessed_number.isdigit():
        return abort(400, "Not a valid number")

    try:
        # check if guessed_number matches the game_number
        valid_guess = int(guessed_number)

        # TODO: CHECK attempts count.
        attempts_max = game.players_count * 10
        if len(game.attempts) > 20:
            return abort(200, "No winner, Please try again")


        #  if yes, Celebrate and change the game status
        if valid_guess == number_to_guess:



            message = "You guessed the correct number!!"
            Game.increment_guess(game)

            # increment guesses

            # TODO: CHANGE GAME STATUS
            game.status = "WIN"
            game_serialized = game.serialize()

            return jsonify(game=game_serialized, message = message), 201

        # if too high, say too low, guess again!
        elif valid_guess > number_to_guess:
            # increment guesses
            # TODO: CHANGE GAME attempts
            # game.attempts += 1
            Game.increment_guess(game)

            game_serialized = game.serialize()
            message = "Your guess is too high. Guess again!"

            return jsonify(game=game_serialized, message=message), 201

        # if too low, say too high, guess again!
        elif valid_guess < number_to_guess:

            # increment guesses
            # TODO: CHANGE GAME attempts
            # game.attempts -= 1
            Game.increment_guess(game)

            game_serialized = game.serialize()
            message = "Your guess is too low. Guess again!"

            return jsonify(game=game_serialized, message=message), 201

    except ValueError:
        abort(500, description="Failed to make an attempt.")

