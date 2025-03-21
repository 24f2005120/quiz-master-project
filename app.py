from flask import Flask, request

from models import db
from routes import init_login_manager, init_routes


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = (
        "we aren't going to consider security much rn and its easy to setup later"
    )

    init_login_manager(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app


app = create_app()


@app.template_global()
def is_active(page_name):
    """used for checking which page to be highlighted in the navbar"""
    return "active" if request.endpoint == page_name else ""


init_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
