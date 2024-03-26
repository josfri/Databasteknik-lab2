from bottle import get, post, run, response, request
from urllib.parse import quote, unquote
import sqlite3

# Set-up
PORT = 8888


db = sqlite3.connect("/Users/josefinefrid/Desktop/Databasteknik/lab2/Databasteknik-lab2/projekt/projekt.sqlite")
db.execute("PRAGMA foreign_keys = ON")

#---------- Reset database ----------
@post('/reset')
def reset():
    c = db.cursor()
    c.executescript(
        """
        PRAGMA foreign_keys = OFF;
        DELETE FROM warehouses;
        DELETE FROM recipes;
        DELETE FROM recipe_quantities;
        DELETE FROM customers;
        DELETE FROM orders;
        DELETE FROM pallets;
        DELETE FROM order_items;
        PRAGMA foreign_keys = ON;
        """
    )
    db.commit()
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
            INTO customers(customer_name, address)
            VALUES (?, ?)
        """, 
        [ new_customer['name'], new_customer['address']]
    )

    db.commit()
    response.status = 201

    return {
        'location' : f'/customers/' + quote(new_customer['name'])
    }

@get('/customers')
def get_customers(): 
    c = db.cursor()
    c.execute(
        """
        SELECT customer_name, address
        FROM customers
        """
    )
    found = [{ 
        "name": customer_name, 
        "address": address } for customer_name, address in c
    ]
    response.status = 200
    return {
        "data": found
    }


#----------Add and check ingredients----------------
@post('/ingredients')
def add_ingredient(): 

    new_ingredient = request.json  
    c = db.cursor()

    c.execute( 
        """
            INSERT 
            INTO warehouses(ingredient, unit)
            VALUES (?, ?)
        """, 
        [ new_ingredient['ingredient'], new_ingredient['unit']]
    )

    db.commit()
    response.status = 201

    return {
        'location' : f'/ingredients/' + quote(new_ingredient['ingredient'])
    }

@post('/ingredients/<ingredient>/deliveries')
def update_ingredient(ingredient): 
    new_delivery = request.json #hämta json objektet 
    c = db.cursor()
    c.execute( 
        """
            UPDATE warehouses 
            SET last_delivery_time = ?, 
                last_delivery_amount = ?,
                amount = amount + ?
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
        FROM warehouses 
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

#--------Add and check recipes/cookies-----------
@post('/cookies')
def add_cookies():
    new_cookie = request.json 
    c = db.cursor()
    for recipeline in new_cookie['recipe']:
        c.execute(
            """
            INSERT 
            INTO recipe_quantities(product_name, ingredient, amount)
            VALUES (?, ?, ?)
            """, 
            [new_cookie['name'], recipeline['ingredient'], recipeline['amount']]
        )
    response.status = 201 
    url_cookie_name = quote(new_cookie['name'])
    return{ 'location': f'/cookies/'+ url_cookie_name}

@get('/cookies')
def get_cookie_names(): 
    c = db.cursor()
    c.execute(
        """
        WITH unblocked_pallets AS (
            SELECT      product_name, count()
            FROM        recipes
            LEFT JOIN   pallets USING (product_name)
            WHERE       blocked = 0
            GROUP BY    product_name
        )
        SELECT      product_name, count() AS nbr_of_pallets
        FROM        recipes
        LEFT JOIN   unblocked_pallets USING (product_name)
        GROUP BY    product_name
        """
    )
    found = [{ "name": product_name, "pallets": nbr_of_pallets} for product_name, nbr_of_pallets  in c]
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
      FROM recipe_quantities
      WHERE product_name = ?
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
def post_pallet():

    new_pallet = request.json
    c = db.cursor()

    try:
        c.execute(
            """
            INSERT 
            INTO pallets (production_date, product_name)
            VALUES (DATETIME('now'), ?)
            RETURNING pallet_nbr
            """, [new_pallet['cookie']]
        )

        found = c.fetchone()
        response.status = 201

        return { 'location': f'/pallets/' + found[0]}

    except:
        response.status = 422
        return {'location': ''}
        
@get('/pallets')
def get_pallets(): 

    c = db.cursor()

    query = """
            SELECT pallet_nbr, product_name, production_date, blocked
            FROM pallets
            WHERE product_name = ?
            """
    
    params = ['product_name']

    if request.query.before:
        query += " AND production_date < ?"
        params.append(unquote(request.query.before))
    if request.query.after:
        query += " AND production_date > ?"
        params.append(unquote(request.query.after))

    c.execute(query,params)
    found = [{ 
        "id": pallet_nbr, 
        "cookie": product_name,
        "productionDate" : production_date,
        "blocked" : blocked
          } for pallet_nbr, product_name, production_date, blocked in c
    ]
    response.status = 200
    return {
        "data": found
    }
   

#---------- Blocking and unblocking ----------
@post('/cookies/<cookie_name>/block')
def post_cookies_block(cookie_name):
    
    c = db.cursor()

    query = """
            UPDATE pallets
            SET is_blocked = 1
            WHERE product_name = ?
            """
    
    params = ['product_name']

    if request.query.before:
        query += " AND production_date < ?"
        params.append(unquote(request.query.before))
    if request.query.after:
        query += " AND production_date > ?"
        params.append(unquote(request.query.after))

    c.execute(query,params)

    response.status = 205
    return ""

@post('/cookies/<cookie_name>/unblock')
def post_cookies_unblock(cookie_name):

    c = db.cursor()

    query = """
            UPDATE pallets
            SET is_blocked = 0
            WHERE product_name = ?
            """
    
    params = ['product_name']

    if request.query.before:
        query += " AND production_date < ?"
        params.append(unquote(request.query.before))
    if request.query.after:
        query += " AND production_date > ?"
        params.append(unquote(request.query.after))

    c.execute(query,params)

    response.status = 205
    return ""

# ---- Functions end here ------

run(host='localhost', port=PORT)
