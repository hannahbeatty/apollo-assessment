# for deployment (run here)

from flask import Flask
from config import Config
from database import db
from api import vehicle_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize SQLAlchemy
    db.init_app(app)

    # register blueprints
    app.register_blueprint(vehicle_bp)

    # create tables if not existing
    with app.app_context():
        db.create_all()

    return app


# allow running with: python app.py
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
