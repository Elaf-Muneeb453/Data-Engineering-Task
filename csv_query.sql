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

    ROUND(
        (COUNT(CASE WHEN TRIM(source_tag) LIKE '%Solar%' THEN 1 END) * 3.0) / 60,
        2
    ) AS solar_hours,

    ROUND(
        (COUNT(CASE WHEN TRIM(source_tag) LIKE '%Battery%' THEN 1 END) * 3.0) / 60,
        2
    ) AS battery_hours,

    ROUND(
        (COUNT(CASE WHEN TRIM(source_tag) LIKE '%DG%' THEN 1 END) * 3.0) / 60,
        2
    ) AS dg_hours

FROM sensor_data
GROUP BY
    site_code,
    date_trunc('hour', time_stamp)
ORDER BY
    hourly_window;


SELECT
    site_code, 
    date_trunc('hour', time_stamp) AS hourly_window,
    ROUND(AVG(CASE WHEN TRIM(source_tag) LIKE '%DG%' THEN (total_load_current*total_voltage)/1000 END)::numeric,2) AS dg_kw,
    ROUND(AVG(CASE WHEN TRIM(source_tag) LIKE '%Battery%' THEN (battery_total_current*total_voltage)/1000 END)::numeric,2) AS battery_kw,
    ROUND(AVG(CASE WHEN TRIM(source_tag) LIKE '%Solar%' THEN (solar_output_current*total_voltage)/1000 END)::numeric,2) AS solar_kw
FROM sensor_data
GROUP BY
    site_code,
    date_trunc('hour', time_stamp)
ORDER BY
    hourly_window;