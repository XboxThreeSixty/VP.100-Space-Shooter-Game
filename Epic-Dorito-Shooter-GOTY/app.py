from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

connect = sqlite3.connect("database.db")
connect.execute("CREATE TABLE IF NOT EXISTS SCORES (name TEXT, score NUM)")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)