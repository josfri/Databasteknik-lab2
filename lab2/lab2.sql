
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
    performance_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    theater_name TEXT,
    start_time TIME,
    date DATE,
    imdb TEXT,
    PRIMARY KEY (performance_id),
    FOREIGN KEY (imdb) REFERENCES movies(imdb)
    FOREIGN KEY (theater_name) REFERENCES theaters(theater_name)
);

CREATE TABLE tickets (
    ticket_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    username TEXT,
    performance_id TEXT,
    PRIMARY KEY (ticket_id),
    FOREIGN KEY (username) REFERENCES customers(username)
    FOREIGN KEY (performance_id) REFERENCES performances(performance_id)
);

-- Insert data into the tables.
INSERT INTO movies (title, year, imdb, run_time) VALUES
('Inception', 2010, 'tt1375666', 148),
('The Godfather', 1972, 'tt0068646', 175),
('Interstellar', 2014, 'tt0816692', 169),
('The Dark Knight', 2008, 'tt0468569', 152),
('Pulp Fiction', 1994, 'tt0110912', 154),
('Forrest Gump', 1994, 'tt0109830', 142),
('The Matrix', 1999, 'tt0133093', 136);

INSERT INTO theaters (theater_name, capacity) VALUES
('Grand Stockholm', 200),
('Sergel', 300),
('Rigoletto', 150);

INSERT INTO performances (theater_name, start_time, date, imdb) VALUES
('Grand Stockholm', '19:30', '2023-04-10', 'tt1375666'),
('Sergel', '20:00', '2023-04-11', 'tt0068646'),
('Rigoletto', '18:00', '2023-04-12', 'tt0816692'),
('Grand Stockholm', '19:00', '2023-04-13', 'tt0468569'),
('Rigoletto', '21:00', '2023-04-14', 'tt0110912'),
('Rigoletto', '16:00', '2023-04-15', 'tt0109830'),
('Grand Stockholm', '14:00', '2023-04-16', 'tt0133093'),
('Grand Stockholm', '15:00', '2023-04-17', 'tt1375666'),
('Sergel', '17:00', '2023-04-17', 'tt0068646'),
('Rigoletto', '19:00', '2023-04-17', 'tt0816692'),
('Grand Stockholm', '21:00', '2023-04-17', 'tt0468569'),
('Sergel', '23:00', '2023-04-17', 'tt0110912'),
('Grand Stockholm', '15:00', '2023-04-18', 'tt0109830'),
('Sergel', '17:00', '2023-04-18', 'tt0133093'),
('Rigoletto', '19:00', '2023-04-18', 'tt1375666'),
('Grand Stockholm', '21:00', '2023-04-18', 'tt0068646'),
('Sergel', '23:00', '2023-04-18', 'tt0816692'),
('Grand Stockholm', '15:00', '2023-04-19', 'tt0468569'),
('Sergel', '17:00', '2023-04-19', 'tt0110912'),
('Rigoletto', '19:00', '2023-04-19', 'tt0109830'),
('Grand Stockholm', '21:00', '2023-04-19', 'tt0133093'),
('Sergel', '23:00', '2023-04-19', 'tt1375666'),
('Grand Stockholm', '15:00', '2023-04-20', 'tt0068646'),
('Sergel', '17:00', '2023-04-20', 'tt0816692'),
('Rigoletto', '19:00', '2023-04-20', 'tt0468569'),
('Grand Stockholm', '21:00', '2023-04-20', 'tt0110912'),
('Sergel', '23:00', '2023-04-20', 'tt0109830');


INSERT INTO customers (username, full_name, password) VALUES
('Fabian', 'Fabian Rosen', 'qwerty56789'),
('josfri', 'Josefine Frid', 'password5'),
('Fremja', 'Fremja Ekre', 'qwertyuio9'),
('leoDicap', 'Leonardo DiCaprio', 'oscars2023'),
('beyKnow', 'Beyonce Knowles', 'lemonade'),
('tomCruise', 'Tom Cruise', 'topGun88'),
('tSwift', 'Taylor Swift', 'folklore'),
('rdjIron', 'Robert Downey Jr.', 'ironman3'),
('scarJo', 'Scarlett Johansson', 'blackwidow'),
('chrEvans', 'Chris Evans', 'capAmerica'),
('emmaStone', 'Emma Stone', 'lalaland'),
('johnnyDepp', 'Johnny Depp', 'pirateLife'),
('jenAni', 'Jennifer Aniston', 'friends4eva');


INSERT INTO tickets (username, performance_id) VALUES
('leoDicap', (SELECT performance_id FROM performances LIMIT 1)),
('beyKnow', (SELECT performance_id FROM performances LIMIT 1)),
('tomCruise', (SELECT performance_id FROM performances LIMIT 1)),
('tSwift', (SELECT performance_id FROM performances LIMIT 2 OFFSET 1)),
('rdjIron', (SELECT performance_id FROM performances LIMIT 2 OFFSET 1)),
('scarJo', (SELECT performance_id FROM performances LIMIT 2 OFFSET 1)),
('chrEvans', (SELECT performance_id FROM performances LIMIT 2 OFFSET 1)),
('emmaStone', (SELECT performance_id FROM performances LIMIT 3 OFFSET 2)),
('johnnyDepp', (SELECT performance_id FROM performances LIMIT 3 OFFSET 2)),
('jenAni', (SELECT performance_id FROM performances LIMIT 3 OFFSET 2)),
('leoDicap', (SELECT performance_id FROM performances LIMIT 3 OFFSET 2));

