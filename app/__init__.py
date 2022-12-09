'''
WDMP: . . .
'''

from flask import Flask, session, render_template, request, redirect, url_for
from db import *

app = Flask(__name__)
app.secret_key = "tmep"


@app.route("/login", methods=["GET", "POST"])
def login():
    if ( request.method == "GET" ):
        return render_template("login.html") # This is for accessing the page
    Input0 = request.form.get("username")
    Input1 = request.form.get("password")
    session_id = account_match(Input0, Input1)
    if ( session_id != None ):
        session["ID"] = session_id
        return redirect(url_for("home_page"))
    return render_template("login.html", response="Username and Passwords do not match")

@app.route("/", methods=["GET", "POST"])
def home_page():
    if(session.get("ID", None) == None):
        stat = "Please Login"
    else:
        print("ID IS : " + str(session['ID']))
        stat = F"Logged in as {get_username(session['ID'])}"
    return render_template("home_page.html", status=stat)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("ID",None) # removes session info, retunrs nothing if not there
    return redirect(url_for("home_page", status="Please Login"))

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if( request.method == "GET"): # display page
        return render_template("register.html", status="Enter a Username and password")
    Input0 = request.form.get("username")
    Input1 = request.form.get("password")
    Session_id = register_new_user(Input0, Input1)
    if( Session_id != -1 ): # see if new user info is already in use, if not then sign them in
        session["ID"] = Session_id
        return redirect(url_for("home_page"))
    return render_template("register.html", status="Login Info is in use")

@app.route("/create_trip", methods=["GET", "POST"])
def create_trip():
    return render_template("create_trip.html")

@app.route("/saved_trips", methods=["GET", "POST"])
def saved_trips():
    return render_template("saved_trips.html")

@app.route("/trip", methods=["GET", "POST"])
def trip():
    return render_template("trip.html")


if __name__ == "__main__":
    app.debug = True
    app.run()