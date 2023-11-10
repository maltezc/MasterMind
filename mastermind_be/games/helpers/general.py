"""General helpers for games"""
from flask import jsonify

from mastermind_be.database import db


def nuke_db():
    """Deletes all tables in db to prep for reset."""

    # Attempt.query.delete()
    # Game.query.delete()
    db.drop_all()

    db.session.commit()
