from datetime import datetime, timedelta, timezone

from flask import (Blueprint, app, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required
from flask_login.utils import current_app
from sqlalchemy import func, select

from models import Quiz, User, db
from models.models import Option, QuestionAttempt, QuizAttempt
from utils.db_utils import select_option, select_quiz

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
    session[f"quiz{quiz_id}_start_time"] = datetime.now(
        timezone.utc
    )  # Record start time in session
    return render_template("user/quiz.html", quiz=quiz)

# NOT using wtform validation here,
# because its kinda a pain to implement
# and it is just mcq/msq not numeric or anything anyways,
# so the benefit is minimal
@user_bp.route("/<int:quiz_id>/submit", methods=["POST"])
def submit_quiz(quiz_id):

    quiz = select_quiz(quiz_id)
    if not quiz:
        return 404

    # time calculation
    start_time = session.pop(f"quiz{quiz_id}_start_time")
    end_time = datetime.now(timezone.utc)
    time_taken = end_time - start_time
    time_taken = (
        int(time_taken.total_seconds()) // 60
    )  # everything going to be stored in minutes in the backend
    frontend_time = int(request.form.get("time_taken"))

    if not (
        time_taken - 5 < frontend_time < time_taken + 5
        or time_taken > quiz.duration + 5
    ):  # prevents eggregious time_taken manipulation hopefully
        raise TimeoutError

    quiz_attempt = QuizAttempt(
        quiz_id=quiz.quiz_id,
        user_id=current_user.user_id,
        total_score=0,  # Initialize, will calculate later
        percentage=0.0,  # Initialize, will calculate later
        start_time=start_time,
        time_taken=time_taken,
    )

    db.session.add(quiz_attempt)
    db.session.flush()

    total_score = 0
    # iterating through the questions instead of the response
    # is more secure as the user can't tamper by sending
    # manipulated post requests that say 'correct option from another quiz' repeatedly
    for question in quiz.questions:
        question_attempt = QuestionAttempt(
            quiz_attempt_id=quiz_attempt.id,
            question_id=question.question_id,
        )
        db.session.add(question_attempt)
        db.session.flush()

        # list of selected option_id's
        selected_options = list(
            map(int, request.form.getlist(f"question_{question.question_id}[]"))
        )

        marks_for_q = question.marks
        correctness = 0
        correct_opts = db.session.scalar(
            select(func.count())
            .select_from(Option)
            .where(
                Option.question_id == question.question_id, Option.is_correct == True
            )
        )
        for option in question.options:
            if option.option_id in selected_options:
                question_attempt.selected_options.append(option)
                # if your answer is correct, you gain a fraction of the marks
                if option.is_correct:
                    correctness += 1 / correct_opts
                else:  # otherwise you lose that fraction
                    correctness -= 1 / correct_opts

        marks_gained = marks_for_q * correctness
        marks_gained = marks_gained if marks_gained > 0 else 0
        print(marks_gained)
        question_attempt.marks_gained = marks_gained
        total_score += marks_gained

    quiz_attempt.total_score = round(total_score, 2)
    quiz_attempt.percentage = round(total_score*100/quiz.total_marks,2)

    db.session.commit()
    return redirect(url_for("user.results", quiz_attempt_id=quiz_attempt.id))

@user_bp.route("/past_attempts/<int:quiz_attempt_id>", methods=["GET"])
def results(quiz_attempt_id):
    quiz_attempt = db.session.scalar(
        select(QuizAttempt).where(QuizAttempt.id == quiz_attempt_id)
    )
    return render_template("user/results.html", quiz_attempt=quiz_attempt)

@user_bp.route("/past_attempts", methods=["GET"])
def history():
    return render_template("user/history.html", user=current_user)
