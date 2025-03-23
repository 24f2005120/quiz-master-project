from datetime import date, time
from typing import Annotated, List, Optional

from flask_login import UserMixin
from sqlalchemy import Boolean, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db

# handy custom types
id_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class User(db.Model, UserMixin):
    __tablename__ = "user"

    user_id: Mapped[id_pk]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    quiz_attempts: Mapped[List["QuizAttempt"]] = relationship(
        back_populates="user", cascade="all,delete-orphan"
    )

    def get_id(self): # just makes wtforms auth work
        return self.user_id # by default configured to self.id, but i named it as user_id from the start so 


class Subject(db.Model):
    __tablename__ = "subject"
    subject_id: Mapped[id_pk]
    subject_name: Mapped[str]
    description: Mapped[str]

    chapters: Mapped[List["Chapter"]] = relationship(
        back_populates="subject", cascade="all,delete-orphan"
    )


class Chapter(db.Model):
    __tablename__ = "chapter"
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subject.subject_id"), primary_key=True
    )
    chapter_id: Mapped[int] = mapped_column(primary_key=True)
    chapter_name: Mapped[str]
    description: Mapped[str]

    subject: Mapped["Subject"] = relationship(back_populates="chapters")
    quizzes: Mapped[List["Quiz"]] = relationship(
        back_populates="chapter",
    )


class Quiz(db.Model):
    __tablename__ = "quiz"
    quiz_id: Mapped[id_pk]
    quiz_name: Mapped[str]

    # we are using chapter.subject_id here because composite ForeignKey to chapter is enough 
    # maybe make this optional

    chapter_id: Mapped[int]
    subject_id: Mapped[int]

    date: Mapped[Optional[date]]
    duration: Mapped[Optional[int]]  # minutes? hopefully
    remarks: Mapped[str]

    questions: Mapped[List["Question"]] = relationship(
        back_populates="quiz", cascade="all,delete-orphan"
    )
    quiz_attempts: Mapped[List["QuizAttempt"]] = relationship(
        back_populates="quiz", cascade="all,delete-orphan"
    )

    chapter: Mapped["Chapter"] = relationship(back_populates="quizzes") # maybe change this 
    #learning the hard way why we shouldn't use composite primary keys
    __table_args__ = (
        ForeignKeyConstraint(
            ['subject_id', 'chapter_id'],  # Composite foreign key
            ['chapter.subject_id', 'chapter.chapter_id']
        ),
    )

class Question(db.Model):
    __tablename__ = "question"
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.quiz_id"))
    question_id: Mapped[id_pk]
    text: Mapped[str]
    marks: Mapped[int]

    quiz: Mapped["Quiz"] = relationship(back_populates="questions")
    options: Mapped[List["Option"]] = relationship(
        back_populates="question", cascade="all,delete-orphan"
    )
    is_msq: Mapped[bool] = mapped_column(default=False)


class Option(db.Model):
    __tablename__ = "option"
    option_id: Mapped[id_pk]
    question_id: Mapped[int] = mapped_column(ForeignKey("question.question_id"))
    text: Mapped[str]
    is_correct: Mapped[bool] = mapped_column(
        default=False
    )  # Assuming default is not correct

    question: Mapped["Question"] = relationship(back_populates="options")
    question_attempts: Mapped[List["QuestionAttempt"]] = relationship(
        secondary="selected_option",
        back_populates="selected_options"
    )


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempt'

    id: Mapped[id_pk]
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.quiz_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    # start_time: Mapped[time]
    # end_time: Mapped[time]
    total_score: Mapped[int]
    percentage: Mapped[float]

    quiz: Mapped["Quiz"] = relationship(back_populates="quiz_attempts")
    user: Mapped["User"] = relationship(back_populates="quiz_attempts")
    question_attempts: Mapped[List["QuestionAttempt"]]=relationship(back_populates="quiz_attempt")


class QuestionAttempt(db.Model):
    __tablename__ = 'question_attempt'

    id: Mapped[id_pk]
    quiz_attempt_id: Mapped[int] = mapped_column(ForeignKey("quiz_attempt.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("question.question_id"))

    marks_gained: Mapped[int] = mapped_column(default=0)

    quiz_attempt: Mapped["QuizAttempt"] = relationship(back_populates="question_attempts")
    selected_options: Mapped[List["Option"]] = relationship(
        secondary="selected_option",
        back_populates="question_attempts"
    )

class SelectedOption(db.Model): #join table for many to many relationship between question_attempt and option
    __tablename__ = 'selected_option'
    question_attempt_id: Mapped[int] = mapped_column(ForeignKey("question_attempt.id"), primary_key=True)
    selected_option_id: Mapped[int] = mapped_column(ForeignKey("option.option_id"), primary_key=True)
