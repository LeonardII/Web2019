from flask import Flask, jsonify, render_template, json, flash, redirect, url_for, session
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

def jsonInsert(data):
    e = []
    for q in data:
        new_entry = Question(
         Frage=q['Frage'],
         Option_eins=q['Optionen'][0],
         Option_zwei=q['Optionen'][1],
         Option_drei=q['Optionen'][2],
         Option_vier=q['Optionen'][3],
          Antwort=q['Antwort'])
        e.append(new_entry)
        i+=1
    
    db.session.add_all(e)
    db.session.commit()

def insertQuestion(frage, optionen, antwort):
    if(len(optionen)==4):
        q = Question(Frage=frage,Option_eins=optionen[0],Option_zwei=optionen[1],Option_drei=optionen[2],Option_vier=optionen[3],Antwort=antwort)
        db.session.add(q)
        db.session.commit()

def getRandomQuestion():
    rand = random.randrange(0, session.query(Question).count())
    row = session.query(Question)[rand]
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


@app.route("/questions/")
@app.route("/questions/<int:index>")
def questions(index=None):
    allQuestions = json.load(open(os.path.join(os.path.realpath(os.path.dirname(__file__)), "questions.json"), "r"))
    if(index==None):
        return jsonify(allQuestions)

    return render_template('hello.html',frage=allQuestions[index]["Frage"],optionen=allQuestions[index]["Optionen"])

@app.route('/play')
def start():
    session['score'] = 0
    session['ques'] = 0
    return render_template('hello.html',fragen=allQuestions, index=0)  

@app.route('/answerQuestion/<int:ques>/<int:ans>', methods=['GET','POST'])
def answerQuestion(ques,ans):
    if( session.get('ques') <= ques ):
        if( int(allQuestions[ques]["Antwort"]) == ans ):
            flash( f'{allQuestions[ques]["Optionen"][ans]} is richtig ', 'success' )
            session['score']+=1
        else:
            flash(f'{allQuestions[ques]["Optionen"][ans]} is falsch ', 'success')

        session['ques']+=1
    else:
        flash('Schon beantwortet', 'success')



    if( ques >= len(allQuestions)-1):
        flash("",'success')
        form = ScoreSubmitForm()
        return render_template('score.html',form=form, score=str(session.get('score'))+"/"+str(len(allQuestions)))
    else:
        return render_template('hello.html',fragen=allQuestions, index=ques+1)



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
            return redirect(url_for('login'))

    return render_template('login.html', form=form)  

@app.route('/suggestQuestion', methods=['GET','POST'])
def suggestQuestion():
    form = SuggestQuestionForm()
    if form.validate_on_submit():
        right_ans = random.randrange(4) # 0-3
        optionen = deque([form.right_answer.data,form.false_answer_1.data,form.false_answer_2.data,form.false_answer_3.data])
        
        for x in range(right_ans):
            optionen.appendleft(optionen.pop())


        q = Question(Frage=form.question.data,Option_eins=optionen[0],Option_zwei=optionen[1],Option_drei=optionen[2],Option_vier=optionen[3],Antwort=right_ans)
        db.session.add(q)
        db.session.commit()

    return render_template('suggestQuestion.html', form=form)  

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/submit')
def submit():
    return render_template('highscore.html')



if __name__ == "__main__":
    app.run()