-- Create database
CREATE DATABASE gateway;

-- Connect to the database
\c gateway;

-- Enable the pgcrypto extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    amount INT NOT NULL CHECK (amount >= 0),
    currency VARCHAR(3) NOT NULL CHECK (currency IN ('USD', 'EUR', 'BRL')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'completed', 'failed', 'cancelled')),
    provider VARCHAR(20) CHECK (provider IN ('provider1', 'provider2')),
    provider_id UUID NOT NULL,
    provider_details VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


/*
Create a test database for the gateway API
This database is used for running tests without affecting the production data.
Table will be created during the test setup.
*/
CREATE DATABASE gateway_test;
