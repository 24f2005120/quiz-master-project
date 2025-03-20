from datetime import date, time
from typing import Annotated, List, Optional

from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import db

# handy custom types
id_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class User(db.Model, UserMixin):
    user_id: Mapped[id_pk]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    scores: Mapped[List["Score"]] = relationship(
        back_populates="user", cascade="all,delete-orphan"
    )

    def get_id(self):
        return self.user_id


class Subject(db.Model):
    subject_id: Mapped[id_pk]
    subject_name: Mapped[str]
    description: Mapped[str]

    chapters: Mapped[List["Chapter"]] = relationship(
        back_populates="subject", cascade="all,delete-orphan"
    )


class Chapter(db.Model):
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subject.subject_id"), primary_key=True
    )
    chapter_id: Mapped[int] = mapped_column(primary_key=True)
    chapter_name: Mapped[str]
    description: Mapped[str]

    subject: Mapped["Subject"] = relationship(back_populates="chapters")
    quizzes: Mapped[List["Quiz"]] = relationship(
        "Quiz",
        # ensures when we do chapter.quizzes it only takes the correct chapter not all the ones with same chapter_id
        primaryjoin="and_(Quiz.subject_id == Chapter.subject_id, Quiz.chapter_id == Chapter.chapter_id)",
        back_populates="chapter",
    )


class Quiz(db.Model):
    quiz_id: Mapped[id_pk]
    quiz_name: Mapped[str]
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapter.chapter_id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.subject_id"))
    date: Mapped[Optional[date]]
    duration: Mapped[Optional[int]]  # minutes? hopefully
    remarks: Mapped[str]

    chapter: Mapped["Chapter"] = relationship(back_populates="quizzes")
    questions: Mapped[List["Question"]] = relationship(
        back_populates="quiz", cascade="all,delete-orphan"
    )
    scores: Mapped[List["Score"]] = relationship(
        back_populates="quiz", cascade="all,delete-orphan"
    )


class Question(db.Model):
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.quiz_id"))
    question_id: Mapped[id_pk]
    text: Mapped[str]
    marks: Mapped[int]

    quiz: Mapped["Quiz"] = relationship(back_populates="questions")


class Score(db.Model):
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.quiz_id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), primary_key=True)
    start_time: Mapped[time]
    time_taken: Mapped[int]  # we'll be storing as seconds

    quiz: Mapped["Quiz"] = relationship(back_populates="scores")
    user: Mapped["User"] = relationship(back_populates="scores")
