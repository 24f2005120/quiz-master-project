from flask import Blueprint, redirect, request
from flask_login import current_user

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods = ["GET", "POST"])
def home():
    if current_user.is_authenticated:
        return redirect("/redirect")
    if request.method
    if request.method=="GET":

