from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({"index":"1",
                    "Frage":"wie gross ist der Eiffelturm?",
                    "optionen":["200m","100m","500m","1km"]})

if __name__ == "__main__":
    app.run(debug=True)