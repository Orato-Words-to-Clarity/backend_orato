-- File: migrations/sql/001_create_users_table.sql
-- Migration: Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

-- Indexes for faster querying
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_users_email ON users (email);
