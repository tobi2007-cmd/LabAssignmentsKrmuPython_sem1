# ================================================================
# Energy Dashboard
# Author : Anujesh Gupta
# Date   : 28 November 2025
# Course : Programming for Problem Solving Using Python
# ================================================================

import os
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------
# OOP CLASSES
# ------------------------------------------------

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


# Stores readings and operations for one building
class Building:
    
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, meter_reading):
        
        # Add a MeterReading object to the building
        self.meter_readings.append(meter_reading)

    def calculate_total_consumption(self):

        # Returns total kWh consumption for this building
        total = sum(r.kwh for r in self.meter_readings)
        return total

    def generate_report(self):

        # Returns a simple text report string for this building
        total = self.calculate_total_consumption()
        return f"Building: {self.name}, Total Consumption: {total:.2f} kWh"


class BuildingManager:

    # Managing multiple Building objects
    def __init__(self):
        self.buildings = {}

    def get_or_create_building(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def add_reading(self, building_name, timestamp, kwh):
        building = self.get_or_create_building(building_name)
        reading = MeterReading(timestamp, kwh)
        building.add_reading(reading)

    def get_building_reports(self):
        reports = []
        for building in self.buildings.values():
            reports.append(building.generate_report())
        return reports


# ------------------------------------------------
# DATA LOADING & CLEANING
# ------------------------------------------------

def load_and_combine_data(data_folder="data"):

    # Reads all .csv files from the given folder and combines them.

    data_folder_path = Path(data_folder)
    if not data_folder_path.exists():
        print(f"[ERROR] Data folder '{data_folder}' does not exist.")
        return pd.DataFrame()

    all_files = list(data_folder_path.glob("*.csv"))

    if not all_files:
        print("[WARNING] No CSV files found in /data folder.")
        return pd.DataFrame()

    df_list = []
    error_files = []

    for file_path in all_files:
        try:
            print(f"[INFO] Reading file: {file_path.name}")
            df = pd.read_csv(file_path)

            # Simple check for required columns
            if "timestamp" not in df.columns or "kwh" not in df.columns:
                print(f"[WARNING] Missing columns in {file_path.name}. Skipping.")
                error_files.append(file_path.name)
                continue

            # Add building name from file name (remove .csv)
            building_name = file_path.stem
            df["building"] = building_name

            # Convert timestamp to datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.dropna(subset=["timestamp", "kwh"])

            df_list.append(df)

        except FileNotFoundError:
            print(f"[ERROR] File not found: {file_path.name}")
            error_files.append(file_path.name)

        except pd.errors.ParserError:
            print(f"[ERROR] Corrupt/invalid data in: {file_path.name}")
            error_files.append(file_path.name)

    if not df_list:
        print("[ERROR] No valid data loaded.")
        return pd.DataFrame()

    df_combined = pd.concat(df_list, ignore_index=True)

    print("\n[INFO] Combined DataFrame created.")
    print(df_combined.head())

    if error_files:
        print("\n[LOG] Files with problem:")
        for f in error_files:
            print("   -", f)

    return df_combined


# ------------------------------------------------
# AGGREGATION FUNCTIONS
# ------------------------------------------------

def prepare_time_index(df):

    # Sets timestamp as index and sorts by time.
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df = df.set_index("timestamp")
    df = df.sort_index()
    return df


def calculate_daily_totals(df):

    # Returns a DataFrame with daily totals per building.
    df = prepare_time_index(df)
    
    # group by building and resample by day
    daily = df.groupby("building")["kwh"].resample("D").sum().reset_index()
    daily.rename(columns={"kwh": "daily_kwh"}, inplace=True)
    return daily


def calculate_weekly_totals(df):

    # Returns a DataFrame with weekly totals per building.
    df = prepare_time_index(df)
    weekly = df.groupby("building")["kwh"].resample("W").sum().reset_index()
    weekly.rename(columns={"kwh": "weekly_kwh"}, inplace=True)
    return weekly


def building_summary(df):

    # Returns a DataFrame with mean, min, max, total kWh per building.
    summary = df.groupby("building")["kwh"].agg(
        mean_kwh="mean",
        min_kwh="min",
        max_kwh="max",
        total_kwh="sum"
    ).reset_index()

    return summary


# ------------------------------------------------
# DASHBOARD PLOT
# ------------------------------------------------

def create_dashboard(daily_df, weekly_df, summary_df, output_file="dashboard.png"):

    if daily_df.empty or weekly_df.empty or summary_df.empty:
        print("[WARNING] Not enough data to create dashboard.")
        return

    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    fig.suptitle("Campus Energy Dashboard", fontsize=16)

    # Line plot: daily consumption per building
    ax1 = axes[0]
    for b_name, grp in daily_df.groupby("building"):
        ax1.plot(grp["timestamp"], grp["daily_kwh"], label=b_name)
    ax1.set_title("Daily Consumption")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("kWh")
    ax1.legend()
    ax1.grid(True)

    # Bar plot: average weekly usage per building
    ax2 = axes[1]
    weekly_avg = weekly_df.groupby("building")["weekly_kwh"].mean().reset_index()
    ax2.bar(weekly_avg["building"], weekly_avg["weekly_kwh"])
    ax2.set_title("Average Weekly Consumption per Building")
    ax2.set_xlabel("Building")
    ax2.set_ylabel("Average Weekly kWh")
    ax2.grid(True, axis="y")

    # Scatter: max daily vs building
    ax3 = axes[2]
    max_daily = daily_df.groupby("building")["daily_kwh"].max().reset_index()
    ax3.scatter(max_daily["building"], max_daily["daily_kwh"])
    ax3.set_title("Peak Daily Consumption per Building")
    ax3.set_xlabel("Building")
    ax3.set_ylabel("Max Daily kWh")
    ax3.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_file)
    plt.close()
    print(f"[INFO] Dashboard saved as {output_file}")


