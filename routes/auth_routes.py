from flask import Blueprint, redirect, render_template, request
from flask_login import login_user
from sqlalchemy import select

from models import User, db

session = db.session

auth_bp = Blueprint("auth", __name__)


def select_user(username):
    return session.scalar(select(User).where(User.username == username))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = select_user(username)
        if user:
            login_user(user)
            if user.password != password:
                print("incorrect password error ")
                return redirect("/login")
            if user.username == "admin":
                return redirect("/admin")
            return redirect("/user")
        else:
            print("user not found error")
            return redirect("/login")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if select_user(username):
            print("user already exists error")
            return redirect("/signup")

        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        login_user(user)
        return redirect("/user")
