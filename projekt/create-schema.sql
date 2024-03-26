
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
DROP TRIGGER IF EXISTS new_cookie;

PRAGMA foreign_keys = ON;

CREATE TABLE warehouses (
    ingredient TEXT,
    amount INT NOT NULL DEFAULT (0),
    unit TEXT,
    last_delivery_time DATETIME,
    last_delivery_amount INT,
    PRIMARY KEY (ingredient)
);

CREATE TABLE recipes (
    product_name TEXT,
    PRIMARY KEY (product_name)
);

CREATE TABLE recipe_quantities (
    product_name TEXT,
    ingredient TEXT,
    amount INT NOT NULL CHECK (amount > 0),
    PRIMARY KEY (product_name, ingredient)
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
    successfully_delivered INT NOT NULL DEFAULT (0),
    customer_name TEXT,
    product_name TEXT,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_name) REFERENCES customers(customer_name),
    FOREIGN KEY (product_name) REFERENCES recipes(product_name)
);

CREATE TABLE pallets (
    pallet_nbr INT AUTO_INCREMENT,
    production_date DATETIME,
    blocked INT NOT NULL DEFAULT (0),
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

CREATE TRIGGER new_cookie
    AFTER INSERT
    ON recipe_quantities
    WHEN NEW.product_name NOT IN recipes
BEGIN
    INSERT
    INTO recipes(product_name)
    VALUES (NEW.product_name);
END;

CREATE TRIGGER new_pallet
    BEFORE INSERT
    ON pallets
BEGIN
    UPDATE warehouses
    SET amount = amount - 54 * (
        SELECT amount
        FROM recipe_quantities
        WHERE product_name = NEW.product_name
            AND ingredient = warehouses.ingredient
    )
    WHERE ingredient IN (
        SELECT ingredient
        FROM recipe_quantities
        WHERE product_name = NEW.product_name
    );
END;
