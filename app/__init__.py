'''
WDMP: . . .
'''

from flask import Flask, session, render_template, request, redirect, url_for
from db import *
from amadeus import *
from opentripmap import *
from weather import *
from google_maps import *
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
    return render_template("login.html", response="Username and passwords do not match.")

@app.route("/", methods=["GET", "POST"])
def home_page():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    elif (get_username(session.get("ID")) == None):
        return redirect(url_for("login"))
    else:
        #print("ID IS : " + str(session['ID']))
        # stat = F"Logged in as {get_username(session['ID'])}"
        session_user = F"{get_username(session['ID'])}"
    return render_template("home_page.html", user=session_user) #status=stat

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("ID",None) # removes session info, retunrs nothing if not there
    return redirect(url_for("login", status="Please login"))

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if( request.method == "GET"): # display page
        return render_template("register.html")
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

@app.route("/account", methods = ["GET", "POST"])
def account():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    account_user = F"{get_username(session['ID'])}"
    account_password = F"{get_password(session['ID'])}"
    return render_template("account.html", user=account_user, passw=account_password)

@app.route("/create_trip_location", methods=["GET", "POST"])
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
    account_user = F"{get_username(session['ID'])}"
    return render_template("create_trip_location.html", START_CITIES=start_cities_dict, END_CITIES=end_cities_dict, start_value=start_city_input, end_value=end_city_input, IATA_S=start_city_iata, IATA_E=end_city_iata, user=account_user)

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
    
@app.route("/flights", methods=["GET", "POST"])
def flights():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    if(request.method == "POST"):
        trip_name = request.form.get("trip_name")
        trip_count = request.form.get("trip_count")
        end_date = request.form.get("end_date")
        start_date = request.form.get("start_date")
        start_location = request.form.get("selected_city_start")
        end_location = request.form.get("selected_city_end")
        start_iata = request.form.get("selected_iata_start")
        end_iata = request.form.get("selected_iata_end")

        flights = get_flight_dict(start_iata, end_iata, start_date, end_date, trip_count)
        result = []
        status = ""
        if (flights == []):
            status = "There are no flights found."
        for data in flights:
            instance = {}
            instance["start-time"] = data["start-time"].split("T") # splits yyyy-mm-ddThh:mm:ss in the middle
            instance["end-time"] = data["end-time"].split("T")
            instance["nice-start-time"] = make_date(data["start-time"])
            instance["nice-end-time"] = make_date(data["end-time"])
            instance["price"] = data["price"]
            instance["company"] = data["company"]
            result.append(instance)

        # Each dictionary will have: start-time: "yyyy-mm-dd", end-time: "yyyy-mm-dd", price: "total_price", company: "company"
    return render_template("create_trip_flights.html", FLIGHTS=result, NAME=trip_name, END_LOCATION=end_location, START_LOCATION=start_location, COUNT=trip_count, STATUS=status)
    

@app.route("/post_flights", methods=["GET", "POST"])
def post_flights():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))

    start_location = request.form.get("start_location")
    end_location = request.form.get("end_location")
    count = request.form.get("trip_count")
    name = request.form.get("trip_name")
    end_date = request.form.get("end_date")
    start_date = request.form.get("start_date")
    price = request.form.get("price")
    company = request.form.get("company")

    trip_id = add_saved_trip(session.get("ID"), name, end_date, start_date, start_location, end_location, count, price, company)
    return redirect(url_for("create_activities", Location=end_location, ID=trip_id))

@app.route("/create_activities", methods=["GET", "POST"])
def create_activities():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    location = request.args.get("Location", None)
    trip_id = request.args.get("ID", None)
    if ( location == None ):
        return redirect(url_for("create_trip"))
    act_list = ['hot_springs', 'volcanoes', 'museums', 'art_galleries', 'adult', 'circuses', 'historical_places', 'castles', 'churches', 'architecture', 'amusements', 'sport', 'casino', 'malls', 'foods']
    return render_template("create_trip_activities.html", LOCATION=location, ID=trip_id, ACTIVITY_LIST=act_list)

