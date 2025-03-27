from app import create_app
from models import User, db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(user_id="0", username="admin", password="password")

    db.session.add(admin)
    db.session.commit()
