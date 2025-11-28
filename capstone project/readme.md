📘 Campus Energy Dashboard – Capstone Project

A Python-based end-to-end energy analytics system designed to help campus administrators understand electricity consumption patterns, identify inefficiencies, and explore energy-saving opportunities.

This project completes all requirements from the Capstone Assignment: “End-to-End Energy Consumption Analysis and Visualization.”

📁 Project Structure
campus-energy-dashboard/
│
├── data/
│   ├── sample_energy_data.csv
│
├── dashboard.png
├── cleaned_energy_data.csv
├── building_summary.csv
├── summary.txt
│
├── campus_energy_dashboard.py
├── README.md

🎯 Objective

Build an automated pipeline that:

Reads multiple energy meter datasets

Cleans and validates the data

Aggregates daily & weekly consumption

Uses OOP to model buildings and readings

Generates multi-chart dashboards

Produces CSV summaries and a text report

📚 Project Overview

The campus management team wants a better understanding of electricity consumption patterns across buildings. Your dashboard helps them:

Identify high-consumption buildings

Detect peak load times

Compare daily vs weekly usage

Explore long-term trends

Improve data-driven decision-making

This system automates ingestion → analysis → visualization → reporting.

🧩 Features
✔ 1. Data Ingestion & Validation

Automatically loads all .csv files from /data/

Assigns building names dynamically

Handles missing files, corrupt lines, and invalid values

Produces a consolidated dataset

✔ 2. Aggregation & Trend Analysis

Daily total energy usage

Weekly average usage

Per-building summary (total, mean, min, max)

✔ 3. Object-Oriented Architecture

MeterReading class

Building class with summary functions

BuildingManager for multi-building operations

✔ 4. Visualization Dashboard

Generates dashboard.png with:

Line chart — daily energy usage

Bar chart — weekly average per building

Scatter plot — peak-hour distribution

✔ 5. Persistence & Reporting

Automatically exports:

cleaned_energy_data.csv

building_summary.csv

summary.txt summarizing campus insights

🛠️ Technologies Used
Component	Technology
Data Processing	Python, Pandas
Visualization	Matplotlib
Architecture	OOP (Python Classes)
File System	pathlib, os
Reporting	CSV + TXT export
🚀 How to Run the Project
1. Install Dependencies
pip install pandas matplotlib

2. Add Your Data

Place your CSV files inside:

/data/


Each CSV should contain:

timestamp, kwh
2024-01-01 01:00, 10.5
...


The script automatically adds building names based on file names.

3. Run the Script
python campus_energy_dashboard.py

4. Output Files Generated
File	Description
cleaned_energy_data.csv	Merged, validated dataset
building_summary.csv	Total, avg, min, max per building
dashboard.png	Multi-chart visualization
summary.txt	Executive insights
📊 Sample Insights (from demo data)

Total campus consumption

Highest consuming building

Peak load timestamps

Usage variation across days & weeks

🧪 Sample Dataset Included

A small dataset (sample_energy_data.csv) is included for testing.
You can replace it with real campus meter logs.

📝 Academic Integrity

This project is developed following the Capstone Assignment guidelines.
Any external dataset or reference should be acknowledged accordingly.

👨‍💻 Author

Anujesh Gupta 
B.Tech CSE (AI/ML)
Programming for Problem Solving using Python Lab
