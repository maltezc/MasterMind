"""Routes for users"""

import requests
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

from mastermind_be.database import db
from mastermind_be.games.helpers.general import nuke_db, return_active_games
from mastermind_be.games.models import Game
import random

from mastermind_be.users.models import User

users_routes = Blueprint('users_routes', __name__)


# Create
@users_routes.post("/")
def create_user():
    """Creating a user"""

    data = request.json
    name = data.get("name")

    if len(name) < 2:
        return jsonify("Name must be longer than 3 characters.")

    user = User.create_user(
        name=name
    )

    serialized_user = user.serialize()
    return jsonify(user=serialized_user), 201


# Read
@users_routes.get("/<int:user_id>")
def get_user(user_id):
    """Retrieves specified user per their id"""

    user = Game.query.get_or_404(user_id)

    user_serialized = user.serialize()

    return jsonify(user=user_serialized), 200


# get all
@users_routes.get("/")
def get_users():
    """Retrieves all users"""

    all_users = User.query.all()

    serialized_users = [user.serialize() for user in all_users]
    return jsonify(users=serialized_users), 200

