
-- Disable foreign key checks, so the tables can be dropped in arbitrary order.
PRAGMA foreign_keys = OFF;

-- Delete the tables if they exist.
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS performances;
DROP TABLE IF EXISTS tickets;

PRAGMA foreign_keys = ON;

-- Create the tables.
CREATE TABLE movies (
    title TEXT,
    year INT,
    imdb TEXT,
    run_time INT,
    PRIMARY KEY (imdb)
);

CREATE TABLE customers (
    username TEXT,
    full_name TEXT,
    password TEXT,
    PRIMARY KEY (username)
);

CREATE TABLE theaters (
    theater_name TEXT,
    capacity INT,
    PRIMARY KEY (theater_name)
);

CREATE TABLE performances (
    performance_id TEXT DEFAULT randomblob(16),
    theater_name TEXT,
    start_time TIME,
    date DATE,
    imdb TEXT,
    PRIMARY KEY (performance_id),
    FOREIGN KEY (imdb) REFERENCES movies(imdb)
    FOREIGN KEY (theater_name) REFERENCES theaters(theater_name)
);

CREATE TABLE tickets (
    ticket_id TEXT DEFAULT randomblob(16),
    username TEXT,
    performance_id TEXT,
    PRIMARY KEY (ticket_id),
    FOREIGN KEY (username) REFERENCES customers(username)
    FOREIGN KEY (performance_id) REFERENCES performances(performance_id)
);

-- Insert data into the tables.
INSERT
INTO    ... (...)
VALUES  (...);
...