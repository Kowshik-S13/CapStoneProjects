from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    app.config.from_object(Config)
    db.init_app(app)

    from app.user_routes import main_routes
    app.register_blueprint(main_routes)
    return app