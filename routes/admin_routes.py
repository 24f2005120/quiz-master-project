from flask import (Blueprint, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import current_user
from flask_login.utils import current_app
from sqlalchemy import func, select

from forms import ChapterForm, QuestionForm, QuizForm, SubjectForm, editQuestionForm
from models import db
from models.models import Chapter, Option, Question, Quiz, Subject

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
            quiz_form=quiz_form,
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
    quiz = Quiz(subject_id=subject_id, chapter_id=chapter_id)  # unsafe
    form.populate_obj(quiz)
    session.add(quiz)
    session.commit()

    return jsonify({"message": "Succesfully created empty quiz"})


def select_quiz(quiz_id):
    return session.scalar(select(Quiz).where(Quiz.quiz_id == quiz_id))


@admin_bp.route("quiz/<int:quiz_id>/delete_quiz", methods=["DELETE"])
def delete_quiz(quiz_id):
    quiz = select_quiz(quiz_id)
    session.delete(quiz)
    session.commit()
    return jsonify({"message": f"Succesfully deleted quiz {quiz.quiz_name}"})


@admin_bp.route("quiz/<int:quiz_id>", methods=["GET", "POST"])
def edit_quiz(quiz_id):
    quiz = select_quiz(quiz_id)
    if not quiz:
        return jsonify({"errors":[f"quiz with quiz_id {quiz_id} not found"]}),404

    if request.method=="POST":
        form = QuizForm()
        if not form.validate_on_submit():
            return jsonify({"errors":form.errors}),400
        quiz = select_quiz(quiz_id)
        form.populate_obj(quiz)
        session.commit()
        return jsonify({"message":"Succesfully edited quiz details"})

    return render_template(
        "admin/quiz.html",
        quiz=quiz,
        quiz_form=QuizForm(),
        question_form=QuestionForm(),
        edit_question_form=editQuestionForm(),
    )


@admin_bp.route("quiz")
def quizzes():
    pass

def select_question(question_id):
    return session.scalar(select(Question).where(Question.question_id==question_id))

@admin_bp.route("quiz/<int:quiz_id>/create_question", methods=["POST", "GET"])
def create_question(quiz_id):
    quiz = select_quiz(quiz_id)
    if not quiz:
        return jsonify({"errors": [f"Quiz with quiz_id {quiz_id} not found"]}), 404

    if request.method == "POST":
        form = QuestionForm(request.form) # Pass request.form here
        if not form.validate_on_submit():
            return jsonify({"errors": form.errors}), 400

        question = Question(quiz_id=quiz_id)
        question.text = form.text.data
        question.marks = form.marks.data
        session.add(question)
        session.flush() # Flush to get question_id

        # Clear existing options and add new ones - Manual Assignment (Correct)
        question.options = [] # Clear existing options
        for option_form in form.options:
            if option_form.text.data:
                option = Option(
                    question_id=question.question_id, # Set question_id here
                    text=option_form.text.data,
                    is_correct=option_form.is_correct.data
                )
                db.session.add(option)

        db.session.commit()
        return jsonify({"message": "Successfully updated question"})    # GET request should not be directly accessed, modal form is used.

    return jsonify({"errors": ["GET method not allowed for this route"]}), 405


@admin_bp.route("quiz/<int:quiz_id>/question/<int:question_id>", methods=["GET", "POST", "DELETE"])
def edit_question(quiz_id, question_id):
    quiz = select_quiz(quiz_id) # Verify quiz exists if needed
    if not quiz:
        return jsonify({"errors": [f"Quiz with quiz_id {quiz_id} not found"]}), 404
    question = select_question(question_id)
    if not question:
        return jsonify({"errors": [f"Question with question_id {question_id} not found"]}), 404


    if request.method == "POST":
        form = QuestionForm(request.form, obj=question) # Pass request.form and obj for editing
        if not form.validate_on_submit():
            return jsonify({"errors": form.errors}), 400


        question = Question(quiz_id=quiz_id)
        question.text = form.text.data
        question.marks = form.marks.data
        session.flush() # Flush to get question_id

        db.session.commit()
        return jsonify({"message": "Successfully updated question"})

    if request.method == "DELETE":
        db.session.delete(question)
        db.session.commit()
        return jsonify({"message": "Successfully deleted question"})


    # GET request to render edit form
    form = QuestionForm(obj=question) # Populate form for editing
    return render_template("admin/quiz.html", quiz=quiz, quiz_form=QuizForm(obj=quiz), question_form=form, quiz_id=quiz_id, question_id=question_id) # Re-render quiz page, adjust if needed

@admin_bp.route("quiz/<int:quiz_id>/question/<int:question_id>/delete_question", methods=["DELETE"])
def delete_question(quiz_id, question_id): # Separate delete route
    question = select_question(question_id)
    if not question:
        return jsonify({"errors": [f"Question with question_id {question_id} not found"]}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Successfully deleted question"})
