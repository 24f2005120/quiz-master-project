from flask import Flask, render_template, requests

app = Flask(__name__)

app.route("/", methods=["GET"])


def home():
    return "<h1>Hello World<\\h1>"
