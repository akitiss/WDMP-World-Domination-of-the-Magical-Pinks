'''
WDMP: . . .
'''

from flask import Flask, session, render_template, request, redirect, url_for

app = Flask(__name__)
#HARD user and pass
user = "user"
passwd = "pass"

@app.route("/", methods=["GET", "POST"])
def login():
    if ( request.method == "GET" ):
        return render_template("login.html")
    if ( request.form.get("username") == user and request.form.get("password") == passwd ):
        return redirect(url_for("home_page"))

@app.route("/Home", methods=["GET", "POST"])
def home_page():
    return "heLLO"

if __name__ == "__main__":
    app.debug = True
    app.run()