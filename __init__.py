from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes import auth, users, disease, compliance, emergency, network
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(disease.bp)
    app.register_blueprint(compliance.bp)
    app.register_blueprint(emergency.bp)
    app.register_blueprint(network.bp)

    return app