import sqlite3

DB_FILE = "test.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor() # Create the three tables if they dont exist yet
c.executescript(""" 
    create TABLE if NOT EXISTS user(u_id int primary key, username varchar(20), password varchar(30));
    create TABLE if NOT EXISTS savedtrips(u_id int, trip_id int, PRIMARY KEY (u_id, trip_id));
    create TABLE if NOt EXISTS tripinfo(trip_id int primary key, trip_name text, country text, city text, hotel text);
    create TABLE if NOT EXISTS trip_places(trip_id int, place_id int, PRIMARY KEY (trip_id, place_id));
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

def add_saved_trip(user_ID, trip_name, country, city, hotel): # This adds to both: Use this one instead of the other
    # add trip info to tripinfo table.
    trip_ID = add_trip_info(trip_name, country, city, hotel)
    c = db.cursor()
    c.execute("insert into savedtrips values(?, ?)", (user_ID, trip_ID))
    db.commit()
    c.close()

def add_trip_info(trip_name, country, city, hotel):
    c = db.cursor()
    c.execute("SELECT MAX(trip_id) FROM tripinfo")
    max_id = c.fetchone()
    if (max_id[0] != None):
        new_id = max_id[0] + 1
    else:
        new_id = 0
    c.execute("insert into tripinfo values(?, ? , ? , ?)", (new_id, str(trip_name),str(country), str(city), str(hotel)))
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
    #print(check
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

def get_trip_info(ID): # ID is a trip_id. returns a tuple with all the data in a trip (id, name, country, city, hotel), or None if none
    c = db.cursor()
    c.execute("select * from tripinfo where (trip_id = ?)", (ID,))
    data = c.fetchall()
    c.close()
    if(data == []):
        return None
    #print(data)
    
    return data[0]

def get_places(ID): # ID is a trip_id. returns a list of all place_ids, or None if none
    c = db.cursor()
    c.execute("select place_id from trip_places where (trip_id = ?)", (ID,))
    data = c.fetchall()
    if data == None : 
        return None
    places = [id[0] for id in data]
    c.close()
    return places
print(get_places(-1))
#print(get_trip_info(-1))
#print(get_savedtrips(-45))
#print(add_place(-1, -2))