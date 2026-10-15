from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

connect = sqlite3.connect("database.db")
connect.execute("CREATE TABLE IF NOT EXISTS leaderboard (id INTEGER AUTO_INCREMENT PRIMARY KEY, username TEXT, score INTEGER)")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/post/<username>/<playerScore>", methods=["GET", "POST"])
def post(username, playerScore):
    if request.method == "POST":
        print("request method works")
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO leaderboard (username, score) VALUES(?, ?)", (username, playerScore))
            users.commit()
            return render_template("index.html")
    else:
        print("did not add to database")
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)