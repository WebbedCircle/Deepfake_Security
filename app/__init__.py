# --- FILE: app/__init__.py ---
from flask import Flask
from flask_login import LoginManager
from app.auth import users
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return users.get(user_id)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app