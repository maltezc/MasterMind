"""General helpers for games"""
from flask import jsonify

from mastermind_be.database import db
from mastermind_be.attempts.models import Attempt
from mastermind_be.games.models import Game
from werkzeug.exceptions import NotFound, abort


def handle_attempts(game, attempts_count, player1, player2, valid_guess):
    """Handles an attempt being made."""

    if attempts_count == 0 or attempts_count % 2 == 0:
        active_player = player1
        Game.player1_increment_guess(game)
        Attempt.make_attempt(game.id, valid_guess)
    else:
        active_player = player2
        Game.player2_increment_guess(game)
        Attempt.make_attempt(game.id, valid_guess)

    winner_bool = False

    #  if yes, Celebrate and change the game status
    number_to_guess = game.number_to_guess
    if valid_guess == number_to_guess:

        # increment guesses & set winner
        if active_player["number"] == 1:
            Game.set_winner_user1(game)
        elif active_player["number"] == 2:
            Game.set_winner_user2(game)

        winner_bool = True
        message = f"{active_player['name']}, You guessed the correct number!!"
        [game_serialized, message] = return_serialized_game_and_message(game, message, winner_bool)
        return [game_serialized, message]

    elif valid_guess > number_to_guess:
        message = f"{active_player['name']}, your guess is too high.!"
        [game_serialized, message] = return_serialized_game_and_message(game, message, winner_bool)
        return [game_serialized, message]

    elif valid_guess < number_to_guess:
        message = f"{active_player['name']}, your guess is too low!"
        [game_serialized, message] = return_serialized_game_and_message(game, message, winner_bool)
        return [game_serialized, message]


def return_serialized_game_and_message(game, message, winner_bool):
    """returns serialized game and message"""

    if winner_bool:
        Game.set_status_completed(game)
    game_serialized = game.serialize()

    return [game_serialized, message]


def guessed_is_digit(guessed_number):
    """Checks if guessed input is a digit and returns error if not."""

    if not guessed_number.isdigit():
        return abort(400, "Not a valid number")


def check_spaces_vs_guessed_length(guessed_number, spaces):
    """Checks if spaces match the length of the number guessed. Returns an error if they dont match."""

    if len(guessed_number) != spaces:
        return abort(400, f"Guess must be {spaces} numbers long!")


def nuke_db():
    """Deletes all tables in db to prep for reset."""

    Attempt.query.delete()
    Game.query.delete()
    # db.drop_all()

    db.session.commit()
