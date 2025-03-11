from flask_login import LoginManager
from sqlalchemy import select

from models import User, db

from .auth_routes import auth_bp
from .main_routes import main_bp


def init_routes(app):
    app.register_blueprint(auth_bp)


def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(select(User).where(User.user_id == user_id))
