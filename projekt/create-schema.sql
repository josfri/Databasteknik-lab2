
-- cd /Users/josefinefrid/Desktop/Databasteknik/lab2/Databasteknik-lab2/projekt/
-- sqlite3 projekt.sqlite < create-schema.sql

-- Disable foreign key checks, so the tables can be dropped in arbitrary order.
PRAGMA foreign_keys = OFF;

-- Delete the tables if they exist.
DROP TABLE IF EXISTS warehouses;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS recipe_quantities;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS pallets;
DROP TABLE IF EXISTS order_items;

PRAGMA foreign_keys = ON;

-- Frågan är om det ska vara decimaler eller inte i siffrorna, dvs om det ska vara INT eller DECIMAL
CREATE TABLE warehouses (
    ingredient TEXT,
    amount DECIMAL NOT NULL DEFAULT (0),
    unit TEXT,
    last_delivery_time TIME,
    last_delivery_amount DECIMAL NOT NULL,
    PRIMARY KEY (ingredient)
);

CREATE TABLE recipes (
    product_name TEXT,
    PRIMARY KEY (product_name)
);

CREATE TABLE recipe_quantities (
    product_name TEXT,
    ingredient TEXT,
    amount DECIMAL NOT NULL,
    FOREIGN KEY (product_name) REFERENCES recipes(product_name),
    FOREIGN KEY (ingredient) REFERENCES warehouses(ingredient)
);

CREATE TABLE customers (
    customer_name TEXT,
    address TEXT,
    PRIMARY KEY (customer_name)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT,
    delivery_day DATE,
    delivery_time TIME,
    successfully_delivered INT NOT NULL,
    customer_name TEXT,
    product_name TEXT,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_name) REFERENCES customers(customer_name),
    FOREIGN KEY (product_name) REFERENCES recipes(product_name)
);

CREATE TABLE pallets (
    pallet_nbr INT AUTO_INCREMENT,
    production_date DATE NOT NULL,
    production_time TIME NOT NULL,
    blocked INT NOT NULL,
    product_name TEXT,
    order_id INT,
    PRIMARY KEY (pallet_nbr),
    FOREIGN KEY (product_name) REFERENCES recipes(product_name),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE order_items (
    order_id INT,
    pallet_nbr INT,
    nbr_pallets INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (pallet_nbr) REFERENCES pallets(pallet_nbr)
);

