from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_login.utils import current_app
from sqlalchemy import select

from models import User, db
from models.models import Quiz

session = db.session

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.before_request  # makes it so you have to be logged in to access, and allows admin to access it too to test :)
@login_required
def user_required():
    pass


@user_bp.route("/", methods=["GET"])
def home():
    upcoming_quizzes = session.scalars(select(Quiz))
    return render_template("user/home.html", upcoming_quizzes=upcoming_quizzes)


