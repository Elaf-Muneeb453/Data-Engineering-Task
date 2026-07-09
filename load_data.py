
import pandas as pd


def data_loading(file_path):
    try:
        df = pd.read_csv(file_path)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s", utc=True)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

result_df = data_loading("Data_Engineering_Challenge.csv")

