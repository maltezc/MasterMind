"""Game routes"""

import os
import requests
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound, abort

from mastermind_be import games
from mastermind_be.database import db
from mastermind_be.games.models import Game

games_routes = Blueprint('games_routes', __name__)


# Create
@games_routes.post("/")
def create_game():
    """Creating a game and initializing a db."""

    # TODO: GET USER INPUT
    data = request.json
    spaces = data.get('spaces')

    try:
        parsed_number = int(spaces)

        if parsed_number < 4 or parsed_number > 7:  # TODO: return this to the front end.
            print("value must be a whole number between 4 and 7")
            abort(400, "Value must be between 4 and 7")

        # Reach out to API
        # Retrieve number
        int_generator_api_url = f"https://www.random.org/integers/?num={spaces}&min=0&max=9&col={spaces}&base=10&format=plain&rnd=new"

        res = requests.get(int_generator_api_url)
        generated_int = res.text.replace("\t", "").replace("\n", "")

        # Initiate GAME IN DB
        game = Game.create_game(
            number_to_guess=generated_int,
            spaces=spaces
        )

        serialized = game.serialize()
        return jsonify(game=serialized), 201
        # return f"creating a game with {generated_int}"

    except ValueError:
        abort(500, description="Failed to create game.")


# Read
@games_routes.get("/<int:game_uid>")
def get_game(game_uid):
    """Retrieves single game by uid from db"""

    # TODO: add user if time.
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


# Update
# none

# Delete
@games_routes.post("reset/")
def reset_game_data():
    """deletes all past game data"""

    db.drop_all()
    db.create_all()

    return jsonify("Reset completed"), 200


