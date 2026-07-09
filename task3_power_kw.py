import pandas as pd

from load_data import result_df

def data_loading():
    try:
        df = result_df.copy()
        df["hour_window"] = df["Timestamp"].dt.floor("h")
        dg = df[df["Source Tag"].str.contains("DG", case=False, na=False)]
        dg["kW"] = (dg["Total Load Current"] * dg["Total Voltage"]) / 1000
        dg_result = (dg.groupby(["Site Code", "hour_window"]).agg(Reading_Count=("Source Tag", "size"),kw=("kW", "mean"),).reset_index())
        dg_result["source"] = "DG"
        dg_result["run_hours"] = dg_result["Reading_Count"] * 3 / 60

        solar = df[df["Source Tag"].str.contains("Solar", case=False, na=False)]
        solar["kW"] = (solar["Solar Output Current"] * solar["Total Voltage"]) / 1000
        solar_result = (solar.groupby(["Site Code", "hour_window"])
                        .agg( Reading_Count=("Source Tag", "size"),
                             kw=("kW", "mean"),)
                        .reset_index())

        solar_result["source"] = "Solar"
        solar_result["run_hours"] = solar_result["Reading_Count"] * 3 / 60

        battery = df[df["Source Tag"].str.contains("Battery", case=False, na=False)]

        battery["kW"] = (battery["Battery Total Current"] * battery["Total Voltage"]) / 1000

        battery_result = (battery.groupby(["Site Code", "hour_window"]).agg(Reading_Count=("Source Tag", "size"),kw=("kW", "mean"),).reset_index())

        battery_result["source"] = "Battery"
        battery_result["run_hours"] = battery_result["Reading_Count"] * 3 / 60

        result = pd.concat([dg_result, solar_result, battery_result],ignore_index=True,)
        result = (result[["Site Code", "hour_window", "source", "run_hours", "kw"]]
                  .rename(columns={"Site Code": "site_code"})
                  .query("run_hours > 0")
                  .sort_values(["hour_window", "source"])
                  .reset_index(drop=True)
                  )
        result["kw"] = result["kw"].round(2)

        print(result)

        return result
    
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

res = data_loading()
res.to_csv("power_kw.csv", index=False)
