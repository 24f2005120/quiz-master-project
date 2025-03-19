from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


# can be extended for different signup / login with class Signup(AuthForm)
class AuthForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class SubjectForm(FlaskForm):
    subject_name = StringField("Subject Name", validators=[DataRequired()])
    description = StringField("Description")


class ChapterForm(FlaskForm):
    chapter_name = StringField("Chapter Name", validators=[DataRequired()])
    description = StringField("Description")
