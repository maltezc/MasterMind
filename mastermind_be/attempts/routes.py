"""Routes for attempts"""

from flask import Blueprint, jsonify, request
from mastermind_be.database import db
from mastermind_be.games.helpers.general import return_serialized_game_and_message
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
        attempts_count = len(game.attempts)

        if attempts_count > attempts_max:
            return abort(200, "No winner, Please try again")

        player1 = {
            "number": 1,
            "name": game.player1_name
        }

        player2 = {
            "number": 2,
            "name": game.player2_name
        }

        if attempts_count == 0 or attempts_count % 2 == 0:
            active_player = player1
            Game.player1_increment_guess(game)
        else:
            active_player = player2
            Game.player2_increment_guess(game)

        #  if yes, Celebrate and change the game status
        if valid_guess == number_to_guess:

            # increment guesses & set winner
            if active_player["number"] == 1:
                Game.set_winner_user1(game)
            elif active_player["number"] == 2:
                Game.set_winner_user2(game)

            message = f"{active_player['name']}, You guessed the correct number!!"
            return_serialized_game_and_message(game, message)

        elif valid_guess > number_to_guess:
            message = f"{active_player['name']}, your guess is too high. Guess again!"
            return_serialized_game_and_message(game, message)

        elif valid_guess < number_to_guess:
            message = f"{active_player['name']}, your guess is too low. Guess again!"
            return_serialized_game_and_message(game, message)

    except ValueError:
        abort(500, description="Failed to make an attempt.")
