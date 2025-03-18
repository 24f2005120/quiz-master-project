from flask import (Blueprint, jsonify, redirect, render_template, request,
                   url_for)
from flask_login import current_user
from flask_login.utils import current_app
from sqlalchemy import select

from forms import SubjectForm
from models import db
from models.models import Chapter, Subject

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
    if request.method == "GET":
        subjects = session.scalars(select(Subject)).all()
        return render_template(
            "admin/home.html", subjects=subjects, subject_form=subject_form
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


@admin_bp.route("delete_subject/<int:subject_id>", methods=["DELETE", "GET"])
def delete_subject(subject_id):
    subject = session.scalar(select(Subject).where(Subject.subject_id == subject_id))
    session.delete(subject)
    session.commit()
    return jsonify({"message": f"Succesfully deleted subject {subject.subject_name}"})


@admin_bp.route("delete_chapter/<chapter_id>", methods=["DELETE"])
def delete_chapter(chapter_id):
    chapter = session.scalar(select(Chapter).where(Chapter.chapter_id == chapter_id))
    session.delete(chapter)
    session.commit()
    return jsonify({"message": f"Succesfully deleted subject {chapter.chapter_name}"})
