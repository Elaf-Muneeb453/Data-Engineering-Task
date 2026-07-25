CREATE TABLE sensor_data (
    site_code VARCHAR(50),
    time_stamp TIMESTAMP,
    source_tag VARCHAR(100),
    solar_output_current FLOAT,
    total_load_current FLOAT,
    battery_total_current FLOAT,
    total_voltage FLOAT
);

SELECT
    site_code,
    date_trunc('hour', time_stamp) AS hourly_window,
    CASE
        WHEN TRIM(source_tag) LIKE '%DG%' THEN 'DG'
        WHEN TRIM(source_tag) LIKE '%Solar%' THEN 'Solar'
        WHEN TRIM(source_tag) LIKE '%Battery%' THEN 'Battery'
    END AS source_tag,
    ROUND((COUNT(*) * 3.0)/60, 2) AS run_hours,
    AVG(
        CASE 
            WHEN TRIM(source_tag) LIKE '%DG%' THEN  (total_load_current*total_voltage)/1000.0
            WHEN TRIM(source_tag) LIKE '%Battery%' THEN (battery_total_current*total_voltage)/1000.0
            WHEN TRIM(source_tag) LIKE '%Solar%' THEN (solar_output_current*total_voltage)/1000.0
        END
    ) AS k_w

FROM sensor_data
WHERE 
    TRIM(source_tag) LIKE '%DG%' OR
    TRIM(source_tag) LIKE '%Solar%' OR
    TRIM(source_tag) LIKE '%Battery%'
GROUP BY
    site_code,
    date_trunc('hour', time_stamp),
    CASE 
        WHEN TRIM(source_tag) LIKE '%DG%' THEN 'DG'
        WHEN TRIM(source_tag) LIKE '%Solar%' THEN 'Solar'
        WHEN TRIM(source_tag) LIKE '%Battery%' THEN 'Battery'
    END
ORDER BY
    hourly_window