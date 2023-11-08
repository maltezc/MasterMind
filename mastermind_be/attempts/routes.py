"""Routes for attempts"""

from flask import Blueprint, jsonify, request
from mastermind_be.database import db


attempts_routes = Blueprint('attempts_routes', __name__)

@attempts_routes.get