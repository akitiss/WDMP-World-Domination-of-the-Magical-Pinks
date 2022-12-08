import sqlite3

DB_FILE = "test.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor() # Create the three tables if they dont exist yet
c.executescript(""" 
    create TABLE if NOT EXISTS user(u_id int primary key, username varchar(20), password varchar(30));
    create TABLE if NOT EXISTS savedtrips(u_id int, trip_id int, PRIMARY KEY (u_id, trip_id));
    create TABLE if NOt EXISTS tripinfo(trip_id primary key, country text, city text, hotel text);
""")
c.close()

def get_username(id):
    c = db.cursor()
    c.execute("select username FROM user WHERE u_id = ?", (id,))
    result = c.fetchone()
    if(len(result) == 0):
        return None
    else:
        return result[0]

def register(username, password):
    c = db.cursor()
    new_id = c.execute("SELECT * FROM TABLE WHERE u_id = (SELECT MAX(u_id) FROM user )") + 1
    c.execute("insert into user values(? ,?, ?)", (new_id, username, password,))
    c.close()