from flask import (Blueprint, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import current_user
from flask_login.utils import current_app
from sqlalchemy import func, select

from forms import ChapterForm, QuizForm, SubjectForm
from models import db
from models.models import Chapter, Quiz, Subject

session = db.session

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.before_request
def require_admin():
    """Apply admin restriction to all routes in this blueprint."""
    if not current_user.is_authenticated or current_user.username != "admin":
        return current_app.login_manager.unauthorized()


@admin_bp.route("/", methods=["GET"])
def admin_home():
    subject_form = SubjectForm()
    chapter_form = ChapterForm()
    quiz_form = QuizForm()
    if request.method == "GET":
        subjects = session.scalars(select(Subject)).all()
        return render_template(
            "admin/home.html",
            subjects=subjects,
            subject_form=subject_form,
            chapter_form=chapter_form,
            quiz_form=quiz_form
        )


@admin_bp.route("/create_subject", methods=["POST"])
def create_subject():
    form = SubjectForm()
    # Validate and process the form submission
    if not form.validate_on_submit():
        return (
            jsonify({"errors": form.errors}),
            400,
        )  # Return errors as JSON for AJAX handling

    new_subject = Subject()
    form.populate_obj(new_subject)

    # make sure no duplicate subs
    if session.scalar(
        select(Subject).where(Subject.subject_name == new_subject.subject_name)
    ):
        return (
            jsonify(
                {
                    "errors": {
                        "Subject Name": [
                            "Subject already exists, please use a different Subject Name"
                        ]
                    }
                }
            ),
            400,
        )

    session.add(new_subject)
    session.commit()
    return jsonify({"message": "Subject created successfully!"})


def select_subject(subject_id):
    return session.scalar(select(Subject).where(Subject.subject_id == subject_id))


@admin_bp.route("delete_subject/<int:subject_id>", methods=["DELETE", "GET"])
def delete_subject(subject_id):
    subject = select_subject(subject_id)
    session.delete(subject)
    session.commit()
    return jsonify({"message": f"Succesfully deleted subject {subject.subject_name}"})


@admin_bp.route("edit_subject/<int:subject_id>", methods=["PUT", "POST"])
def edit_subject(subject_id):
    subject = select_subject(subject_id)
    form = SubjectForm()
    if not form.validate_on_submit():
        return (
            jsonify({"errors": form.errors}),
            400,
        )
    form.populate_obj(subject)
    session.commit()
    return jsonify({"message": "Subject Edited Successfully"})


@admin_bp.route("<int:subject_id>/create_chapter", methods=["POST"])
def create_chapter(subject_id):
    subject = session.scalar(select(Subject).where(Subject.subject_id == subject_id))
    if not subject:
        return jsonify({"errors": {"subject": ["subject not found"]}}), 400
    form = ChapterForm()
    if not form.validate_on_submit():
        return (
            jsonify({"errors": form.errors}),
            400,
        )  # Return errors as JSON for AJAX handling

    # since composite keys have to be incremented manually in sqlite
    max_number = session.scalar(
        select(func.max(Chapter.chapter_id)).where(Chapter.subject_id == subject_id)
    )
    # If there are no chapters yet, max_number will be None. Start at 1.
    chapter_number = (max_number or 0) + 1

    new_chapter = Chapter(subject_id=subject_id, chapter_id=chapter_number)
    form.populate_obj(new_chapter)
    session.add(new_chapter)
    session.commit()
    return jsonify({"message": "Chapter created successfully"})


def select_chapter(subject_id, chapter_id):
    return session.scalar(
        select(Chapter).where(
            Chapter.chapter_id == chapter_id and Chapter.subject_id == subject_id
        )
    )


@admin_bp.route(
    "<int:subject_id>/delete_chapter/<int:chapter_id>", methods=["DELETE", "GET"]
)
def delete_chapter(subject_id, chapter_id):
    chapter = select_chapter(subject_id, chapter_id)
    session.delete(chapter)
    session.commit()
    return jsonify({"message": f"Succesfully deleted subject {chapter.chapter_name}"})


@admin_bp.route(
    "<int:subject_id>/edit_chapter/<int:chapter_id>", methods=["POST", "PUT"]
)
def edit_chapter(subject_id, chapter_id):
    chapter = select_chapter(subject_id, chapter_id)
    form = ChapterForm()
    if not form.validate_on_submit():
        return (
            jsonify({"errors": form.errors}),
            400,
        )
    form.populate_obj(chapter)
    session.commit()
    return jsonify({"message": "Subject Edited Successfully"})


@admin_bp.route("<int:subject_id>/<int:chapter_id>/create_quiz", methods=["POST"])
# @admin_bp.route("create_quiz", methods=["POST"]) if i want to make unassigned quizzes possible
def create_quiz(subject_id, chapter_id):
    form = QuizForm()
    if not form.validate_on_submit():
        return (jsonify({"errors": form.errors}), 400)
    quiz = Quiz(subject_id=subject_id,chapter_id=chapter_id)#unsafe
    form.populate_obj(quiz)
    session.add(quiz)
    session.commit()

    return jsonify({"message":"Succesfully created empty quiz"})

def select_quiz(quiz_id):
    return session.scalar(select(Quiz).where(Quiz.quiz_id==quiz_id))
@admin_bp.route("quiz/<int:quiz_id>/delete_quiz", methods=["DELETE"])
def delete_quiz(quiz_id):
    quiz = select_quiz(quiz_id)
    session.delete(quiz)
    session.commit()
    return jsonify({"message":f"Succesfully deleted quiz {quiz.quiz_name}"})

@admin_bp.route("quiz/<int:quiz_id>", methods=["GET", "POST"])
def edit_quiz(quiz_id):
    quiz = select_quiz(quiz_id)
    return f"quiz {quiz.quiz_name}"


@admin_bp.route("quizzes")
def quizzes():
    pass


