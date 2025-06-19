from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)

    # Register routes
    from app.routes.upload import upload_bp
    from app.routes.search import search_bp
    app.register_blueprint(upload_bp)
    app.register_blueprint(search_bp)

    return app
