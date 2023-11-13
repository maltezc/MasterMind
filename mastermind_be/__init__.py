import os
from flask import Flask
from flask_cors import CORS

from mastermind_be.database import connect_db
from mastermind_be.config import DevelopmentConfig

import mastermind_be.games.routes
from mastermind_be.games.routes import games_routes
from mastermind_be.attempts.routes import attempts_routes
from mastermind_be.users.routes import users_routes

from mastermind_be.database import db

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
CORS(app)

connect_db(app)


# Register Blueprints
app.register_blueprint(games_routes, url_prefix='/api/games')
app.register_blueprint(attempts_routes, url_prefix='/api/attempts')
app.register_blueprint(users_routes, url_prefix='/api/users')

if __name__ == '__main__':
    app.run()
