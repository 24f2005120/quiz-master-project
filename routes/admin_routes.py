from flask import Blueprint, render_template, request
from flask_login import current_user
from flask_login.utils import current_app
from sqlalchemy import select

from models import db
from models.models import Subject

session = db.session

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.before_request
def require_admin():
    """Apply admin restriction to all routes in this blueprint."""
    if not current_user.is_authenticated or current_user.username != "admin":
        return current_app.login_manager.unauthorized()


@admin_bp.route("/", methods=["GET", "POST"])
def admin_home():
    if request.method == "GET":
        subjects = session.scalars(select(Subject))
        return render_template("admin_home.html", subjects=subjects)


@admin_bp.route("/create_subject", methods=["GET"])
def create_subject():
    if request.method == "GET":
        return render_template("create_subject.html")
