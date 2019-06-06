from flask import Flask, jsonify, render_template, json
import os

app = Flask(__name__)

@app.route("/questions/")
@app.route("/questions/<int:index>")
def questions(index=None):
    allQuestions = json.load(open(os.path.join(os.path.realpath(os.path.dirname(__file__)), "questions.json"), "r"))
    if(index==None):
        return jsonify(allQuestions)

    return render_template('hello.html',frage=allQuestions[index]["Frage"],optionen=allQuestions[index]["Optionen"])

@app.route('/')
def start():
    return render_template('test.html')  


@app.route('/register')
def register():
    return render_template('register.html')  

if __name__ == "__main__":
    app.run(debug=True)