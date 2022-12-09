'''
WDMP: . . .
'''

from flask import Flask, session, render_template, request, redirect, url_for
from db import *

app = Flask(__name__)
app.secret_key = "tmep"
# user and pass
user = "user"
passwd = "pass"

@app.route("/login", methods=["GET", "POST"])
def login():
    if ( request.method == "GET" ):
        return render_template("login.html") # This is for accessing the page
    if ( request.form.get("username") == user ):
        if( request.form.get("password") == passwd ):
            session["ID"] = request.form.get("username") # change to session id.
            return redirect(url_for("home_page"))
        return render_template("login.html", response="The Username and Password do not match")
    return render_template("login.html", response="Please Enter a Valid Username")

@app.route("/", methods=["GET", "POST"])
def home_page():
    if(session.get("ID", None) == None):
        stat = "Please Login"
    else:
        stat = F"Logged in as {session['ID']}"
    return render_template("index.html", status=stat)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("ID",None) # removes session info, retunrs nothing if not there
    return redirect(url_for("home_page", status="Please Login"))

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if( request.method == "GET"):
        return render_template("register.html", message="Enter a Username and password")
    Input0 = request.form.get("username")
    Input1 = request.form.get("password")
    Session_id = register_new_user(Input0, Input1)
    if( Session_id != None ):
        session["ID"] = Session_id
        return redirect(url_for("home_page"))
    return render_template("register.html", message="Login Info is in use")

if __name__ == "__main__":
    app.debug = True
    app.run()