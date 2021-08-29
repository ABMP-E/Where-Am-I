import os
import json

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session



from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db1 = SQL("sqlite:///users.db")

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("Regestration.figma")

    else:
        fullname=request.form.get("fullname")
        username=request.form.get("username")
        emailid=request.form.get("emailid")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if(password!=confirm_password):
            return render_template("error.figma")

        db1.execute("INSERT INTO users(username,name,email_address,password,score) VALUES (:username,:name,:email,:password,0)",username=username,name=fullname,email=emailid, password=password)

        session["user_id"] = username

        return render_template("dashboard.figma")


@app.route("/login",methods=["GET","POST"])
def login():
    if(request.method=="GET"):
        return render_template("login.figma")

    else:
        if not request.form.get("username"):
            return render_template("error.figma")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.figma")


        rows = db1.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        if len(rows) != 1 or not (rows[0]["password"]==request.form.get("password")):
            return render_template("password_mismatch.figma")

        session["user_id"] = request.form.get("username")

@app.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
    if request.method == "GET":
        return render_template("dashboard.figma")



        

