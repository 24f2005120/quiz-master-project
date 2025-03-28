from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect("/redirect")
    if request.method == "GET":
        return render_template("landing.html")