@app.route("/create_activities_display", methods=["GET", "POST"])
def create_activities_display():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    trip_id = request.form.get("trip_id")
    if(trip_id == None): # If for some reason the trip_id is empty, send user back to the create trips page
        return redirect(url_for("create_trip"))
    
    city = request.form.get("location", None)
    activity_count = request.form.get("activity_count", 1)
    act_list = ['hot_springs', 'volcanoes', 'museums', 'art_galleries', 'adult', 'circuses', 'historical_places', 'castles', 'churches', 'architecture', 'amusements', 'sport', 'casino', 'malls', 'foods']
    selected_activities = []

    for x in act_list:
        if(request.form.get(x, "False") == "True"):
            selected_activities.append(x)
    if(len(selected_activities) == 0):
        return render_template("create_trip_activities_display.html") # ERROR user didnt select any activities
    places_dict = get_places(city, 5000, selected_activities, int(activity_count)) 
    data = []
    for place_dict in places_dict:
        for place in place_dict:
            info = {
                "name": place, # ----------add more data we need here----------
                "xid": place_dict[place]["xid"],
                "url": place_dict[place]["url"],
                "lat": place_dict[place]["lat"],
                "lon": place_dict[place]["lon"],
                "category": place_dict[place]["category"],
                "image": (get_img_link(place_dict[place]["lat"], place_dict[place]["lon"]))
            }
            add_place(trip_id, info["xid"], info["name"], info["url"], info["lat"], info["lon"], info["category"]) # adds place to DB
            data.append(info)
    #print("DATA: "+ str(data))
    return render_template("create_trip_activities_display.html", ACTIVITIES=data, TRIP_ID=trip_id, LOCATION=city)

@app.route("/hotels", methods=["GET", "POST"])
def create_hotel():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    trip_id = request.form.get("trip_id")
    if(trip_id == None): # If for some reason the trip_id is empty, send user back to the create trips page
        return redirect(url_for("create_trip"))

    city = request.form.get("location", None)
    hotel_dict = get_hotels(city, 9)
    hotel_data = []
    for hotel in hotel_dict:
        entry = {
            "name": hotel,
            "url": hotel_dict[hotel]["url"],
            "xid": hotel_dict[hotel]["xid"],
            "lat": hotel_dict[hotel]["lat"],
            "lon": hotel_dict[hotel]["lon"],
        } # trip_id, hotel_id, name, url, lat, lon
        hotel_data.append(entry)
    return render_template("create_trip_hotels.html", HOTELS=hotel_data, TRIP_ID=trip_id)

@app.route("/post_hotels", methods=["GET", "POST"])
def post_hotels():
    #if user DID NOT fill in all fields, return error message 
    trip_id = request.form.get("trip_id")
    url = request.form.get("url")
    xid = request.form.get("xid")
    lon = request.form.get("lon")
    lat = request.form.get("lat")
    name = request.form.get("name")
    #add to db
    add_hotel(trip_id, xid, name, url, lat, lon)
    return redirect(url_for("saved_trips"))

@app.route("/saved_trips", methods=["GET", "POST"])
def saved_trips():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    trips_id = get_savedtrips(session.get('ID'))
    all_data = []
    for trip_id in trips_id:
        trip_info = get_trip_info(trip_id)
        trip_data = {
            "name": trip_info[2],
            "start_date": make_date(trip_info[3]),
            "end_date": make_date(trip_info[4]),
            "start_location": trip_info[5],
            "end_location": trip_info[6],
            "trip_id": trip_info[0]
        }
        all_data.append(trip_data)
    all_data = all_data[::-1]
    account_user = F"{get_username(session['ID'])}"
    return render_template("saved_trips.html", TRIPS_LIST=all_data, user=account_user)

@app.route("/trip", methods=["GET", "POST"])
def trip():
    if(session.get("ID", None) == None):
        return redirect(url_for("login"))
    trip_id = request.form.get("trip_id")
    trip_info = get_trip_info(trip_id)
    flight_info = get_flight_info(trip_info[1])
    places_id = get_all_places_id(int(trip_id))
    places_info = []
    for id in places_id:
        info = get_place_info(id)
        if len(info) > 0:
            place = {
                "name": info[0][1],
                "url": info[0][2],
                "image": get_img_link(info[0][3], info[0][4]), 
                "category": info[0][5],  
            }
            places_info.append(place)
    #making dates pretty
    trip_start_date = make_date(trip_info[4])
    trip_end_date = make_date(trip_info[3])
    flight_start_date = make_date(flight_info[3])
    flight_end_date = make_date(flight_info[4])
    weather_data = get_weather(trip_info[6])
    hotel = get_hotel(trip_id)
    print(hotel)
    if (weather_data == []):
        status_weather = "Sorry the weather API is not working right now!"
    else:
        status_weather = "Check out the weather!"
    #trip_id int primary key, flight_id int, trip_name text, end_date text, start_date text, start_location text, end_location text, trip_count int
    return render_template("trip.html",TRIP_DATA=trip_info,FLIGHT_DATA=flight_info,PLACES_DATA=places_info,TRIP_START=trip_start_date,TRIP_END=trip_end_date,FLIGHT_START=flight_start_date,FLIGHT_END=flight_end_date,WEATHER=weather_data,WEATHER_STATUS=status_weather,HOTEL_DATA=hotel)


if __name__ == "__main__":
    app.debug = True
    app.run()