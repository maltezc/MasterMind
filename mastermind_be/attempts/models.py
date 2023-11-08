"""Attempts models"""

from datetime import datetime
from sqlalchemy.orm import validates

from mastermind_be.database import db


# attempts Table
class Attempt(db.Model):
    """ One-to-many table connecting a game to many image attempts. """

    __tablename__ = "attempts"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    game_id = db.Column(
        db.Integer,
        db.ForeignKey("games.id", ondelete="CASCADE")
    )

    game = db.relationship('Game', back_populates='attempts', uselist=False)

    guess = db.Column(
        db.Integer,
        nullable=False
    )

    @validates("guess")
    def validate_guess(self, key, value):
        """Validates guess is a whole number and doesnt contain any special characters """

        if not value.isdigit():
            raise ValueError("Number to guess must be a number.")
        parsed_value = int(value)
        return parsed_value



    date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    def serialize(self):
        """Returns self"""

        return {
            "id": self.id,
            "game_id": self.game_id,
            "guess": self.guess,
            "date_created": self.date_created
        }

    @classmethod
    def make_attempt(cls, game_id, guess):
        """Makes a guessing attempt"""

        attempt = Attempt(
            game_id=game_id,
            guess=guess
        )

        db.session.add(attempt)
        db.session.commit()

        return attempt

        # try:
        #     # confirm is int, is not string, and contains no special characters.
        #
        # except ValueError as error:
        #     abort(400, "enter a valid value")