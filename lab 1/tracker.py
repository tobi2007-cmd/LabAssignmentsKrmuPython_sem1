"""
Project Title: Daily Calorie Tracker CLI
Name: Anujesh Gupta
Date: 7/10/2025
Course: Programming for Problem Solving using Python
"""

import datetime

# Welcome message
print("========================================")
print("      Welcome to Daily Calorie Tracker")
print("========================================")
print("This tool helps you track your daily calorie intake,")
print("compare it with your daily limit, and save the session log.\n")

# Input & Data Collection
meals = []
calories = []

num_meals = int(input("How many u have taken today? "))

for i in range(num_meals):
    print(f"\nEnter details for Meal {i + 1}:")
    meal_name = input("Meal Name (e.g., Breakfast, Lunch, Snack): ")
    calorie_amount = float(input("Calories for this meal: "))
    
    meals.append(meal_name)
    calories.append(calorie_amount)

# Calorie Calculations
total_calories = sum(calories)
average_calories = total_calories / len(calories)

daily_limit = float(input("\nEnter your daily calorie limit: "))

# Exceed Limit Warning System
if total_calories > daily_limit:
    status_message = "⚠️  You have exceeded your daily calorie limit!"
else:
    status_message = "✅ Great job! You are within your daily calorie limit."

# Neatly Formatted Output
print("\n\n========================================")
print("         Daily Calorie Summary")
print("========================================")
print(f"{'Meal Name':<15}{'Calories'}")
print("----------------------------------------")

for i in range(len(meals)):
    print(f"{meals[i]:<15}{calories[i]}")

print("----------------------------------------")
print(f"{'Total:':<15}{total_calories}")
print(f"{'Average:':<15}{average_calories:.2f}")
print("----------------------------------------")
print(status_message)
print("========================================\n")

# Save Session Log to File
save = input("Would you like to save this session report to a file? (yes/no): ").strip().lower()

if save == "yes":
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = "calorie_log.txt"

    with open(filename, "a") as file:
        file.write("========================================\n")
        file.write(f"Session Date & Time: {timestamp}\n")
        file.write("----------------------------------------\n")
        for i in range(len(meals)):
            file.write(f"{meals[i]:<15}{calories[i]}\n")
        file.write("----------------------------------------\n")
        file.write(f"Total Calories: {total_calories}\n")
        file.write(f"Average Calories: {average_calories:.2f}\n")
        file.write(f"Daily Limit: {daily_limit}\n")
        file.write(f"Status: {status_message}\n")
        file.write("========================================\n\n")

    print(f"✅ Session saved successfully as '{filename}'.")
else:
    print("Session not saved. Thank you for using the tracker!")

print("\nThank you for using the Daily Calorie Tracker! Stay healthy 😄")
