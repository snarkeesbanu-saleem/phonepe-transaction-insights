DROP TABLE IF EXISTS aggregated_transaction CASCADE;
DROP TABLE IF EXISTS aggregated_user CASCADE;
DROP TABLE IF EXISTS aggregated_insurance CASCADE;
DROP TABLE IF EXISTS map_transaction CASCADE;
DROP TABLE IF EXISTS map_user CASCADE;
DROP TABLE IF EXISTS map_insurance CASCADE;
DROP TABLE IF EXISTS top_transaction_state CASCADE;
DROP TABLE IF EXISTS top_transaction_district CASCADE;
DROP TABLE IF EXISTS top_transaction_pincode CASCADE;
DROP TABLE IF EXISTS top_user_state CASCADE;
DROP TABLE IF EXISTS top_insurance CASCADE;

CREATE TABLE aggregated_transaction (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    transaction_type VARCHAR(100),
    transaction_count BIGINT,
    transaction_amount DECIMAL(20,2)
);

CREATE TABLE aggregated_user (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    brand VARCHAR(100),
    count BIGINT,
    percentage DECIMAL(10,2)
);

CREATE TABLE aggregated_insurance (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    insurance_count BIGINT,
    insurance_amount DECIMAL(20,2)
);

CREATE TABLE map_transaction (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    district VARCHAR(100),
    transaction_count BIGINT,
    transaction_amount DECIMAL(20,2)
);

CREATE TABLE map_user (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    district VARCHAR(100),
    registered_users BIGINT,
    app_opens BIGINT
);

CREATE TABLE map_insurance (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100),
    year INT,
    quarter INT,
    district VARCHAR(100),
    insurance_count BIGINT,
    insurance_amount DECIMAL(20,2)
);

CREATE TABLE top_transaction_state (
    id SERIAL PRIMARY KEY,
    year INT,
    quarter INT,
    state VARCHAR(100),
    transaction_count BIGINT,
    transaction_amount DECIMAL(20,2)
);

CREATE TABLE top_transaction_district (
    id SERIAL PRIMARY KEY,
    year INT,
    quarter INT,
    state VARCHAR(100),
    district VARCHAR(100),
    transaction_count BIGINT,
    transaction_amount DECIMAL(20,2)
);

CREATE TABLE top_transaction_pincode (
    id SERIAL PRIMARY KEY,
    year INT,
    quarter INT,
    state VARCHAR(100),
    pincode VARCHAR(10),
    transaction_count BIGINT,
    transaction_amount DECIMAL(20,2)
);

CREATE TABLE top_user_state (
    id SERIAL PRIMARY KEY,
    year INT,
    quarter INT,
    state VARCHAR(100),
    registered_users BIGINT
);

CREATE TABLE top_insurance (
    id SERIAL PRIMARY KEY,
    year INT,
    quarter INT,
    state VARCHAR(100),
    insurance_count BIGINT,
    insurance_amount DECIMAL(20,2)
);

SELECT '✅ All 11 tables created successfully!' AS status;
