-- Database schema for octopus case study
-- This file defines the database structure for data stored in the data/ folder

-- Create database (PostgreSQL syntax, adjust for your database system)
-- CREATE DATABASE IF NOT EXISTS octopus_case_study;

-- Example table structure
-- Uncomment and modify based on your CSV data files

-- Example: Users or entities table
-- CREATE TABLE IF NOT EXISTS entities (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Example: Transactions or events table
-- CREATE TABLE IF NOT EXISTS transactions (
--     id SERIAL PRIMARY KEY,
--     entity_id INTEGER REFERENCES entities(id),
--     amount DECIMAL(10, 2),
--     transaction_date DATE,
--     description TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Example: Metadata or attributes table
-- CREATE TABLE IF NOT EXISTS metadata (
--     id SERIAL PRIMARY KEY,
--     entity_id INTEGER REFERENCES entities(id),
--     key VARCHAR(100),
--     value TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Add indexes for performance
-- CREATE INDEX IF NOT EXISTS idx_entity_name ON entities(name);
-- CREATE INDEX IF NOT EXISTS idx_transaction_entity ON transactions(entity_id);
-- CREATE INDEX IF NOT EXISTS idx_transaction_date ON transactions(transaction_date);
-- CREATE INDEX IF NOT EXISTS idx_metadata_entity ON metadata(entity_id);

-- Note: Update this schema based on the actual structure of your CSV files in the data/ folder
