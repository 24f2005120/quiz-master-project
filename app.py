from flask import Flask, render_template, request

import models
from database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    return "<h1>Hello World</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
