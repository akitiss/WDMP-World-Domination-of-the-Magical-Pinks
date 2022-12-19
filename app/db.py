import sqlite3

DB_FILE = "test.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor() # Create the three tables if they dont exist yet
c.executescript(""" create TABLE if NOT EXISTS user(u_id int primary key, username varchar(20), password varchar(30));
    create TABLE if NOT EXISTS savedtrips(u_id int, trip_id int, PRIMARY KEY (u_id, trip_id));
    create TABLE if NOt EXISTS tripinfo(trip_id int primary key, flight_id int, trip_name text, hotel int, end_date text, start_date text, start_location text, end_location text, trip_count int);
    create TABLE if NOT EXISTS trip_places(trip_id int, place_id text, PRIMARY KEY (trip_id, place_id));
    create TABLE if NOT EXISTS flight(flight_id int primary key, start_location text, end_location text, start_time text, end_time text, price text, company text, count text);
    create TABLE if NOT EXISTS places(place_id int, name text, url text)
""")
c.close()

def get_username(id):
    c = db.cursor()
    c.execute("select username FROM user WHERE u_id = ?", (id,))
    result = c.fetchone()
    c.close()
    if(result == None):
        return None
    else:
        return result[0]

def register_new_user(username, password): # if username and password combination already exists, return False, else return ID
    c = db.cursor()
    c.execute("select exists(select 1 from user where username=? and password=?)", (username, password,)) # returns 1 if if already exists
    if (c.fetchone()[0] == 1):
        return -1
    c.execute("SELECT MAX(u_id) FROM user")
    max_id = c.fetchone()
    if (max_id[0] != None):
        new_id = max_id[0] + 1
    else:
        new_id = 0
    c.execute("insert into user values(? ,?, ?)", (new_id, username, password,))
    db.commit()
    c.close()
    return new_id

def account_match(username, password): # if it matches, return u_id, else return None
    c = db.cursor()
    c.execute('select u_id from user where (username = ? AND password = ?)', (str(username), str(password),))
    u_id = c.fetchone()
    c.close()
    if(u_id != None):
        return u_id[0]
    else:
        return None

def add_saved_trip(user_ID, trip_name, hotel, end_date, start_date, start_location, end_location, trip_count, price, company): # This adds to both: USE THIS
    # add trip info to tripinfo table.
    trip_ID = add_trip_info(trip_name, hotel, end_date, start_date, start_location, end_location, trip_count, price, company)
    c = db.cursor()
    c.execute("insert into savedtrips values(?, ?)", (user_ID, trip_ID))
    db.commit()
    c.close()
    return trip_ID

def add_trip_info(trip_name, hotel, end_date, start_date, start_location, end_location, trip_count, price, company): # USE THE ABOVE METHOD TO ADD ALL
    c = db.cursor()
    c.execute("SELECT MAX(trip_id) FROM tripinfo")
    max_id = c.fetchone()
    if (max_id[0] != None):
        new_id = max_id[0] + 1
    else:
        new_id = 0
    flight_id = add_flight_info(start_location, end_location, start_date, end_date, price, company, trip_count)
    c.execute("insert into tripinfo values(?, ?, ?, ?, ?, ?, ?, ?, ?)", (new_id, flight_id, str(trip_name), hotel, str(end_date), str(start_date), str(start_location), str(end_location), str(trip_count)))
    db.commit()
    c.close()
    return new_id

def add_flight_info(start_location, end_location, start_time, end_time, price, company, count): # DONT CALL THIS USE add_saved_trip instead
    c = db.cursor()
    c.execute("SELECT MAX(flight_id) FROM flight")
    max_id = c.fetchone()
    if (max_id[0] != None):
        new_id = max_id[0] + 1
    else:
        new_id = 0
    c.execute("insert into flight values(?, ?, ?, ?, ?, ?, ?, ?)", (new_id, start_location, end_location, start_time, end_time, price, company, count))
    db.commit()
    c.close()
    return new_id

def add_place(trip_id, place_id):
    c = db.cursor()
    c.execute("select trip_id from trip_places where (trip_id = ? AND place_id = ?)", (trip_id, place_id))
    check = c.fetchone() 
    if(check != None):
        c.close()
        return False
    c.execute("insert into trip_places values(?, ?)", (trip_id, place_id))
    db.commit()
    c.close()
    return True

def get_savedtrips(ID): # ID is a u_id. Fetches a list of all trip_ids that a user has in their saved trips.
    c = db.cursor()
    c.execute("select trip_id from savedtrips where (u_id = ?)", (ID,))
    data = c.fetchall()
    c.close()
    if data == None : 
        return []
    trips = [id[0] for id in data]
    return trips

def get_trip_info(ID): # ID is a trip_id
    c = db.cursor()
    c.execute("select * from tripinfo where (trip_id = ?)", (ID,))
    data = c.fetchall()
    c.close()
    if(data == []):
        return None
    #print(data)
    return data[0] # tuple of items: (trip_id, flight_id, trip_name, hotel, end_date, start_date, start_location, end_location, trip_count)

def get_flight_info(ID): # ID is a flight_id.
    c = db.cursor()
    c.execute("select * from flight where (flight_id = ?)", (ID,))
    data = c.fetchall()
    c.close()
    if(data == []):
        return None
    #print(data)
    return data[0] # tuple of items: (flight_id, start_location, end_location, start_time, end_time, price, company, count)

def get_all_places_id(ID): # ID is a trip_id. returns a list of all place_ids, or None if none
    c = db.cursor()
    c.execute("select place_id from trip_places where (trip_id = ?)", (ID,))
    data = c.fetchall()
    if data == None : 
        return None
    places = [id[0] for id in data]
    c.close()
    return places

def get_place_info(ID): # ID is a place_id
    c = db.cursor()
    c.execute("select * from places where (place_id = ?)", (ID,))
    data = c.fetchall()
    if data == None : 
        return None
    c.close()
    return data

def make_date(date):
    final = []
    splitted = date.split("T")
    time_splitted = splitted[1].split(":")
    zone = " AM"
    string = ""
    if (int(time_splitted[0]) == 0):
        string += ("12:" + time_splitted[1] + zone)
    elif (int(time_splitted[0]) == 12):
        string += ("12:" + time_splitted[1] + " PM")
    elif (int(time_splitted[0]) > 12):
        string += (str(int(time_splitted[0])-12) + ":" + time_splitted[1] + " PM")
    else:
        string += ("" + time_splitted[0][1:] + ":" + time_splitted[1] + zone)
    final.append(string)
    final.append(splitted[0])
    return final

#print(add_flight_info(1000))
#print(get_places(-1))
#print(get_flight_info(1))
#print(get_savedtrips(0))
#print(add_place(-1, -2))