"""games models"""
from sqlalchemy import Enum as SQLAlchemyEnum
from werkzeug.exceptions import abort
from datetime import datetime

from sqlalchemy.orm import validates

from mastermind_be.database import db
from mastermind_be.games.helpers.enums import GameStatusEnum


# game table
class Game(db.Model):
    """ Games table """

    __tablename__ = 'games'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    # TODO: SET enums for status. ONGOING, WIN, LOSS
    status = db.Column(
        db.Text,
        # SQLAlchemyEnum(GameStatusEnum, name='game_status_enum'),
        nullable=False,
        default="ONGOING"
    )

    spaces = db.Column(
        db.Integer,
        db.CheckConstraint('spaces >= 4 AND spaces <= 7'),
        nullable=False
    )

    @validates("spaces")
    def validate_spaces(self, key, value):
        """validates number of spaces is between 4 and 7"""

        parsed_value = int(value)
        if 4 > parsed_value > 7:
            raise ValueError("Number to guess must be between 4 and 7")
        return parsed_value

    number_to_guess = db.Column(
        db.Integer,
        nullable=False
    )

    date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    attempts = db.Relationship("Attempt", back_populates="game", uselist=True)
    # attempts = db.Column(
    #     db.Integer,
    #     nullable=False,
    #     default=0
    # )

    def serialize(self):
        """returns self"""

        return {
            "id": self.id,
            "number_to_guess": self.number_to_guess,
            "spaces": self.spaces,
            "status": self.status,
            "date_created": self.date_created,
            "attempts": self.attempts
        }

    @classmethod
    def create_game(cls, number_to_guess, spaces):
        """Instantiates a game with a number to guess"""

        game = Game(
            number_to_guess=number_to_guess,
            spaces=spaces,
        )

        db.session.add(game)
        db.session.commit()

        return game


# attempt#

# attempt table?

# userId
# attempt#
# attempt time stamp

# user table

# userId
# username
# userSignupDate
# usertotal attempts
# usertotal Games
# userwins
