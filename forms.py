from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FieldList,
    FormField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Optional


# can be extended for different signup / login with class Signup(AuthForm)
class AuthForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class SubjectForm(FlaskForm):
    subject_name = StringField("Subject Name", validators=[DataRequired()])
    description = TextAreaField("Description")


class ChapterForm(FlaskForm):
    chapter_name = StringField("Chapter Name", validators=[DataRequired()])
    description = TextAreaField("Description")


class QuizForm(FlaskForm):
    quiz_name = StringField("Quiz Name", validators=[DataRequired()])
    date = DateField("Date", validators=[Optional()])
    duration = IntegerField("Duration (minutes)", validators=[Optional()])
    remarks = TextAreaField("Remarks")


class OptionForm(FlaskForm):
    text = TextAreaField("Option Text", validators=[DataRequired()])
    is_correct = BooleanField("Is Correct")


class QuestionForm(FlaskForm):
    text = TextAreaField("Question Text", validators=[DataRequired()])
    marks = IntegerField("Marks", validators=[DataRequired()], default=1)
    options = FieldList(
        FormField(OptionForm),
        min_entries=1,
        max_entries=10,
        label="Options",
    )


class editQuestionForm(FlaskForm):
    text = TextAreaField("Question Text", validators=[DataRequired()])
    marks = IntegerField("Marks", validators=[DataRequired()], default=1)
