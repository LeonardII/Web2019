from flask import Flask, jsonify, render_template, json, flash, redirect, url_for, session
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm, ScoreSubmitForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '123a25d7a9273d2e115c87095c028cc1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://GzkqBfvtZN:nfhSObaxFY@remotemysql.com:3306/GzkqBfvtZN'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

from dataModels import *

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
        flash(f'Account erstell für {form.username.data}!', 'success')
        return redirect(url_for('start'))
    return render_template('register.html', form=form)  

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('play'))
    return render_template('login.html', form=form)  

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

