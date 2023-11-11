"""General helpers for games"""
from flask import jsonify

from mastermind_be.database import db
from mastermind_be.games.models import Game


def return_active_games():
    """
    Filter for and return active games in descending order by data_created

    :return:
    """

    active_games = Game.query.filter(Game.status == "ACTIVE").order_by(Game.datetime_created.desc()).all()
    return active_games

def nuke_db():
    """Deletes all tables in db to prep for reset."""

    # Attempt.query.delete()
    # Game.query.delete()
    db.drop_all()

    db.session.commit()
