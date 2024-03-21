
-- Frågan är om det ska vara decimaler eller inte i siffrorna, dvs om det ska vara INT eller DECIMAL
CREATE TABLE Warehouse (
    ingredient TEXT,
    amount DECIMAL NOT NULL,
    unit TEXT,
    last_delivery_time TIME,
    last_delivery_amount DECIMAL NOT NULL,
    PRIMARY KEY (ingredient)
);

CREATE TABLE Recipe (
    product_name TEXT,
    PRIMARY KEY (product_name)
);

CREATE TABLE Recipe_quantity (
    product_name TEXT,
    ingredient TEXT,
    amount DECIMAL NOT NULL,
    FOREIGN KEY (product_name) REFERENCES Recipe(product_name),
    FOREIGN KEY (ingredient) REFERENCES Warehouse(ingredient)
);

CREATE TABLE Customer (
    customer_name TEXT,
    address TEXT,
    PRIMARY KEY (customer_name)
);

CREATE TABLE Order (
    order_id INT AUTO_INCREMENT,
    delivery_day DATE,
    delivery_time TIME,
    successfully_delivered INT NOT NULL,
    customer_name TEXT,
    product_name TEXT,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_name) REFERENCES Customer(customer_name),
    FOREIGN KEY (product_name) REFERENCES Recipe(product_name)
);

CREATE TABLE Pallet (
    pallet_nbr INT AUTO_INCREMENT,
    production_date DATE NOT NULL,
    production_time TIME NOT NULL,
    blocked INT NOT NULL,
    product_name TEXT,
    order_id INT,
    PRIMARY KEY (pallet_nbr),
    FOREIGN KEY (product_name) REFERENCES Recipe(product_name),
    FOREIGN KEY (order_id) REFERENCES Order(order_id)
);

CREATE TABLE Order_item (
    order_id INT,
    pallet_nbr INT,
    nbr_pallets INT,
    FOREIGN KEY (order_id) REFERENCES Order(order_id),
    FOREIGN KEY (pallet_nbr) REFERENCES Pallet(pallet_nbr)
);

