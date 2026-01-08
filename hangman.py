from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

WORDS = {
    "Tech": ['algorithm', 'cybersecurity', 'blockchain', 'encryption', 'developer',
             'python', 'javascript', 'database', 'programming', 'software'],
    "Animal": ['elephant', 'giraffe', 'kangaroo', 'penguin', 'cheetah',
               'dolphin', 'butterfly', 'crocodile', 'rhinoceros', 'octopus'],
    "Fruit": ['strawberry', 'pineapple', 'watermelon', 'blueberry', 'raspberry',
              'banana', 'orange', 'mango', 'papaya', 'coconut'],
    "Country": ['australia', 'brazil', 'canada', 'germany', 'japan',
                'mexico', 'spain', 'thailand', 'argentina', 'portugal']
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        category = request.form.get("category")
        word = random.choice(WORDS[category]).upper()

        session["word"] = word
        session["display"] = "_" * len(word)
        session["attempts"] = 6
        session["guessed"] = []
        session["category"] = category

        return redirect(url_for("game"))

    return render_template("index.html", page="menu")


@app.route("/game", methods=["GET", "POST"])
def game():
    if "word" not in session:
        return redirect(url_for("index"))

    word = session["word"]
    display = session["display"]
    attempts = session["attempts"]
    guessed = session["guessed"]
    category = session["category"]

    message = ""

    if request.method == "POST":
        guess = request.form.get("guess").upper()

        if len(guess) != 1 or not guess.isalpha():
            message = "Enter only one letter!"
        elif guess in guessed:
            message = "You already guessed that letter!"
        else:
            guessed.append(guess)

            if guess in word:
                new_display = ""
                for i in range(len(word)):
                    if word[i] in guessed:
                        new_display += word[i]
                    else:
                        new_display += "_"
                display = new_display
                message = "Good guess!"
            else:
                attempts -= 1
                message = "Wrong guess!"

    session["display"] = display
    session["attempts"] = attempts
    session["guessed"] = guessed

    win = "_" not in display
    lose = attempts <= 0

    return render_template(
        "index.html",
        page="game",
        display=display,
        attempts=attempts,
        guessed=guessed,
        category=category,
        message=message,
        word=word,
        win=win,
        lose=lose
    )


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
