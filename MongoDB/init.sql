-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS UserDatabase;

-- Switch to the database
USE UserDatabase;

-- Create the 'users' table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
