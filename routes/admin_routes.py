from functools import wraps

from flask import Blueprint, render_template, request
from flask_login import current_user
from flask_login.utils import current_app

from models import User, db

session = db.session

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):  # creates a decorater to check admin is logged in
    @wraps(f)
    def decorated_f(*args, **kwargs):
        if (
            not current_user.is_authenticated  # just reusing the code of login_required
            or current_user.username != "admin"
        ):
            return current_app.login_manager.unauthorized()

        return f(*args, **kwargs)

    return decorated_f


@admin_bp.route("/", methods=["GET", "POST"])
@admin_required
def admin_home():
    if request.method == "GET":
        return render_template("admin_home.html")
