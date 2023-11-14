"""models for users"""

from datetime import datetime
from sqlalchemy.orm import validates

from mastermind_be.database import db


class User(db.Model):
    """ Users table """

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    @validates("spaces")
    def validate_spaces(self, value):
        """validates number of spaces is between 4 and 7"""

        if len(value) < 2:
            raise ValueError("Name must be longer than 1 character")
        return value

    # games won
    # can filter for this

    # games
    player1_games = db.Relationship("Game", back_populates="player1", foreign_keys="Game.player1_id", uselist=True)
    player2_games = db.Relationship("Game", back_populates="player2", foreign_keys="Game.player2_id", uselist=True)

    # games = db.Relationship("Game", back_populates="user", foreign_keys="[Game.player1_id], [Game.player2_id]", uselist=True)

    # attempts
    attempts = db.Relationship("Attempt", back_populates="user", uselist=True)

    def serialize(self, deep=True):
        """returns self"""

        serialized_attempts = [attempt.serialize() for attempt in self.user.attempts]

        user_data = {
            "id": self.id,
            "name": self.name,
            "attempts": serialized_attempts
        }

        # if include_orders:
        #     user_data['orders'] = [order.serialize(include_user=False) for order in self.orders]
        if deep:
            serialized_games = [game.serialize() for game in self.user.games]
            user_data["games"] = serialized_games

        return user_data

    @classmethod
    def create_user(cls, name):
        """Creates a User"""

        user = User(
            name=name
        )

        db.session.add(user)
        db.session.commit()

        return user


