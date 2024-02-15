from bottle import get, post, run, response, request
from urllib.parse import unquote
import sqlite3

# Set-up
PORT = 7007
# sqlite3 lab3.sqlite < lab3.sql
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
            return f"/users/{username}"
    except sqlite3.IntegrityError:
        response.status = 409
        return "User id already in use"

@post('/movies')
def insert_movie(): 
    newmovie = request.json; 
#behövs den här? 
    if not newmovie or 'imdbKey' not in newmovie or 'title' not in newmovie or 'year' not in newmovie:
        response.status = 400
        return ' '
      
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO   movies(imdbKey, title, year)
            VALUES (?,?,?)
            RETURNING imdbKey
            """,
            [newmovie['imdbKey'], newmovie['title'], newmovie['year']]
        )
        found = c.fetchone()
        if not found:
            response.status = 400
            return "Illegal..."
        else:
            db.commit()
            response.status = 201
            imdbKey, = found
            return f"/movies/{imdbKey}"
    except sqlite3.IntegrityError:
        response.status = 409
        return "Movie is already in use"
    
@post('/performances')
def insert_performances(): 
    newperformance = request.json; 
#behövs den här? 
    if not newperformance or 'imdbKey' not in newperformance or 'date' not in newperformance or 'time' not in newperformance or 'theater' not in newperformance:
        response.status = 400
        return ' '
      
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO   performances(imdbKey, theater, date, time)
            VALUES (?,?,?,?)
            RETURNING  performanceId
            """,
            [ newperformance['imdbKey'], newperformance['theater'], newperformance['date'], newperformance['time']]
        )
        print("hej")
        found = c.fetchone()
        if not found:
            response.status = 400
            return "Illegal..."
        else:
            db.commit()
            response.status = 201
            performanceId, = found
            return f"/performances/{performanceId}"
    except sqlite3.IntegrityError:
        response.status = 409
        return "Performance is already in use"

@get('/movies')
def get_movies():
    c = db.cursor()
    c.execute(
        """
        SELECT   imdbKey, title, year
        FROM     movies
        """
    )
    response.status = 200
    found = [{"imdbKey": imdbKey,
              "title": title,
              "year": year } for imdbKey, title, year in c]
    return {"data": found}

@get('/movies/<imdb_key>')
def get_movies_imdb(imdb_key):
    c = db.cursor()
    
    c.execute(
        """
        SELECT   imdbKey, title, year
        FROM     movies
        WHERE    imdbKey = ?
        """,
        [imdb_key]
    )
    found = [{"imdbKey": imdbKey,
                "title": title,
                "year": year } for imdbKey, title, year in c]
    if not found:
        response.status = 400
        return ""
    if len(found) == 0:
        response.status = 404
        return ""
    return {"data": found}
    
    

@get('/performances')
def getPerformances():
    c = db.cursor()
    c.execute(
        """
        SELECT performanceId, imdbKey, theater, date, time, year, title
        FROM performances JOIN movies USING (imdbKey)
        """
    )
    response.status = 200
    found = [{"performaceId": performanceId, 
             "date": date,
            "startTime": time,
            "title": title,
            "year": year,
            "theater": theater,
              } for performanceId, imdbKey, theater, date, time, year, title in c]
    return {"data": found}

@post('/tickets')
def insert_ticket():
    newticket = request.json

    c = db.cursor()

    #Find customer?
    c.execute(
        """
        SELECT      username, pwd
        FROM        customers
        WHERE       username = ? AND pwd = ?
        """,
        [newticket['username'], hash(newticket['pwd'])]
    )
    
    found = c.fetchone()
    if not found:
        response.status = 401
        return "User not found"

    ##Find performance?
    c.execute(
    """
    SELECT      performanceId
    FROM        performances
    WHERE       performanceId = ?
    """,
    [newticket['performanceId']]
    )
    found = c.fetchone()
    if not found:
        response.status = 400
        return "Performance was not found"
    
    #fins number of sold ticket and the capacity:
    c.execute(
         """
         WITH soldtickets(performanceId, numberoftickets) AS (
         SELECT performanceId, count()
         FROM tickets 
         WHERE performanceId = ?
         )

         SELECT capacity - numberoftickets
         FROM theaters 
         JOIN performances USING (theater)
         JOIN soldtickets USING (performanceId)
        """,
        [newticket['performanceId']]
    )
    #checking if there are any left
    remaining_tickets, = c.fetchone()
    if remaining_tickets < 1:
                response.status = 400
                return 'Tickets sold out'
    else:
        c.execute(
            """
            INSERT
            INTO       tickets (username, performanceId)
            VALUES     (?, ?)
            RETURNING  ticketId
            """,
            [newticket['username'], newticket['performanceId']]
        )
        ticket_id, = c.fetchone()
        return f"/tickets/{ticket_id}"

run(host='localhost', port=PORT)
