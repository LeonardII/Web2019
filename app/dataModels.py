from run import db

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(80), nullable=False)
    Password = db.Column(db.String(80), nullable=False)
    fragenRichtig = db.Column(db.Integer, default=0)
    def __repr__(self):
        return '<User %r>' % self.Name
