
from flask import Blueprint, jsonify, request
from mastermind_be.database import db
games_routes = Blueprint('games_routes', __name__)



@games_routes.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'