from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from forms import AuthForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("landing.html", auth_form=AuthForm())
