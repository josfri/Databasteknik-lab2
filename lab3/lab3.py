from bottle import get, post, run, response, request
from urllib.parse import unquote
import sqlite3

# Set-up
PORT = 7007
# sqlite3 lab3.sqlite < /Users/josefinefrid/Desktop/Databasteknik/lab3/lab3.sql
db = sqlite3.connect("../lab3.sqlite")
db.execute("PRAGMA foreign_keys = ON")

#kryptering: 
def hash(msg):
    import hashlib
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

@get('/ping')
def ping():
    return 'pong'

#empties the database, and enters the following theaters:
#"Kino", 10 seats
#"Regal", 16 seats
#"Skandia", 100 seats
@post('/reset')
def reset():
    c = db.cursor()
    c.executescript(
        """
        PRAGMA foreign_keys = OFF;
        DELETE FROM theaters;
        DELETE FROM performances;
        DELETE FROM movies;
        DELETE FROM tickets;
        DELETE FROM customers;
        PRAGMA foreign_keys = ON;

        INSERT
        INTO    theaters(theater, capacity)
        VALUES  ('Kino', 10),
                ('Regal', 16),
                ('Skandia', 100)
        """
    )
    db.commit()

@post('/users')
def insert_user(): 
    newuser = request.json; 
    #kolla att allt är med i nya användaren: annars error. 
    if not newuser or 'username' not in newuser or 'fullName' not in newuser or 'pwd' not in newuser:
        response.status = 400
        return ''
    
    #kolla om användaren redan finns när vi lägger in, tog christians tudentkod och ändrar: 
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO   customers(username, fullName, pwd)
            VALUES (?,?,?)
            RETURNING  username
            """,
            [newuser['username'], newuser['fullName'], hash(newuser['pwd'])]
        )
        found = c.fetchone()
        if not found:
            response.status = 400
            return "Illegal..."
        else:
            db.commit()
            response.status = 201
            username, = found
            return f"http://localhost:{PORT}/{username}"
    except sqlite3.IntegrityError:
        response.status = 409
        return "User id already in use"





run(host='localhost', port=PORT)
