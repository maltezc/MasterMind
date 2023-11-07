import os
from flask import Flask
from mastermind_be.database import connect_db

app = Flask(__name__)

import mastermind_be.games.routes

from mastermind_be.games.routes import games_routes

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

connect_db(app)

# Register Blueprints
app.register_blueprint(games_routes, url_prefix='/api/games')


if __name__ == '__main__':
    app.run()
