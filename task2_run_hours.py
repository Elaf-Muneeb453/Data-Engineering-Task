import pandas as pd

from load_data import result_df

def data_loading():
    try:
        df = result_df.copy()
        df["hour_window"] = df["Timestamp"].dt.floor("h")
        print(df["hour_window"])

        dg = df[df["Source Tag"].str.contains("DG", case=False, na=False)]

        dg_result = (
            dg.groupby(["Site Code", "hour_window"])
            .size()
            .reset_index(name="Reading Count")
        )

        dg_result["source"] = "DG"
        dg_result["run_hours"] = dg_result["Reading Count"] * 3 / 60
        
        
        solar = df[df["Source Tag"].str.contains("Solar", case=False, na=False)]

        solar_result = (
            solar.groupby(["Site Code", "hour_window"])
            .size()
            .reset_index(name="Reading Count")
        )

        solar_result["source"] = "Solar"
        solar_result["run_hours"] = solar_result["Reading Count"] * 3 / 60
        
        battery = df[df["Source Tag"].str.contains("Battery", case=False, na=False)]

        battery_result = (
            battery.groupby(["Site Code", "hour_window"])
            .size()
            .reset_index(name="Reading Count")
        )

        battery_result["source"] = "Battery"
        battery_result["run_hours"] = battery_result["Reading Count"] * 3 / 60

        result = pd.concat([dg_result, solar_result, battery_result], ignore_index=True)

        result = (
            result[["Site Code", "hour_window", "source","run_hours"]]
            .rename(columns={"Site Code": "site_code"})
            .query("run_hours > 0")
            .sort_values(["hour_window", "source"])
            .reset_index(drop=True)
        )

        # print(result)

        return result
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


dataframe = data_loading()
dataframe.to_csv("run_hours_output.csv", index=False)
