from flask import Flask
app = Flask(__name__)

@app.route("/hi/<person>")
def hi(person):
    return "Hi " + person

@app.route("/fancyhi/<person>")
def fancyhi(person):
    return f"""<html>
<body>
<h1>
Fancy Greetings
</h1>
I want to wish you a very hearty hello!
Enjoy your day, {person}
<br>
Enough for now!
</body>
</html>
"""

@app.route("/count/<int:n>")
def count(n):
    ret = f"<html><body><h1>Counting to {n}</h1>\n<ul>"
    for j in range(1, n + 1):
        ret += f"<li>{j}</li>\n"
    ret += "</ul>\n</body></html>"
    return ret, 200

@app.route("/")
def hello():
    return "Hello from Python!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
