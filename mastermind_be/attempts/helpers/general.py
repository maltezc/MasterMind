"""general helpers for attempts"""

from mastermind_be.attempts.models import Attempt
from mastermind_be.games.models import Game


# TODO: SET UP COMPUTER GESSING ON 2 SECOND TIMER.

def handle_attempts(game, attempts_count, player1, player2, valid_guess):
    """Handles an attempt being made."""

    if attempts_count == 0 or attempts_count % 2 == 0:
        active_player = player1
        Game.player1_increment_guess(game)
        Attempt.make_attempt(game.id, valid_guess, player1["name"])
    else:
        active_player = player2
        Game.player2_increment_guess(game)
        Attempt.make_attempt(game.id, valid_guess, player2["name"])

    winner_bool = False

    #  if yes, Celebrate and change the game status
    number_to_guess = game.number_to_guess
    if valid_guess == number_to_guess:

        # increment guesses & set winner
        if active_player["number"] == 1:
            Game.set_winner_user1(game, player1["name"])
        elif active_player["number"] == 2:
            # Game.set_winner_user2(game, player2["name"])
            Game.set_winner_user1(game, player2["name"])

        winner_bool = True
        message = f"{active_player['name']}, You guessed the correct number!!"
        [game_serialized, message] = return_serialized_game_and_message(game, message, winner_bool)
        return [game_serialized, message]

    elif valid_guess > number_to_guess:
        message = f"{active_player['name']}, your guess is too high!"
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


def set_player_game_info(game):
    """Sets the player info for the game in dictionaries"""

    player1 = {
        "number": 1,
        "name": game.player1_name
    }

    player2 = {
        "number": 2,
        "name": game.player2_name
    }

    return [player1, player2]
