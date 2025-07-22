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
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'completed', 'failed')),
    provider VARCHAR(20) NOT NULL CHECK (provider IN ('provider1', 'provider2')),
    provider_id UUID NOT NULL,
    provider_details VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

