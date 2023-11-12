"""general helpers for attempts"""

from mastermind_be.attempts.models import Attempt
from mastermind_be.games.helpers.general import return_active_games
from mastermind_be.games.models import Game


def correct_number_guessed(game, active_player, player1, player2):
    """Sets the appropriate winner, and returns game serialized and appropriate message if the correct number is
    guessed."""

    # increment guesses & set winner
    if active_player["number"] == 1:
        Game.set_winner_user1(game, player1["name"])
    elif active_player["number"] == 2:
        Game.set_winner_user1(game, player2["name"])

    winner_bool = True
    message = f"{active_player['name']}, You guessed the correct number!!"
    [game_serialized, message] = return_serialized_game_and_message(game, message, winner_bool)
    return [game_serialized, message]


def handle_attempts(game, attempts_count, attempts_max,  player1, player2, valid_guess):
    """Handles an attempt being made."""

    active_player = None

    if not game.multiplayer:
        active_player = player1
        Game.player1_increment_guess(game)
        Attempt.make_attempt(game.id, valid_guess, player1["name"])

    elif game.multiplayer:
        if attempts_count == 0 or attempts_count % 2 == 0:
            active_player = player1
            Game.player1_increment_guess(game)
            Attempt.make_attempt(game.id, valid_guess, player1["name"])
        else:
            active_player = player2
            Game.player2_increment_guess(game)
            Attempt.make_attempt(game.id, valid_guess, player2["name"])

    if attempts_count >= attempts_max - 1:
        Game.set_status_completed(game)

    winner_bool = False
    number_to_guess = game.number_to_guess

    if valid_guess == number_to_guess:
        correct_number_guessed(game, active_player, player1, player2)

    correct_counter = check_positions(valid_guess, number_to_guess)

    message = resolve_message(correct_counter)

    [game_serialized, message] = return_serialized_game_and_message(game, message, winner_bool)
    return [game_serialized, message]


def resolve_message(correct_counter):
    """Assesses correct_number and returns message accordingly"""

    if correct_counter["number"] == 0 and correct_counter["location"] == 0:
        message = "All incorrect"
        return message

    else:
        correct_number_count = correct_counter["number"]
        numbers_word = 'number' if correct_number_count == 1 else 'numbers'

        correct_location_count = correct_counter["location"]
        locations_word = 'location' if correct_location_count == 1 else 'locations'
        message = f"{correct_number_count} correct {numbers_word} and {correct_location_count} correct {locations_word}"
        return message


def return_serialized_game_and_message(game, message, winner_bool):
    """
    Returns serialized game and message

    :param game:
    :param message:
    :param winner_bool:
    :return:
    """

    if winner_bool:
        Game.set_status_completed(game)
    game_serialized = game.serialize()

    return [game_serialized, message]


def set_single_player_game_info(game):
    """Sets the player info for a single player game"""

    player1 = {
        "number": 1,
        "name": game.player1_name
    }

    return player1


def set_multiplayer_game_info(game):
    """Sets the player info for a multiplayer game"""

    player1 = {
        "number": 1,
        "name": game.player1_name
    }

    player2 = {
        "number": 2,
        "name": game.player2_name
    }

    return [player1, player2]


def enumerate_and_check_splits(guess_splits, game_number_splits, correct_counter, found_numbers):
    """
    Enumerates the incoming guess values and check for position match to the game_number. If a matched number and
    position is found, the correct_counter number and the correct_counter location is incremented. if only the
    correct number is found, only correct_counter number is incremented.

    :param guess_splits:
    :param game_number_splits:
    :param correct_counter:
    :param found_numbers:
    :return:
    """

    for i, num in enumerate(guess_splits):
        if guess_splits[i] == game_number_splits[i]:
            correct_counter["number"] += 1
            correct_counter["location"] += 1

            found_numbers[num] = 1

        elif guess_splits[i] in game_number_splits:
            found_numbers[num] = 1
            correct_counter["number"] += 1

    return correct_counter


def check_positions(guess, game_number):
    """Check's positions of numbers from the guessed number against the game_number. Returns correct_counter
    dictionary that holds record of how many correct numbers and locations."""

    # Example Run:
    #     Game initializes and selects “0 1 3 5”
    #     Player guesses “2 2 4 6”, game responds “all incorrect”
    #     Player guesses “0 2 4 6”, game responds “1 correct number and 1 correct location”
    #     Player guesses “2 2 1 1”, game responds “1 correct number and 0 correct location”
    #     Player guesses “0 1 5 6”, game responds “3 correct numbers and 2 correct location”

    guess_splits = list(str(guess))
    game_number_splits = list(str(game_number))

    correct_counter = {
        "number": 0,
        "location": 0
    }

    found_numbers = {}

    enumerate_and_check_splits(guess_splits, game_number_splits, correct_counter, found_numbers)

    return correct_counter


def return_other_games(game_uid):
    """
    Returns message that contains other game_uid's for the user to try or try to create a new game."

    :param game_uid:
    :return:
    """

    active_games = return_active_games()
    if len(active_games) == 1:
        active_game_message = f" Try continuing game {active_games[0].id}"
    elif len(active_games) > 1:
        active_game_ids = [active_game.id for active_game in active_games]
        active_game_ids.reverse()
        game_ids = ", ".join(map(str, active_game_ids))
        active_game_message = f" Try continuing one of these games: {game_ids}"
    else:
        active_game_message = " Try creating a new game!"

    return f"Game #{game_uid} does not exist.{active_game_message}"
