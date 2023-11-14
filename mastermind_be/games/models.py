"""games models"""
from datetime import datetime
from sqlalchemy.orm import validates
from mastermind_be.database import db


# game table
class Game(db.Model):
    """ Games table """

    __tablename__ = 'games'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    users = db.Relationship("User", back_populates="game", uselist=True)

    # player1_name = db.Column(
    #     db.Text,
    #     nullable=False
    # )

    # player1_guesses_count = db.Column(
    #     db.Integer,
    #     nullable=False,
    #     default=0
    # )

    # player2_name = db.Column(
    #     db.Text,
    #     nullable=True
    # )

    # player2_guesses_count = db.Column(
    #     db.Integer,
    #     nullable=False,
    #     default=0
    # )

    # TODO: SET enums for status. ACTIVE, COMPLETED
    status = db.Column(
        db.Text,
        # SQLAlchemyEnum(GameStatusEnum, name='game_status_enum'),
        nullable=False,
        default="ACTIVE"
    )

    # winner = db.Column(
    #     db.Text,
    #     nullable=True,
    # )

    spaces = db.Column(
        db.Integer,
        db.CheckConstraint('spaces >= 4 AND spaces <= 7'),
        nullable=False
    )

    difficulty = db.Column(
        db.Text,
        default="easy",
        nullable=False
    )

    @validates("spaces")
    def validate_spaces(self, key, value):
        """validates number of spaces is between 4 and 7"""

        parsed_value = int(value)
        if 4 > parsed_value > 7:
            raise ValueError("Number to guess must be between 4 and 7")
        return value

    number_to_guess = db.Column(
        db.String(7),
        nullable=False
    )

    # players_count = db.Column(
    #     db.Integer,
    #     nullable=False,
    #     default=1
    # )

    multiplayer = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    datetime_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
    )

    datetime_completed = db.Column(
        db.DateTime,
        nullable=True
    )

    attempts = db.Relationship("Attempt", back_populates="game", uselist=True)

    def serialize(self, deep=True):
        """returns self"""

        serialized_attempts = [attempt.serialize() for attempt in self.attempts]

        game_data = {
            "id": self.id,
            "number_to_guess": self.number_to_guess,
            "spaces": self.spaces,
            "difficulty": self.difficulty,
            # "player1_name": self.player1_name,
            # "player1_guesses_count": self.player1_guesses_count,
            # "player2_name": self.player2_name,
            # "player2_guesses_count": self.player2_guesses_count,
            "multiplayer": self.multiplayer,
            # "players_count": self.players_count,
            # "winner": self.winner,
            "status": self.status,
            "datetime_created": self.datetime_created,
            "datetime_completed": self.datetime_completed,
            "attempts": serialized_attempts
        }

        if deep:
            serialized_users = [user.serialize(False) for user in self.users]
            game_data["users"] = serialized_users

        return game_data



    @classmethod
    def create_game(cls, number_to_guess, spaces, difficulty, users):
        """Instantiates a game with a number to guess"""

        game = Game(
            number_to_guess=number_to_guess,
            spaces=spaces,
            difficulty=difficulty,
            # users=users
            # player1_name=player1_name,
            # player2_name=player2_name
        )

        db.session.add(game)
        db.session.commit()

        for user in users:
            game.users.append(user)

        db.commit()

        return game

    # @staticmethod
    # def player1_increment_guess(game):
    #     """Static Method to Increment player1 guesses on a game."""
    #
    #     game.player1_guesses_count += 1
    #     db.session.commit()
    #
    #     return game

    # @staticmethod
    # def player2_increment_guess(game):
    #     """Static Method to Increment player2 guesses on a game."""
    #
    #     game.player2_guesses_count += 1
    #     db.session.commit()
    #
    #     return game

    @staticmethod
    def set_status_completed(game):
        """Sets the game status to completed"""

        game.status = "COMPLETED"
        game.datetime_completed = datetime.now()

        db.session.commit()

        return game

    # @staticmethod
    # def set_winner_user1(game, user_id):
    #     """Sets the winner to user1"""
    #
    #     game.winner = user_id
    #     db.session.commit()
    #
    #     return game

# user table


