-- Create database
CREATE DATABASE provider2;

-- Connect to the database
\c provider2;

-- Enable the pgcrypto extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE transaction (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(20) NOT NULL CHECK (status IN ('paid', 'failed', 'voided')),
    original_amount INT NOT NULL CHECK (original_amount >= 0),
    amount INT NOT NULL CHECK (amount >= 0),
    currency VARCHAR(3) NOT NULL CHECK (currency IN ('USD', 'EUR', 'BRL')),
    statement_descriptor TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE carddetails(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID REFERENCES transaction(id),
    number VARCHAR(16) NOT NULL,
    holder VARCHAR(100) NOT NULL,
    cvv VARCHAR(5) NOT NULL,
    expiration VARCHAR(5) NOT NULL,
    installment_number INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
