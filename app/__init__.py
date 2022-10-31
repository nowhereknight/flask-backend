from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    cors = CORS(api, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
