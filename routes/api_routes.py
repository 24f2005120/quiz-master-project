from flask import Blueprint, jsonify

# Assuming your models are in a file named models.py in the same directory
# and your db object is already configured as shown in the problem description
# from . import db # if you are in a package, otherwise adjust import
from models import (Chapter, Quiz,  # Assuming your models are in models.py
                    Subject, db)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def serialize_subject(subject):
    return {
        "subject_id": subject.subject_id,
        "subject_name": subject.subject_name,
        "description": subject.description,
    }


def serialize_chapter(chapter):
    return {
        "subject_id": chapter.subject_id,
        "chapter_id": chapter.chapter_id,
        "chapter_name": chapter.chapter_name,
        "description": chapter.description,
    }


def serialize_quiz(quiz):
    return {
        "quiz_id": quiz.quiz_id,
        "quiz_name": quiz.quiz_name,
        "chapter_id": quiz.chapter_id,
        "subject_id": quiz.subject_id,
        "date": str(quiz.date) if quiz.date else None,
        "duration": quiz.duration,
        "remarks": quiz.remarks,
        "total_marks": quiz.total_marks,
    }


session = db.session


@api_bp.route("/subjects", methods=["GET"])
def get_subjects():
    subjects = session.query(Subject).all()
    session.close()
    return jsonify([serialize_subject(subject) for subject in subjects])


@api_bp.route("/subjects/<int:subject_id>/chapters", methods=["GET"])
def get_chapters_by_subject(subject_id):
    subject = session.query(Subject).filter_by(subject_id=subject_id).first()
    if not subject:
        session.close()  # or db.session.close() if using db object
        return jsonify({"message": "Subject not found"}), 404
    chapters = subject.chapters
    session.close()  # or db.session.close() if using db object
    return jsonify([serialize_chapter(chapter) for chapter in chapters])


@api_bp.route(
    "/subjects/<int:subject_id>/chapters/<int:chapter_id>/quizzes", methods=["GET"]
)
def get_quizzes_by_chapter(subject_id, chapter_id):
    chapter = (
        session.query(Chapter)
        .filter_by(subject_id=subject_id, chapter_id=chapter_id)
        .first()
    )
    if not chapter:
        session.close()  # or db.session.close() if using db object
        return jsonify({"message": "Chapter not found"}), 404
    quizzes = chapter.quizzes
    session.close()  # or db.session.close() if using db object
    return jsonify([serialize_quiz(quiz) for quiz in quizzes])
