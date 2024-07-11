-- Create users table if not exists
-- Define columns: id, email, name, country
-- Set id as primary key
-- Ensure email is unique
-- Set default country to US
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
