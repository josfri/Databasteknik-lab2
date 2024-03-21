from bottle import get, post, run, response, request
from urllib.parse import quote, unquote
import sqlite3

# Set-up
PORT = 7007
# sqlite3 lab3.sqlite < lab3.sql
db = sqlite3.connect("/Users/josefinefrid/Desktop/Databasteknik/lab2/Databasteknik-lab2/lab3/lab3.sqlite")
db.execute("PRAGMA foreign_keys = ON")

#functions start here 



#---------- Reset database ----------

@post('/reset')
def reset():
    c = db.cursor()
    c.executescript(
        """
        PRAGMA foreign_keys = OFF;
        DELETE FROM Warehouse;
        DELETE FROM Recipe;
        DELETE FROM Recipe_quantity;
        DELETE FROM Customer;
        DELETE FROM Order;
        DELETE FROM Pallet;
        DELETE FROM Order_item;
        PRAGMA foreign_keys = ON;

        """
    )
    response.status = 205 
    return { 
        "location": '/'
    }



#---------- Add and check customers ----------
@post('/customers')
def add_customer(): 
    new_customer = request.json #hämta json objektet 
    c = db.cursor()
    c.execute( 
        """
            INSERT 
            INTO Customer(customer_name, address)
            VALUES (?, ?)
        """, 
        [ new_customer['customer_name'], new_customer['address']]
    )
  
    url_encoded_cname = new_customer['customer_name'])
    response.status = 201
    return {
        'location' : f'/ingredients/' + url_encoded_cname
    }

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
        [ new_ingredient['ingredient'], new_ingredient['unit']]
    )
  
    url_encoded_ingredient = quote(new_ingredient['ingredient'])
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
        """, [new_delivery['deliveryTime'], new_delivery['quantity'], new_delivery['quantity'], unquote(ingredient)]
    ) # här kan man göra en trigger istället i databsen som ändrar amount i warehpuse när vi lägger till en delivery. OBS vet ej om det funkar som det är nu!! 
  # och borde man unquotea ingredient i input-attributet??? 
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

#--------Add and check recipes/ookies- Fremjas kod-----------

@post('/cookies')
def add_cookies():
    new_cookie = request.json 
    c = db.cursor()
    for recipeline in new_cookie['recipe'] :
        c.execute(
            """
            INSERT 
            INTO Recipe_quantity(product_name, ingredient, amount)
            VALUES (?, ?, ?)
            """, [new_cookie['name'], recipeline['ingredient'], recipeline['amount']]
        )
    response.status = 201 
    url_cookie_name = quote(new_cookie['name'])
    return{ 'location': f'/cookies/'+ url_cookie_name}

@get('/cookies')
def get_cookie_names(): 
    c = db.cursor()
    c.execute(
        """
        SELECT product_name 
        FROM Recipe 
        """
    )
    found = [{ 
        "name": product_name} for product_name in c
    ]
    response.status = 200
    return {
        "data": found
    }

@get('/cookies/<cookie_name>/recipe')
def get_cookie_recipe(cookie_name):
  c = db.cursor()
  c.execute(
      """
      SELECT ingredient, amount, unit
      FROM Recipe_quantity 
      WHERW product_name = ?
      """, [unquote(cookie_name)]
  )
  found = [{'ingredient': ingredient, 'amount': amount, 'unit': unit} for ingredient, amount, unit in c]
  if not found:
      response.status = 404
  else:
      response.status = 200
  return { 'data': found }




#---------- Add and check pallets ----------

@post('/pallets')


#---------- Blocking and unblocking ----------

#---------- Cookies part 2 ----------



#functions end here 

run(host='localhost', port=PORT)
