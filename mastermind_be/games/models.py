"""games models"""
from sqlalchemy import Enum as SQLAlchemyEnum
from werkzeug.exceptions import abort
from datetime import datetime

from sqlalchemy.orm import validates

from mastermind_be.database import db
from mastermind_be.games.helpers.enums import GameStatusEnum


# game table
class Game(db.Model):
    """ Listing in the system """

    __tablename__ = 'games'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    status = db.Column(
        SQLAlchemyEnum(GameStatusEnum, name='game_status_enum'),
        nullable=False
    )

    spaces = db.Column(
        db.Integer,
        db.CheckConstraint('spaces >= 4 AND spaces <= 7'),
        nullable=False
    )

    @validates("spaces")
    def validate_spaces(self, key, value):
        """validates number of spaces is between 4 and 7"""

        if 4 <= value <= 7:
            raise ValueError("Spaces must be between 4 and 7")
        return value;

    number = db.Column(
        db.Integer,
        nullable=False
    )

    game_date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    attempts = db.Column(
        db.Integer,
        nullabe=False,
        default=0
    )




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
