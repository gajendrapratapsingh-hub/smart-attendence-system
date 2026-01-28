from flask import Flask, render_template, redirect, url_for, session, send_file
import pandas as pd
import os
from face_recog import start_camera

app = Flask(__name__)
app.secret_key = "attendance_secret"

USERNAME = "Gajendra"
PASSWORD = "31072004"

@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def do_login():
    from flask import request
    username = request.form["username"]
    password = request.form["password"]

    if username == USERNAME and password == PASSWORD:
        session["logged_in"] = True
        return redirect(url_for("dashboard"))
    return "Invalid credentials"

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/start")
def start():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    start_camera()
    return redirect(url_for("attendance"))

@app.route("/attendance")
def attendance():
    if not os.path.exists("attendance/attendance.csv"):
        return "No attendance file found."

    df = pd.read_csv("attendance/attendance.csv")
    return render_template("attendance.html", tables=df.values.tolist(), titles=df.columns.tolist())

@app.route("/download/excel")
def download_excel():
    return send_file("attendance/attendance.xlsx", as_attachment=True)

@app.route("/download/pdf")
def download_pdf():
    return send_file("reports/attendance.pdf", as_attachment=True)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