# ------------------------------------------------
# PERSISTENCE & SUMMARY REPORT
# ------------------------------------------------

def save_outputs(df_combined, summary_df, daily_df, weekly_df, output_folder="output"):
    
    os.makedirs(output_folder, exist_ok=True)

    cleaned_path = os.path.join(output_folder, "cleaned_energy_data.csv")
    summary_path = os.path.join(output_folder, "building_summary.csv")
    report_path = os.path.join(output_folder, "summary.txt")

    df_combined.to_csv(cleaned_path, index=False)
    summary_df.to_csv(summary_path, index=False)

    print(f"[INFO] Cleaned data saved to {cleaned_path}")
    print(f"[INFO] Summary data saved to {summary_path}")

    # Calculate campus-level info
    total_campus_kwh = summary_df["total_kwh"].sum()
    highest_row = summary_df.loc[summary_df["total_kwh"].idxmax()]
    highest_building = highest_row["building"]
    highest_consumption = highest_row["total_kwh"]

    # Find peak load time from daily totals
    peak_day_row = daily_df.loc[daily_df["daily_kwh"].idxmax()]
    peak_building = peak_day_row["building"]
    peak_day = peak_day_row["timestamp"]
    peak_value = peak_day_row["daily_kwh"]

    # Trend example
    first_week = weekly_df["weekly_kwh"].iloc[0]
    last_week = weekly_df["weekly_kwh"].iloc[-1]
    trend = "increased" if last_week > first_week else "decreased or remained similar"

    # Write text report
    with open(report_path, "w") as f:
        f.write("Campus Energy Summary Report\n")
        f.write("=====================================\n")
        f.write(f"Total campus consumption: {total_campus_kwh:.2f} kWh\n")
        f.write(f"Highest-consuming building: {highest_building} ({highest_consumption:.2f} kWh)\n")
        f.write(f"Peak daily load: {peak_value:.2f} kWh\n")
        f.write(f"Peak day: {peak_day} (Building: {peak_building})\n")
        f.write(f"Overall trend (weekly): {trend}\n")

    print(f"[INFO] Summary report saved to {report_path}")


# ------------------------------------------------
# MAIN
# ------------------------------------------------

def main():
    print("===== Campus Energy Dashboard (Simple Version) =====")

    # Load and combine data from /data folder
    df_combined = load_and_combine_data(data_folder="data")

    if df_combined.empty:
        print("[ERROR] No data to process. Exiting.")
        return

    # Aggregations
    daily_df = calculate_daily_totals(df_combined)
    weekly_df = calculate_weekly_totals(df_combined)
    summary_df = building_summary(df_combined)

    print("\n[INFO] Building Summary:")
    print(summary_df)

    # Create BuildingManager and fill with readings
    manager = BuildingManager()
    for _, row in df_combined.iterrows():
        manager.add_reading(
            building_name=row["building"],
            timestamp=row["timestamp"],
            kwh=row["kwh"]
        )

    print("\n[INFO] OOP Building Reports:")
    for rep in manager.get_building_reports():
        print("  ", rep)

    # Creating dashboard plot
    create_dashboard(daily_df, weekly_df, summary_df, output_file="output/dashboard.png")

    # Save outputs
    save_outputs(df_combined, summary_df, daily_df, weekly_df, output_folder="output")

    print("\n===== Done. Check the 'output' folder. =====")


if __name__ == "__main__":
    main()
