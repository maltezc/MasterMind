"""models for users"""

from datetime import datetime
from sqlalchemy.orm import validates

from mastermind_be import db


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
    games = db.Relationship("Game", back_populates="user", uselist=True)

    # attempts
    attempts = db.Relationship("Attempt", back_populates="user", uselist=True)

    def serialize(self):
        """returns self"""

        serialized_attempts = [attempt.serialize() for attempt in self.user.attempts]
        serialized_games = [game.serialize() for game in self.user.games]

        return {
            "id": self.id,
            "name": self.name,
            "games": serialized_games,
            "attempts": serialized_attempts
        }

    @classmethod
    def create_user(cls, name):
        """Creates a User"""

        user = User(
            name=name
        )

        db.session.add(user)
        db.session.commit()

        return user
