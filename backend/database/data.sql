
-- Create the rabais table
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

-- Create the trotinette table
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

-- Create the reservations table
CREATE TABLE IF NOT EXISTS reservations (
    id_reservation INTEGER PRIMARY KEY,
    start_date DATETIME,
    end_date DATETIME,
    pick_up_location_id INTEGER,
    drop_off_location_id INTEGER,
    total_cost INTEGER,
    trotinette_id INTEGER,
    user_id INTEGER,
    options TEXT,
    reservation_hours INTEGER,
    FOREIGN KEY (trotinette_id) REFERENCES trotinette (id_trotinette),
    FOREIGN KEY (user_id) REFERENCES users (id_user)
);

-- Create the users table
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

-- Create the sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    id_session VARCHAR(32),
    email VARCHAR(25),
    name VARCHAR(10),
    user_type TEXT DEFAULT 'user' CHECK(user_type IN ('user', 'admin'))
);

-- Create the addresses table
CREATE TABLE IF NOT EXISTS addresses (
    id_address INTEGER PRIMARY KEY,
    address TEXT,
    country VARCHAR(20),
    city VARCHAR(20),
    province TEXT,
    postal_code VARCHAR(7)
);

-- Create the locations table
CREATE TABLE IF NOT EXISTS locations (
    id_location INTEGER PRIMARY KEY,
    name VARCHAR(20),
    address_id INTEGER,
    FOREIGN KEY (address_id) REFERENCES addresses (id_address)
);

-- Create the pictures table
CREATE TABLE IF NOT EXISTS pictures (
    id_pictures VARCHAR(32) PRIMARY KEY,
    data BLOB
);

-- Create the support_requests table
CREATE TABLE IF NOT EXISTS support_requests (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    support_option VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users (id_user)
);

-- Create the credit_cards table
CREATE TABLE IF NOT EXISTS credit_cards (
    id INTEGER PRIMARY KEY,
    card_number VARCHAR(16),
    expiry_date VARCHAR(5),
    cvv VARCHAR(3),
    card_holder_name VARCHAR(100),
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id_user)
);

-- Create the payment_history table
CREATE TABLE IF NOT EXISTS payment_history (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount INTEGER,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    card_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id_user),
    FOREIGN KEY (card_id) REFERENCES credit_cards (id)
);

-- -- Insert sample values
-- INSERT INTO credit_cards (card_number, expiry_date, cvv, card_holder_name, user_id)
-- VALUES 
-- -- ('1234567890123456', '12/25', '123', 'John Doe', 1),
-- -- ('9876543210987654', '06/24', '456', 'Jane Smith', 2),
-- -- ('1111222233334444', '09/23', '789', 'Alice Johnson', 3),
-- -- ('4444444444444444', '01/24', '789', 'Alice test1', 4),
-- -- ('5555555555555555', '01/25', '789', 'Alice test2', 5);


