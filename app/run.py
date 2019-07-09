from flask import Flask, jsonify, render_template, json, flash, redirect, url_for
import os
from forms import RegistrationForm, LoginForm, ScoreSubmitForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '123a25d7a9273d2e115c87095c028cc1'
allQuestions = json.load(open(os.path.join(os.path.realpath(os.path.dirname(__file__)), "questions.json"), "r"))
score = 0


@app.route("/questions/")
@app.route("/questions/<int:index>")
def questions(index=None):
    allQuestions = json.load(open(os.path.join(os.path.realpath(os.path.dirname(__file__)), "questions.json"), "r"))
    if(index==None):
        return jsonify(allQuestions)

    return render_template('hello.html',frage=allQuestions[index]["Frage"],optionen=allQuestions[index]["Optionen"])

@app.route('/play')
def start():
    global score
    score = 0
    return render_template('hello.html',fragen=allQuestions, index=0)  

@app.route('/answerQuestion/<int:ques>/<int:ans>', methods=['GET','POST'])
def answerQuestion(ques,ans):
    if(int(allQuestions[ques]["Antwort"]) == ans):
        flash(f'{allQuestions[ques]["Optionen"][ans]} is richtig ', 'success')
        global score
        score+=1
    else:
        flash(f'{allQuestions[ques]["Optionen"][ans]} is falsch ', 'success')

    if( ques >= len(allQuestions)-1):
        flash("",'success')
        form = ScoreSubmitForm()
        return render_template('score.html',form=form, score=str(score)+"/"+str(len(allQuestions)))
    else:
        return render_template('hello.html',fragen=allQuestions, index=ques+1)



@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account erstell für {form.username.data}!', 'success')
        return redirect(url_for('start'))
    return render_template('register.html', form=form)  

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)  

@app.route('/submit')
def submit():
    return render_template('highscore.html')

if __name__ == "__main__":
    app.run()