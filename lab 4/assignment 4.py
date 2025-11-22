import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Global variable for the DataFrame (will be updated across tasks)
df = None

# Task 1: Data Acquisition and Loading
def task1_load_and_inspect_data(file_path='weather_data.csv'):
    """
    Load the CSV file into a Pandas DataFrame and inspect its structure.
    - Prints head, info, and describe.
    """
    global df
    df = pd.read_csv(file_path)
    print("Task 1: Data Acquisition and Loading")
    print("First 5 rows (head):")
    print(df.head())
    print("\nData info:")
    print(df.info())
    print("\nDescriptive statistics:")
    print(df.describe())

# Task 2: Data Cleaning and Processing
def task2_clean_and_process_data():
    """
    Handle missing values, convert date columns to datetime, and filter relevant columns.
    - Assumes columns: 'Date', 'Temperature', 'Rainfall', 'Humidity'.
    """
    global df
    print("\nTask 2: Data Cleaning and Processing")
    # Handle missing values
    df = df.fillna(df.mean(numeric_only=True))
    # Convert date column to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    # Filter relevant columns
    relevant_columns = ['Date', 'Temperature', 'Rainfall', 'Humidity']
    df = df[relevant_columns]
    print("Cleaned DataFrame:")
    print(df.head())

# Task 3: Statistical Analysis with NumPy
def task3_compute_statistics():
    """
    Compute daily, monthly, and yearly statistics using NumPy and Pandas resample.
    - Returns stats for potential use in other tasks.
    """
    global df
    print("\nTask 3: Statistical Analysis with NumPy")
    df.set_index('Date', inplace=True)
    # Daily stats
    daily_stats = df.resample('D').agg({'Temperature': ['mean', 'min', 'max', 'std'],
                                        'Rainfall': ['mean', 'min', 'max', 'std'],
                                        'Humidity': ['mean', 'min', 'max', 'std']})
    # Monthly stats
    monthly_stats = df.resample('M').agg({'Temperature': ['mean', 'min', 'max', 'std'],
                                          'Rainfall': ['mean', 'min', 'max', 'std'],
                                          'Humidity': ['mean', 'min', 'max', 'std']})
    # Yearly stats
    yearly_stats = df.resample('Y').agg({'Temperature': ['mean', 'min', 'max', 'std'],
                                         'Rainfall': ['mean', 'min', 'max', 'std'],
                                         'Humidity': ['mean', 'min', 'max', 'std']})
    print("Daily Statistics:")
    print(daily_stats.head())
    print("\nMonthly Statistics:")
    print(monthly_stats.head())
    print("\nYearly Statistics:")
    print(yearly_stats.head())
    return daily_stats, monthly_stats, yearly_stats

# Task 4: Visualization with Matplotlib
def task4_create_visualizations():
    """
    Create required plots: line chart, bar chart, scatter plot, and combined figure.
    - Saves each as PNG files.
    """
    global df
    print("\nTask 4: Visualization with Matplotlib")
    # Line chart for daily temperature trends
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Temperature'], label='Daily Temperature')
    plt.title('Daily Temperature Trends')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.savefig('daily_temperature_trends.png')
    plt.show()
    
    # Bar chart for monthly rainfall totals
    monthly_rainfall = df['Rainfall'].resample('M').sum()
    plt.figure(figsize=(10, 5))
    monthly_rainfall.plot(kind='bar')
    plt.title('Monthly Rainfall Totals')
    plt.xlabel('Month')
    plt.ylabel('Rainfall (mm)')
    plt.savefig('monthly_rainfall_totals.png')
    plt.show()
    
    # Scatter plot for humidity vs. temperature
    plt.figure(figsize=(10, 5))
    plt.scatter(df['Humidity'], df['Temperature'])
    plt.title('Humidity vs. Temperature')
    plt.xlabel('Humidity (%)')
    plt.ylabel('Temperature (°C)')
    plt.savefig('humidity_vs_temperature.png')
    plt.show()
    
    # Combined figure: Line and bar in subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    ax1.plot(df.index, df['Temperature'], color='blue')
    ax1.set_title('Daily Temperature Trends')
    ax1.set_ylabel('Temperature (°C)')
    monthly_rainfall.plot(kind='bar', ax=ax2, color='green')
    ax2.set_title('Monthly Rainfall Totals')
    ax2.set_ylabel('Rainfall (mm)')
    plt.tight_layout()
    plt.savefig('combined_plots.png')
    plt.show()

# Task 5: Grouping and Aggregation
def task5_group_and_aggregate():
    """
    Group data by month and season, calculate aggregates using Pandas groupby.
    - Returns groups for potential use.
    """
    global df
    print("\nTask 5: Grouping and Aggregation")
    df['Month'] = df.index.month
    monthly_group = df.groupby('Month').agg({'Temperature': ['mean', 'min', 'max'],
                                             'Rainfall': 'sum',
                                             'Humidity': 'mean'})
    print("Monthly Aggregates:")
    print(monthly_group)
    
    # Define seasons
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn'
    
    df['Season'] = df['Month'].apply(get_season)
    seasonal_group = df.groupby('Season').agg({'Temperature': ['mean', 'min', 'max'],
                                               'Rainfall': 'sum',
                                               'Humidity': 'mean'})
    print("\nSeasonal Aggregates:")
    print(seasonal_group)
    return monthly_group, seasonal_group

# Task 6: Export and Storytelling
def task6_export_and_report(monthly_stats, yearly_stats):
    """
    Export cleaned data to CSV and generate a Markdown report summarizing insights.
    - Assumes plots are saved from Task 4.
    """
    global df
    print("\nTask 6: Export and Storytelling")
    # Export cleaned data
    df.to_csv('cleaned_weather_data.csv')
    
    # Generate Markdown report
    report = f"""
# Weather Data Analysis Report

## Dataset Description
- Source: Downloaded from [e.g., Kaggle or IMD].
- Columns: Date, Temperature, Rainfall, Humidity.
- Records: {len(df)}.

## Key Insights
- **Temperature Trends**: The average yearly temperature is {yearly_stats['Temperature']['mean'].mean():.2f}°C. Daily trends show seasonal variations.
- **Rainfall**: Monthly totals indicate peaks in monsoon months. Total yearly rainfall: {df['Rainfall'].sum():.2f} mm.
- **Humidity vs. Temperature**: Scatter plot suggests an inverse correlation.
- **Anomalies**: Check extremes in monthly stats for outliers.

## Visualizations
- Daily Temperature Trends: See `daily_temperature_trends.png`.
- Monthly Rainfall Totals: See `monthly_rainfall_totals.png`.
- Humidity vs. Temperature: See `humidity_vs_temperature.png`.
- Combined Plots: See `combined_plots.png`.

## Tools Used
- Pandas for data handling.
- NumPy for computations.
- Matplotlib for visualizations.
"""
    with open('weather_analysis_report.md', 'w') as f:
        f.write(report)
    print("Exported cleaned data to 'cleaned_weather_data.csv' and report to 'weather_analysis_report.md'.")

# Main execution: Run all tasks in sequence
if __name__ == "__main__":
    task1_load_and_inspect_data()
    task2_clean_and_process_data()
    daily_stats, monthly_stats, yearly_stats = task3_compute_statistics()
    task4_create_visualizations()
    monthly_group, seasonal_group = task5_group_and_aggregate()
    task6_export_and_report(monthly_stats, yearly_stats)
    print("\nAll tasks completed! Check your directory for outputs.")
