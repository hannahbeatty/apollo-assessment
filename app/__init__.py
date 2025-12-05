from flask import Flask
from app.config import Config
from app.database import db
from app.api import vehicle_bp

def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)

    # Load default config
    app.config.from_object(Config)

    if testing:
        app.config["TESTING"] = True # change if not testing

    # Init database
    db.init_app(app)

    # Register routes
    app.register_blueprint(vehicle_bp)

    return app
