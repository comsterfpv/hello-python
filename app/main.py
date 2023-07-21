import random
import time
import requests

from flask import Flask, url_for, render_template, request, flash, redirect
from cryptography.fernet import Fernet

from possible_answers import possibleAnswers
from possible_guesses import possibleGuesses

app = Flask(__name__)

css_head = "<head><link rel='stylesheet' href='/style.css'></head>"
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/wordle', methods=('GET', 'POST'))
def looping():
    return render_template('create.html')
    turns = 0
    word = possibleAnswers[random.randint(0, len(possibleAnswers)-1)]

    turns_encrypted = f.encrypt(bytes(str(turns).encode()))
    word_encrypted = f.encrypt(bytes(word))
    
    word_payload = {'word': word_encrypted}
    requests.post('http://localhost:5000/wordle', data=word_payload)

    word = f.decrypt(requests.get('http://localhost:5000/wordle', data=word_payload)).decode
    turns = int(f.decrypt(requests.get('http://localhost:5000/wordle', data=word_payload)).decode)

    if turns < 6:
        correct, guessable = validate(word,turns)
        if not guessable:
            return render_template('create.html')
        elif correct:
            return render_template('create.html')
        return render_template('create.html')
        
    turns_payload = {'turns': turns_encrypted}
    requests.post('http://localhost:5000/wordle', data=turns_payload)

    turns+=1

def check(guess,word):
    temp = word
    ret = [0,0,0,0,0]
    for j in range(0, 5):
        if guess[j] == temp[j]:
            ret[j] = 2
            temp = temp[:j] + "!" + temp[j+1:]
    for j in range(0, 5):
        for k in range(0, 5):
            if j == k:
                continue
            if guess[j] == temp[k] and ret[j] != 2:
                ret[j] = 1
                temp = temp[:k] + "!" + temp[k+1:]
                break
            elif k == 4:
                pass
    return ret

def display(correct,status,word,guess,turns):
    if correct:
        flash("\nGreat job, you got it in " + str(turns+1) + "!", 'alert')
    else:
        pixels = -100
        for j in range(0,5):
            if status[j] == 2:
                flash(guess[j], 'green')
            elif status[j] == 1:
                flash(guess[j], 'yellow')
            else:
                flash(guess[j], 'white')
            pixels+=50
        flash(word, 'alert')
        if turns == 5:
            flash("Too bad! The answer was " + word + ".", 'alert')
            
def validate(word,turns):
    guessable = False
    correct = False
    if request.method == 'POST':
        guess = request.form['title'].lower()

        if not guess.isalpha():
            flash('Includes non-letters', 'alert')
        elif len(guess) != 5:
            flash('Not five letters', 'alert')
        else:
            for j in range(0, len(possibleGuesses)):
                if guess == possibleGuesses[j]:
                    guessable = True
                    status = check(guess,word) 
                    display(correct,status,word,guess,turns)
                    if status == [2,2,2,2,2]:
                        correct = True 
                        display(correct,status,word,guess,turns)
                        return(correct,guessable)

            if not guessable:
                flash('Not in word list', 'alert')
    return(correct,guessable)

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

@app.route("/factor/<int:n>")
def factor(n):
    ret = f"<html>{css_head}<body><h1>Factors of {n}</h1>\n<ul>"
    for j in range(1, n + 1):
        if (n/j)%1 == 0:
            url = url_for("factor", n = int(n/j))
            ret += f"<li><a href='{url}'>{int(n/j)}</a></li>\n"
    ret += "</ul>\n</body></html>"
    return ret, 200

@app.route("/random/<int:n>")
def randomGenerator(n):
    ret = f"<html><body><h1>5 random numbers from 0 to {n}</h1>\n<ul>"
    for j in range(5):
        rand = random.randint(0,n)
        ret += f"<li>{rand}</li>\n"
    ret += "</ul>\n</body></html>"
    return ret, 200

@app.route("/")
def hello():
    return "Hello from Python!"

@app.route("/style.css")
def style():
    return """body {
  background-color: lightblue;
}"""

if __name__ == "__main__":
    app.run(host='0.0.0.0')