from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select

from forms import AuthForm
from models import User, db

session = db.session

auth_bp = Blueprint("auth", __name__)


def select_user(username):
    return session.scalar(select(User).where(User.username == username))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect("/redirect")

    form = AuthForm(request.form)

    if request.method == "GET":
        return render_template("login.html", form=form)

    if request.method == "POST" and form.validate():
        user = select_user(form.data["username"])

        if not user:
            print("user not found error")
            return redirect(request.url)

        if user.password != form.data["password"]:
            print("incorrect password error ")
            return redirect(request.url)

        login_user(user)
        if user.username == "admin":
            return redirect("/admin")

        return redirect("/user")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect("/redirect")

    form = AuthForm(request.form)

    if request.method == "GET":
        return render_template("signup.html", form=form)

    if request.method == "POST" and form.validate():

        if select_user(form.data["username"]):
            print("user already exists error")
            return redirect("/signup")

        user = User(**form.data)
        session.add(user)
        session.commit()
        login_user(user)
        return redirect("/user")


@auth_bp.route("/redirect", methods=["GET", "POST"])
def already_authenticated():

    if not current_user.is_authenticated:
        print("this shouldn't have happened")
        return redirect("login")

    if current_user.username == "admin":
        return redirect("/admin")

    return redirect("/user")


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect("/")
