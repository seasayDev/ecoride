CREATE TABLE IF NOT EXISTS rabais (
    id_rabais INTEGER PRIMARY KEY,
    name VARCHAR(20),
    value INTEGER,
    code VARCHAR(10),
    start_date DATE,
    end_date DATE,
    image_id VARCHAR(32) DEFAULT NULL,
    active BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS trotinette (
    id_trotinette INTEGER PRIMARY KEY,
    name VARCHAR(20),
    category VARCHAR(20),
    price INTEGER,
    available BOOLEAN,
    location_id INTEGER,
    image_id VARCHAR(32) DEFAULT NULL,
    qte INTEGER DEFAULT 0,
    FOREIGN KEY (location_id) REFERENCES locations (id_location)
);

CREATE TABLE IF NOT EXISTS reservations (
    id_reservation INTEGER PRIMARY KEY,
    start_date DATETIME,
    end_date DATETIME,
    pick_up_address TEXT,
    drop_off_address TEXT,
    total_cost INTEGER,
    trotinette_id INTEGER,
    user_id INTEGER,
    options TEXT,
    FOREIGN KEY (trotinette_id) REFERENCES trotinette (id_trotinette),
    FOREIGN KEY (user_id) REFERENCES users (id_user)
);

CREATE TABLE IF NOT EXISTS users (
    id_user INTEGER PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    email VARCHAR(50),
    address_id INTEGER,
    date_of_birth DATE,
    phone TEXT,
    user_type TEXT DEFAULT 'user' CHECK(user_type IN ('user', 'admin')),
    salt VARCHAR(32),
    hash VARCHAR(128),
    FOREIGN KEY (address_id) REFERENCES addresses (id_address)
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    id_session VARCHAR(32),
    email VARCHAR(25),
    name VARCHAR(10),
    user_type TEXT DEFAULT 'user' CHECK(user_type IN ('user', 'admin'))
);

CREATE TABLE IF NOT EXISTS addresses (
    id_address INTEGER PRIMARY KEY,
    address TEXT,
    country VARCHAR(20),
    city VARCHAR(20),
    province TEXT,
    postal_code VARCHAR(7)
);

CREATE TABLE IF NOT EXISTS locations (
    id_location INTEGER PRIMARY KEY,
    name VARCHAR(20),
    address_id INTEGER,
    FOREIGN KEY (address_id) REFERENCES addresses (id_address)
);

CREATE TABLE IF NOT EXISTS pictures (
    id_pictures VARCHAR(32) PRIMARY KEY,
    data BLOB
);
