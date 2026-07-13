# import pandas as pd

# import sqlite3

# df = pd.read_csv("Data_Engineering_Challenge.csv")

# conn = sqlite3.connect("csv_database.db")
# df.to_sql("sales", conn, if_exists="replace", index=False)
# conn.close()

import pandas as pd
from sqlalchemy import create_engine


df = pd.read_csv("Data_Engineering_Challenge.csv")

df.rename(
    columns={
        "Site Code": "site_code",
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

df.to_sql("sensor_data1", con=engine, if_exists="replace", index=False)


print("Data successfully imported into PostgreSQL!")
