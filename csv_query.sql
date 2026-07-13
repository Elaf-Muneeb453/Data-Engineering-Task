CREATE TABLE sensor_data1 (
    site_code VARCHAR(50),
    Timestamp TIMESTAMP,
    source VARCHAR(100),
    solar_output_current FLOAT,
    total_load_current FLOAT,
    battery_total_current FLOAT,
    total_voltage FLOAT
);


SELECT *
FROM sensor_data1
LIMIT 10;