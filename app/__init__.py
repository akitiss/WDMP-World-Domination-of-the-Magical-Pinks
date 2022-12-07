'''
WDMP: . . .
'''

from flask import Flask, session, render_template, request, redirect, url_for

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
            session["USERNAME"] = request.form.get("username")
            return redirect(url_for("home_page"))
        return render_template("login.html", response="The Username and Password do not match")
    return render_template("login.html", response="Please Enter a Valid Username")

@app.route("/", methods=["GET", "POST"])
def home_page():
    if(session.get("USERNAME", None) == None):
        stat = "Please Login"
    else:
        stat = F"Logged in as {session['USERNAME']}"
    return render_template("index.html", status=stat)

if __name__ == "__main__":
    app.debug = True
    app.run()