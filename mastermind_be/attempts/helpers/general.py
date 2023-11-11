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

    # TODO: check positions - The player had guessed a correct number and its correct location
    # split the guess and the game number.
    check_positions(valid_guess, number_to_guess) # TODO: test this.


    # check positions against eachother.


    # elif valid_guess > number_to_guess:
    #     message = f"{active_player['name']}, your guess is too high!"
    #     [game_serialized, message] = return_serialized_game_and_message(game, message, winner_bool)
    #     return [game_serialized, message]
    #
    # # TODO: The player’s guess was incorrect
    #
    # elif valid_guess < number_to_guess:
    #     message = f"{active_player['name']}, your guess is too low!"
    #     [game_serialized, message] = return_serialized_game_and_message(game, message, winner_bool)
    #     return [game_serialized, message]


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


def check_positions(guess, game_number):
    """Check's positions of numbers from the guessed number against the game_number."""

    '''Example Run:
        Game initializes and selects “0 1 3 5”
        Player guesses “2 2 4 6”, game responds “all incorrect”
        Player guesses “0 2 4 6”, game responds “1 correct number and 1 correct location”
        Player guesses “2 2 1 1”, game responds “1 correct number and 0 correct location”
        Player guesses “0 1 5 6”, game responds “3 correct numbers and 2 correct location”'''

    guess_splits = guess.split()
    game_number_splits = game_number.split()

    correct_counter = {
        "number": 0,
        "location": 0
    }

    found_numbers = {}

    #  could use for loop to check for numbers?
    for i, num  in enumerate(guess_splits) :
        if guess_splits[i] == game_number_splits[i]: # if numbers match
            # increment correct NUmber and location counter
            correct_counter["number"] =+1
            correct_counter["location"] =+1

            found_numbers[num] = 1
            # if both numbers match game number length, its a win
        # use some kind of dictionary counter.
        if guess_splits[i] in game_number_splits:
            found_numbers[num] = 1
            correct_counter["number"] = +1

    return [correct_counter, found_numbers]


    # if each position matches, “all incorrect”
    # if a number matches and a location matches, “1 correct number and 1 correct location”
    # if a number matches but no locations match, “1 correct number and 0 correct location”
    # if more than one position matches and more than 1 correct numbers match.




# test