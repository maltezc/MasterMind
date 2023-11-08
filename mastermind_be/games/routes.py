"""Game routes"""

import os
import requests
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound, abort

from mastermind_be import games
from mastermind_be.database import db
from mastermind_be.games.models import Game

games_routes = Blueprint('games_routes', __name__)


# @games_routes.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

# TODO: create game
@games_routes.get("/")
def get_games():
    """Retrieves all games from db"""

    # TODO: add user if time.
    all_games = Game.query.all()

    serialized = [game.serialize() for game in all_games]
    return jsonify(games=serialized), 200


@games_routes.post("/")
def create_game():
    """Creating a game and initializing a db."""

    # TODO: GET USER INPUT
    data = request.json
    spaces = data.get('spaces')

    try:
        parsed_number = int(spaces)

        if parsed_number < 4 or parsed_number > 7: # TODO: return this to the front end.
            print("value must be a whole number between 4 and 7")
            abort(400, "Value must be between 4 and 7")

        # TODO: reach out to API
        # TODO: Retrieve number
        int_generator_api_url = f"https://www.random.org/integers/?num={spaces}&min=0&max=9&col={spaces}&base=10&format=plain&rnd=new"

        res = requests.get(int_generator_api_url)
        generated_int = res.text.replace("\t", "").replace("\n","")

        # TODO: INITIATE GAME IN DB
        game = Game.create_game(
            number_to_guess=generated_int,
            spaces=spaces
        )

        serialized = game.serialize()
        return jsonify(game=serialized), 201
        # return f"creating a game with {generated_int}"

    except ValueError:
        abort(500, description="Failed to create game.")


@games_routes.post("reset/")
def reset_game_data():
    """deletes all past game data"""

    db.drop_all()
    db.create_all()

    return jsonify("Reset completed"), 200

# TODO: make an attempt
