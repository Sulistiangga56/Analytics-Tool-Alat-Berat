--Tabel master unit alat berat
CREATE TABLE unit_master (
    unit_id SERIAL PRIMARY KEY,
    unit_name VARCHAR(20) NOT NULL,
    unit_code VARCHAR(50) NOT NULL UNIQUE,
    unit_type VARCHAR(50) NOT NULL,
    manufacturer VARCHAR(50) NOT NULL,
    year_manufactured INT
);

--Tabel log harian unit
CREATE TABLE equipment_logs (
    log_id SERIAL PRIMARY KEY,
    unit_id INT REFERENCES unit_master(unit_id),
    log_date DATE NOT NULL,
    hours_operated DECIMAL(5, 2),
    fuel_used DECIMAL(5, 2),
    breakdown BOOLEAN DEFAULT FALSE,
    remarks TEXT
);