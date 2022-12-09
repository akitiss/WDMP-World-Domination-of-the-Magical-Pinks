import sqlite3

DB_FILE = "test.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)
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
    if(result == None):
        return None
    else:
        return result[0]

def register_new_user(username, password): # if username and password combination already exists, return False, else return ID
    c = db.cursor()
    c.execute("select exists(select 1 from user where username=? and password=?)", (username, password,)) # returns 1 if if already exists
    if (c.fetchone()[0] == 1):
        return False
    c.execute("SELECT MAX(u_id) FROM user")
    max_id = c.fetchone()
    if (len(max_id) > 0):
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
    if(u_id != None):
        return u_id[0]
    else:
        print("RETURNED NONE")
        return None