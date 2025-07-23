-- Create database
CREATE DATABASE provider1;

-- Connect to the database
\c provider1;

-- Enable the pgcrypto extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE charge (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(20) NOT NULL CHECK (status IN ('authorized', 'refunded', 'failed')),
    original_amount INT NOT NULL CHECK (original_amount >= 0),
    current_amount INT NOT NULL CHECK (current_amount >= 0),
    currency VARCHAR(3) NOT NULL CHECK (currency IN ('USD', 'EUR', 'BRL')),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE paymentmethod(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    charge_id UUID REFERENCES charge(id),
    type VARCHAR(20) NOT NULL CHECK (type IN ('card')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE carddetails(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paymentmethod_id UUID REFERENCES paymentmethod(id),
    number VARCHAR(16) NOT NULL,
    holder_name VARCHAR(100) NOT NULL,
    cvv VARCHAR(4) NOT NULL,
    expiration_date VARCHAR(7) NOT NULL,
    installments INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/*
Create a test database for the provider1 API
This database is used for running tests without affecting the production data.
Table will be created during the test setup.
*/
CREATE DATABASE provider1_test;

