from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("smartlab.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment TEXT,
            lab TEXT,
            instructor TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        experiment = request.form["experiment"]
        lab = request.form["lab"]
        instructor = request.form["instructor"]
        date = request.form["date"]
        time = request.form["time"]

        conn = sqlite3.connect("smartlab.db")
        conn.execute(
            "INSERT INTO schedules (experiment, lab, instructor, date, time) VALUES (?, ?, ?, ?, ?)",
            (experiment, lab, instructor, date, time)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    conn = sqlite3.connect("smartlab.db")
    schedules = conn.execute("SELECT * FROM schedules").fetchall()
    conn.close()
    return render_template("index.html", schedules=schedules)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)