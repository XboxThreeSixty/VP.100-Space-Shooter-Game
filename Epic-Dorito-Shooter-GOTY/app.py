from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

connect = sqlite3.connect("database.db")

def sortingCriteria(givenTuple):
    return givenTuple[2]

# used for people going onto the website normally 
@app.route("/")
def index():
    connect = sqlite3.connect("database.db")
    indexCursor = connect.cursor()
    indexCursor.execute("SELECT * FROM leaderboard")
    data = indexCursor.fetchall()

    # sorting the list of tuples greatest to least and only taking the top 5
    if len(data) > 1:
        data.sort(reverse=True, key=sortingCriteria)
    if len(data) > 5:
        while len(data) != 5:
            data.pop(5)

    return render_template("index.html", items=data)

# used for HTTP requests sent by game.py
@app.route("/post/<username>/<playerScore>/<date>", methods=["GET", "POST"])
def post(username, playerScore, date):
    if request.method == "POST":
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO leaderboard (username, score, date) VALUES(?, ?, ?)", (username, playerScore, date))
            users.commit()
            return render_template("index.html")
    else:
        print("did not add to database")
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)

# SQL command to make the leaderboard table in case I need it for whatever reason
# CREATE TABLE IF NOT EXISTS leaderboard (id INT AUTO_INCREMENT PRIMARY KEY, username TEXT NOT NULL, score INT)