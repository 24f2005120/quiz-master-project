from wtforms import Form, PasswordField, StringField


# can be extended for different signup / login with class Signup(AuthForm)
class AuthForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")
