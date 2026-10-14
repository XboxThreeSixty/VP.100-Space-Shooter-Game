from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

connect = sqlite3.connect("database.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == "POST":
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            # these variables are here as placeholders
            username = "placeholder"
            playerScore = 0
            cursor.execute("INSERT INTO leaderboard VALUES(?, ?)", (username, playerScore))
            users.commit()
            return render_template("index.html")
    else:
        pass

if __name__ == "__main__":
    app.run(debug = True)