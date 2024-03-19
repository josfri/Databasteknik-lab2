from bottle import get, post, run, response, request
from urllib.parse import unquote
import sqlite3

# Set-up
PORT = 7007
# sqlite3 lab3.sqlite < lab3.sql
db = sqlite3.connect("/Users/josefinefrid/Desktop/Databasteknik/lab2/Databasteknik-lab2/lab3/lab3.sqlite")
db.execute("PRAGMA foreign_keys = ON")

#functions start here 



#Reset database

#Add and check customers

#----------Add and check ingredients- Fremjas kod----------------

@post('/ingredients')
def add_ingredient(): 
    new_ingredient = request.json #hämta json objektet 
    c = db.cursor()
    c.execute( 
        """
            INSERT 
            INTO Warehouse(ingredient, unit)
            VALUES (?, ?)
        """, 
        [ new_ingredient('ingredient'), new_ingredient('unit'),]
    )
  
    url_encoded_ingredient = quote(new_ingredient('ingredient'))
    response.status = 201
    return {
        'location' : f'/ingredients/' + url_encoded_ingredient 
    }

@post('/ingredients/<ingredient>/deliveries')
def update_ingredient(ingredient): 
    new_delivery = request.json #hämta json objektet 
    c = db.cursor()
    c.execute( 
        """
            UPDATE Warehouse 
            SET last_delivery_time = ?, 
                last_delivery_amount = ?,
                amount = amount + ?, 
            WHERE ingredient = ?
            RETURNING ingredient, amount, unit
        """, [new_delivery('deliveryTime'), new_delivery('quantity'), new_delivery('quantity'), ingredient]
    ) # här kan man göra en trigger istället i databsen som ändrar amount i warehpuse när vi lägger till en delivery. OBS vet ej om det funkar som det är nu!! 
  
    found = [{ 
        "ingredient": ingredient, 
        "quantity": amount, 
        "unit": unit} for ingredient, amount, unit in c
    ]
    response.status = 201
    return {
        "data": found
    }

@get('/ingredients')
def get_ingredients(): 
    c = db.cursor()
    c.execute(
        """
        SELECT ingredient, amount, unit
        FROM Warehouse 
        """
    )
    found = [{ 
        "ingredient": ingredient, 
        "quantity": amount, 
        "unit": unit} for ingredient, amount, unit in c
    ]
    response.status = 200
    return {
        "data": found
    }

#--------Add and check recipes/ookies-----------

#Add and check pallets

#Blocking and unblocking

#Cookies part 2



#functions end here 

run(host='localhost', port=PORT)
