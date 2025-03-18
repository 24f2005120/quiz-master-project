from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_login.utils import current_app

user_bp = Blueprint("user", __name__, url_prefix="user")


@user_bp.before_request
@login_required
def require_user():
    """Apply user restriction to all routes in this blueprint."""
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
