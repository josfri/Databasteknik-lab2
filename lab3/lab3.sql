
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
    imdbKey TEXT,
    run_time INT,
    PRIMARY KEY (imdbKey)
);

CREATE TABLE customers (
    username TEXT,
    fullName TEXT,
    pwd TEXT,
    PRIMARY KEY (username)
);

CREATE TABLE theaters (
    theater TEXT,
    capacity INT,
    PRIMARY KEY (theater)
);

CREATE TABLE performances (
    performanceId TEXT DEFAULT (lower(hex(randomblob(16)))),
    imdbKey TEXT,
    theater TEXT,
    date DATE,
    time TIME,
    remainingSeats INT,
    PRIMARY KEY (performanceId),
    FOREIGN KEY (imdbKey) REFERENCES movies(imdbKey)
    FOREIGN KEY (theater) REFERENCES theaters(theater)
);


CREATE TABLE tickets (
    ticketId TEXT DEFAULT (lower(hex(randomblob(16)))) NOT NULL,
    username TEXT,
    performanceId TEXT,
    PRIMARY KEY (ticketId),
    FOREIGN KEY (username) REFERENCES customers(username),
    FOREIGN KEY (performanceId) REFERENCES performances(performanceId)
);

CREATE TRIGGER check_seats 
BEFORE INSERT ON tickets 
WHEN((SELECT remainingSeats FROM performances WHERE performanceId = new.performanceId) IS 0)
BEGIN
    SELECT RAISE(ABORT, 'No available seats!');
END;

CREATE TRIGGER decrement_seats AFTER INSERT ON tickets
BEGIN
    UPDATE performances
    SET remainingSeats = remainingSeats - 1
    WHERE performanceId = new.performanceId;
END;

CREATE TRIGGER increment_seats AFTER DELETE ON tickets
BEGIN
    UPDATE performances
    SET remainingSeats = remainingSeats + 1
    WHERE   performanceId = old.performanceId;
END;