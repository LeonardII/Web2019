from flask import Flask, jsonify, render_template, json, flash, redirect, url_for, session, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_manager, LoginManager, login_required, current_user, login_user, logout_user
from forms import *
import random
from collections import deque

app = Flask(__name__)

app.config['SECRET_KEY'] = '123a25d7a9273d2e115c87095c028cc1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://GzkqBfvtZN:nfhSObaxFY@remotemysql.com:3306/GzkqBfvtZN'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

from dataModels import *

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


def insertQuestion(frage, optionen, antwort):
    if(len(optionen)==4):
        q = Question(Frage=frage,Option_eins=optionen[0],Option_zwei=optionen[1],Option_drei=optionen[2],Option_vier=optionen[3],Antwort=antwort)
        db.session.add(q)
        db.session.commit()

def getRandomQuestion():
    rand = random.randrange(0, db.session.query(Question).count())
    row = db.session.query(Question)[rand]
    return row

def getQuestion(i):
    row = db.session.query(Question).filter_by(id=i).first()
    db.session.commit()
    return row
        

def addUser(name, email, passwort):
    u = User(Name=name, Email=email)
    u.set_password(passwort)
    db.session.add(u)
    db.session.commit()

def getUser(email):
    q = User.query.filter_by(Email=email).first()
    db.session.commit()
    return q

allQuestions = json.load(open(os.path.join(os.path.realpath(os.path.dirname(__file__)), "questions.json"), "r"))


@app.route('/play')
def start():
    nextQuestion = getRandomQuestion()
    return redirect(url_for('answerQuestion',qid=1))  

@app.route('/answerQuestion/<int:qid>', methods=['GET','POST'])
def answerQuestion(qid=0):
    form = AnswerQuestionForm()
    if request.method=='POST':
        antwort = None
        if form.option_eins.data:
            antwort = 0
        elif form.option_zwei.data:
            antwort = 1
        elif form.option_drei.data:
            antwort = 2
        elif form.option_vier.data:
            antwort = 3

        frage = getQuestion(qid)
        print("Frage: ",frage)

        if( int(frage.Antwort) == antwort):
            flash('Richtig ', 'success' )
        else:
            flash('Falsch ', 'success')


    nextQuestion = getRandomQuestion()
    return render_template('hello.html',frage=nextQuestion, form=form)



@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(f'Account erstell für {form.username.data}!', 'success')
        addUser(form.username.data,form.email.data,form.password.data)
        return redirect(url_for('start'))
    return render_template('register.html', form=form)  



@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('start'))
    form = LoginForm()
    if form.validate_on_submit():
        user = getUser(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('start'))
        else:
            flash("Login fehlgeschlagen, versuche ein anderes Passwort!",category="login")
            return redirect(url_for('login'))
    else:
        flash("Login fehlgeschlagen, Email ungültig!",category="login")

    return render_template('login.html', form=form)  

@app.route('/suggestQuestion', methods=['GET','POST'])
def suggestQuestion():
    form = SuggestQuestionForm()
    if form.validate_on_submit():
        right_ans = random.randrange(4) # 0-3
        optionen = deque([form.right_answer.data,form.false_answer_1.data,form.false_answer_2.data,form.false_answer_3.data])
        
        for x in range(right_ans):
            optionen.appendleft(optionen.pop())


        q = Question(Frage=str(form.question.data),Option_eins=str(optionen[0]),Option_zwei=str(optionen[1]),
        Option_drei=str(optionen[2]),Option_vier=str(optionen[3]),Antwort=str(right_ans))
        db.session.add(q)
        db.session.commit()

    return render_template('suggestQuestion.html', form=form)  

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




if __name__ == "__main__":
    app.run()