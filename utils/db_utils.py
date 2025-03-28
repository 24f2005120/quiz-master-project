from sqlalchemy import select

from models import db
from models.models import Chapter, Option, Question, Quiz, Subject, User

# yes i could have made this a single function and very dry but
# this way just felt a bit more natural yk
# less scalable, slightly more readable


def select_subject(subject_id):
    return db.session.scalar(select(Subject).where(Subject.subject_id == subject_id))


def select_user(username):
    return db.session.scalar(select(User).where(User.username == username))


def select_chapter(subject_id, chapter_id):
    return db.session.scalar(
        select(Chapter).where(
            Chapter.chapter_id == chapter_id and Chapter.subject_id == subject_id
        )
    )


def select_quiz(quiz_id):
    return db.session.scalar(select(Quiz).where(Quiz.quiz_id == quiz_id))


def select_question(
    question_id: int,
) -> Question | None:  # just playing a bit with pythons type annotations
    return db.session.scalar(
        select(Question).where(Question.question_id == question_id)
    )


def select_option(option_id):
    return db.session.scalar(select(Option).where(Option.option_id == option_id))
