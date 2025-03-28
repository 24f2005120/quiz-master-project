from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from forms import AuthForm
from models import db
from models.models import User
from utils.db_utils import select_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect("/redirect")

    form = AuthForm()

    if request.method == "GET":
        return render_template("login.html", form=form)

    if request.method == "POST" and form.validate_on_submit:
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

    form = AuthForm()

    if request.method == "GET":
        return render_template("signup.html", form=form)

    if request.method == "POST" and form.validate_on_submit:
        if select_user(form.data["username"]):
            print("user already exists error")
            return redirect("/signup")

        user = User()
        form.populate_obj(user)
        session.add(user)
        session.commit()
        login_user(user)
        return redirect("/user")

    return "Not supposed to happen"


@auth_bp.route("/redirect", methods=["GET", "POST"])
def already_authenticated():

    if not current_user.is_authenticated:
        print("this shouldn't have happened")
        return redirect("login")

    if current_user.username == "admin":
        return redirect("/admin")

    return redirect(url_for("user.home"))


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect("/")
