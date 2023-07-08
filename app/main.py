from flask import Flask
app = Flask(__name__)

@app.route("/hi/<person>")
def hi(person):
    return "Hi " + person

@app.route("/")
def hello():
    return "Hello from Python!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
