from flask import (Blueprint, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from flask_login.utils import current_app
from sqlalchemy import func, select

from models import Quiz, User, db
from models.models import Option
from utils.db_utils import select_quiz

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.before_request  # makes it so you have to be logged in to access, and allows admin to access it too to test :)
@login_required
def user_required():
    pass


@user_bp.route("/", methods=["GET"])
def home():
    upcoming_quizzes = db.session.scalars(select(Quiz))
    return render_template("user/home.html", upcoming_quizzes=upcoming_quizzes)


@user_bp.route("/<int:quiz_id>", methods=["GET"])
def quiz(quiz_id):
    quiz = select_quiz(quiz_id)
    # ok-ish unreadable list comprehension
    # makes a list that tells whether or not to make this question checkbox instead of radio in the tmeplate
    return render_template("user/quiz.html", quiz=quiz) 


#
# NOT using wtform validation here,
# because its kinda a pain to implement
# and it is just mcq/msq not numeric or anything anyways,
# so the benefit is minimal
#


@user_bp.route("/<int:quiz_id>/submit", methods=["POST"])
def submit_quiz(quiz_id):
    quiz = select_quiz(quiz_id)
    print(request.form)
    return jsonify(request.form)
