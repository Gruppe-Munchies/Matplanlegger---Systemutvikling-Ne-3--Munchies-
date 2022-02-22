from database import db
from backend.server import app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    spade = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


with app.test_request_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Local db updated!")
