import pandas as pd
from sqlalchemy import create_engine


df = pd.read_csv("Data_Engineering_Challenge.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit = 's', utc=True)

df.rename(
    columns={
        "Site Code": "site_code",
        "Timestamp": "time_stamp",
        "Source Tag": "source_tag",
        "Solar Output Current": "solar_output_current",
        "Total Load Current": "total_load_current",
        "Battery Total Current": "battery_total_current",
        "Total Voltage": "total_voltage",
    },
    inplace=True,
)

username = "postgres"
password = "123789"
host = "localhost"
port = "5000"
database = "csv_database"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
)

df.to_sql("sensor_data", con=engine, if_exists="append", index=False)


print("Data successfully imported into PostgreSQL!")

