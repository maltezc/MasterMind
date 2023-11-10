import os
from flask import Flask

from mastermind_be.attempts.routes import attempts_routes
from mastermind_be.database import connect_db
from mastermind_be.config import DevelopmentConfig

import mastermind_be.games.routes
from mastermind_be.games.routes import games_routes

from mastermind_be.database import db

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

connect_db(app)


# Register Blueprints
app.register_blueprint(games_routes, url_prefix='/api/games')
app.register_blueprint(attempts_routes, url_prefix='/api/attempts')

if __name__ == '__main__':
    app.run()
