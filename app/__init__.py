'''
WDMP: . . .
'''

from flask import Flask, session, render_template, request, redirect, url_for
from db import *
from amadeus import *
#from test import *

app = Flask(__name__)
app.secret_key = "tmep"


@app.route("/login", methods=["GET", "POST"])
def login():
    if ( request.method == "GET" ):
        return render_template("login.html") # This is for accessing the page
    Input0 = request.form.get("username")
    Input1 = request.form.get("password")
    session_id = account_match(Input0, Input1)
    #city = get_rand_city()
    #link = get_city_img(city['city'])
    if ( session_id != None ):
        session["ID"] = session_id
        return redirect(url_for("home_page"))
    return render_template("login.html", bkg = city, response="Username and passwords do not match.")

@app.route("/", methods=["GET", "POST"])
def home_page():
    if(session.get("ID", None) == None):
        stat = "Please Login"
        return redirect(url_for("login"))
    else:
        print("ID IS : " + str(session['ID']))
        stat = F"Logged in as {get_username(session['ID'])}"
    return render_template("home_page.html", status=stat)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("ID",None) # removes session info, retunrs nothing if not there
    return redirect(url_for("login", status="Please login"))

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if( request.method == "GET"): # display page
        return render_template("register.html", status="Enter a username and password")
    Input0 = request.form.get("username")
    Input1 = request.form.get("password")
    Input2 = request.form.get("password_confirm")
    if Input1 == Input2:
        Session_id = register_new_user(Input0, Input1)
        if( Session_id != -1 ): # see if new user info is already in use, if not then sign them in
            session["ID"] = Session_id
            return redirect(url_for("home_page"))
        return render_template("register.html", status="Login info is in use.")
    else:
        return render_template("register.html", status="Passwords do not match.")

@app.route("/create_trip_location1", methods=["GET", "POST"])
def create_trip():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    #print(request.args.get("start"))

    start_city_input = request.args.get("start_input", "")
    end_city_input = request.args.get("end_input", "")
    end_city_iata = request.args.get("end_iata", "")
    start_city_iata = request.args.get("start_iata", "")
    start_cities_dict = {}
    end_cities_dict = {}
    if(request.args.get("start") != None):
        start_cities_dict = get_cities_dict(request.args.get("start"))
    if(request.args.get("end") != None):
        end_cities_dict = get_cities_dict(request.args.get("end"))
    return render_template("create_trip_location1.html", START_CITIES=start_cities_dict, END_CITIES=end_cities_dict, start_value=start_city_input, end_value=end_city_input, IATA_S=start_city_iata, IATA_E=end_city_iata)

@app.route("/search_location_from", methods=["POST"])
def search_location_from():
    previous_input = request.form.get("input_city")
    iata_start = request.form.get("selected_iata_start")
    iata_end = request.form.get("selected_iata_end")
    end_city_input = request.form.get("selected_city_end", "")
    start_city_input = request.form.get("selected_city_start", "")
    return redirect(url_for("create_trip", start=previous_input, end_input=end_city_input, start_input=start_city_input, start_iata=iata_start, end_iata=iata_end))

@app.route("/search_location_to", methods=["POST"])
def search_location_to():
    previous_input = request.form.get("input_city")
    iata_start = request.form.get("selected_iata_start")
    iata_end = request.form.get("selected_iata_end")
    start_city_input = request.form.get("selected_city_start", "")
    end_city_input = request.form.get("selected_city_end", "")
    return redirect(url_for("create_trip", end=previous_input, end_input=end_city_input, start_input=start_city_input, start_iata=iata_start, end_iata=iata_end))

@app.route("/post_location", methods=["GET", "POST"])
def post_location():
    #if user DID NOT fill in all fields, return error message 
    trip_name = request.form.get("trip_name")
    trip_count = request.form.get("trip_count")
    city = request.form.get("selected_city")
    end_date = request.form.get("end_date")
    start_date = request.form.get("start_date")
    start_location = request.form.get("selected_city_start")
    end_location = request.form.get("selected_city_end")
    print("START: " + start_location)
    print("END: " + end_location)
    #add to db
    return redirect(url_for("flights")) 
    
@app.route("/flights", methods=["GET", "POST"])
def flights():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    return render_template("create_trip_flights.html")

@app.route("/post_flights", methods=["GET", "POST"])
def post_flights():
    #if user DID NOT fill in all fields, return error message 
    flight = request.form.get("flights")
    #add to db
    return redirect(url_for("create_activities")) 

@app.route("/create_activities", methods=["GET", "POST"])
def create_activities():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    return render_template("create_trip_activities.html")

@app.route("/post_activities", methods=["GET", "POST"])
def post_activities():
    #if user DID NOT fill in all fields, return error message 
    activity_count = request.form.get("activity_count")
    #add to db
    return redirect(url_for("create_activities_display"))

@app.route("/create_activities_display", methods=["GET", "POST"])
def create_activities_display():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    return render_template("create_trip_activities_display.html")

@app.route("/hotels", methods=["GET", "POST"])
def create_hotel():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    return render_template("create_trip_hotels.html")

@app.route("/post_hotels", methods=["GET", "POST"])
def post_hotels():
    #if user DID NOT fill in all fields, return error message 
    hotel = request.form.get("hotel")
    #add to db
    return redirect(url_for("saved_trips"))

@app.route("/saved_trips", methods=["GET", "POST"])
def saved_trips():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    return render_template("saved_trips.html")

@app.route("/trip", methods=["GET", "POST"])
def trip():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    return render_template("trip.html")


if __name__ == "__main__":
    app.debug = True
    app.run()