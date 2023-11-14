"""Game routes"""

import requests
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

from mastermind_be.database import db
from mastermind_be.games.helpers.general import nuke_db, return_active_games
from mastermind_be.games.models import Game
import random

from mastermind_be.users.models import User

games_routes = Blueprint('games_routes', __name__)

easy = {
    "url": "https://www.random.org/integers/?num=4&min=0&max=7&col=4&base=10&format=plain&rnd=new",
    "spaces": '4'
}

medium = {"url": "https://www.random.org/integers/?num=5&min=0&max=7&col=5&base=10&format=plain&rnd=new",
          "spaces": "5"
          }

hard = {"url": "https://www.random.org/integers/?num=6&min=0&max=7&col=6&base=10&format=plain&rnd=new",
        "spaces": "6"
        }

legendary = {"url": "https://www.random.org/integers/?num=7&min=0&max=7&col=7&base=10&format=plain&rnd=new",
             "spaces": "7"
             }


# Create
@games_routes.post("/")
def create_game():
    """Creating a game and initializing a db."""

    data = request.json
    difficulty = data.get("difficulty", "easy")
    # player1_name = data.get('player1_name')
    # player2_name = data.get('player2_name', None)

    try:
        int_generator_api_url = None
        spaces = 4

        match difficulty:
            case "easy":
                int_generator_api_url = easy["url"]
                spaces = 4
            case "medium":
                int_generator_api_url = medium["url"]
                spaces = 5
            case "hard":
                int_generator_api_url = hard["url"]
                spaces = 6
            case "legendary":
                int_generator_api_url = legendary["url"]
                spaces = 7

        res = requests.get(int_generator_api_url)
        selected_num = res.text.replace("\t", "").replace("\n", "")

        if len(selected_num) != spaces:
            return jsonify("Uh oh, Something happened. Please try again.")

        string_num = selected_num
        int_num = int(selected_num)

        # users = []
        #
        # player1 = User.query.filter(User.name == "player1_name").first()
        # users.append(player1)

        # if player2_name is not None:
        #     player2 = User.query.filter(User.name == "player2_name").first()
        #     users.append(player2)

        # Initiate GAME IN DB

        game = Game.create_game(
            number_to_guess=selected_num,
            spaces=spaces,
            difficulty=difficulty,
            # users=users
            # player1_name=player1_name,
            # player2_name=player2_name,
        )

        serialized = game.serialize()
        return jsonify(game=serialized), 201

    except ValueError:
        abort(500, description="Failed to create game.")


@games_routes.post("/<int:game_uid>/add_user/<int:user_uid>")
def add_user_to_game(game_uid, user_uid):
    """Adds a user to a game"""

    game = Game.query.get(game_uid, None)

    if game is None:
        return jsonify("Game does not exist.")
    if game.player1 and game.player2:
        return jsonify("Cannot add any more players")
    if game.status != "SETUP":
        return jsonify("Game is not in setup mode anymore.")

    user = User.query.get(user_uid, None)
    if user is None:
        return jsonify("User does not exist.")

    if game.player1 is None:
        game.player1 = user
    elif game.player2 is None:
        game.player2 = user

    return game


# Read
@games_routes.get("/<int:game_uid>")
def get_game(game_uid):
    """Retrieves single game by uid from db"""

    game = Game.query.get_or_404(game_uid)

    serialized = game.serialize()
    return jsonify(game=serialized), 200


@games_routes.get("/")
def get_games():
    """Retrieves all games from db"""

    # TODO: add user if time.
    all_games = Game.query.all()

    serialized = [game.serialize() for game in all_games]
    return jsonify(games=serialized), 200


# get active games
@games_routes.get("/active")
def get_active_games():
    """Retrieves all active games from db"""

    active_games = return_active_games()

    serialized = [game.serialize() for game in active_games]
    return jsonify(games=serialized), 200


# get completed games
@games_routes.get("/completed")
def get_completed_games():
    """Retrieves all active games from db"""

    completed_games = Game.query.filter(Game.status == "COMPLETED").order_by(Game.datetime_completed.desc()).all()

    serialized = [game.serialize() for game in completed_games]
    return jsonify(games=serialized), 200


# Update
@games_routes.patch("<int:game_uid>")
def start_game(game_uid):
    """Changes the game status to active"""

    game = Game.query.get(game_uid, None)
    if game is None:
        return jsonify("Game does not exist.")

    Game.start_game(game)

    return game


# none

# Delete
@games_routes.post("reset/")
def reset_game_data():
    """deletes all past game data"""

    # db.drop_all()
    nuke_db()
    db.create_all()

    return jsonify("Reset completed"), 200
