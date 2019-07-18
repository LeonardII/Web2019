from run import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Frage = db.Column(db.String(80), nullable=False)
    Option_eins = db.Column(db.String(80), nullable=False)
    Option_zwei = db.Column(db.String(80), nullable=False)
    Option_drei = db.Column(db.String(80), nullable=False)
    Option_vier = db.Column(db.String(80), nullable=False)
    Antwort = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Question %r>' % self.Frage

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    fragenRichtig = db.Column(db.Integer, default=0)
    def __repr__(self):
        return '<User %r>' % self.Name
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



