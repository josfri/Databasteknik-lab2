
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
    PRIMARY KEY (performanceId),
    FOREIGN KEY (imdbKey) REFERENCES movies(imdbKey)
    FOREIGN KEY (theater) REFERENCES theaters(theater)
);


CREATE TABLE tickets (
    ticketId TEXT DEFAULT (lower(hex(randomblob(16)))),
    username TEXT,
    performanceId TEXT,
    PRIMARY KEY (ticketId),
    FOREIGN KEY (username) REFERENCES customers(username),
    FOREIGN KEY (performanceId) REFERENCES performances(performanceId)
);

DROP TRIGGER IF EXISTS tickets_left;
CREATE TRIGGER tickets_left
BEFORE INSERT ON tickets
WHEN
  (
  SELECT coalesce(count(ticketId), 0) AS sold_tickets
            FROM performances
            LEFT OUTER JOIN tickets USING (performanceId)
            JOIN theaters USING (theater)
            GROUP BY performanceId
            HAVING sold_tickets < capacity AND performanceId = NEW.performanceId
)
BEGIN
  SELECT RAISE (ROLLBACK, "No tickets left");
END;