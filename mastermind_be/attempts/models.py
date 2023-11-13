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

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE")
    )
    user = db.relationship('User', back_populates='attempts', uselist=False)

    guess = db.Column(
        db.String(7),
        nullable=False
    )

    winning_attempt = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # player_name = db.Column(
    #     db.Text,
    #     nullable=False,
    # )

    @validates("guess")
    def validate_guess(self, key, value):
        """Validates guess is a whole number and doesn't contain any special characters """

        try:
            parsed_value = int(value)
        except ValueError:
            raise ValueError("Value entered is not a number.")

        if 4 > len(value) > 7:
            raise ValueError("Number to guess must be between 4 and 7")
        return value

    datetime_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
    )

    hint = db.Column(
        db.Text,
        nullable=False,
    )

    def serialize(self):
        """Returns self"""

        return {
            "id": self.id,
            "game_id": self.game_id,
            "guess": self.guess,
            # "player_name": self.player_name,
            "user_id": self.user_id,
            "winning_attempt": self.winning_attempt,
            "datetime_created": self.datetime_created,
            "hint": self.hint
        }

    @classmethod
    def make_attempt(cls, game_id, guess, player_id, hint):
        """Makes a guessing attempt"""

        attempt = Attempt(
            game_id=game_id,
            guess=guess,
            player_id=player_id,
            # player_name=player_name,
            hint=hint
        )

        db.session.add(attempt)
        db.session.commit()

        return attempt
