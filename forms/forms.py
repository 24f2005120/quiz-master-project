from wtforms import Form, StringField 

class AuthForm(Form): # can be extended for different signup / login with class Signup(AuthForm)
    username = StringField('Username')
    password = StringField('Password')

