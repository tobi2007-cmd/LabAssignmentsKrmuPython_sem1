  # gradebook.py
  # Author: Anujesh Gupta
  # Date: October 2024
  # Title: GradeBook Analyzer CLI
import csv
import os
def display_menu():
      print("\nWelcome to GradeBook Analyzer!")
      print("Choose an option:")
      print("1. Manual entry of student names and marks")
      print("2. Load from CSV file")
      print("3. Exit")

def manual_input():
      marks = {}
      num_students = int(input("Enter number of students: "))
      for _ in range(num_students):
          name = input("Enter student name: ")
          mark = float(input(f"Enter marks for {name}: "))
          marks[name] = mark
      return marks

def csv_input(filename):
      marks = {}
      if not os.path.exists(filename):
          print(f"File {filename} not found. Please ensure it exists.")
          return {}
      with open(filename, 'r') as file:
          reader = csv.DictReader(file)
          for row in reader:
              marks[row['Name']] = float(row['Marks'])
      return marks

def calculate_average(marks_dict):
      if not marks_dict:
          return 0
      return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict):
      if not marks_dict:
          return 0
      values = sorted(marks_dict.values())
      n = len(values)
      if n % 2 == 0:
          return (values[n//2 - 1] + values[n//2]) / 2
      else:
          return values[n//2]
def find_max_score(marks_dict):
      if not marks_dict:
          return 0
      return max(marks_dict.values())
def find_min_score(marks_dict):
      if not marks_dict:
          return 0
      return min(marks_dict.values())
def assign_grades(marks_dict):
      grades = {}
      for name, mark in marks_dict.items():
          if mark >= 90:
              grades[name] = 'A'
          elif mark >= 80:
              grades[name] = 'B'
          elif mark >= 70:
              grades[name] = 'C'
          elif mark >= 60:
              grades[name] = 'D'
          else:
              grades[name] = 'F'
      return grades
def grade_distribution(grades_dict):
      dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
      for grade in grades_dict.values():
          dist[grade] += 1
      return dist
def pass_fail_filter(marks_dict):
      passed = [name for name, mark in marks_dict.items() if mark >= 40]
      failed = [name for name, mark in marks_dict.items() if mark < 40]
      return passed, failed
def print_table(marks_dict, grades_dict):
      print("\nName\tMarks\tGrade")
      print("-" * 25)
      for name in marks_dict:
          print(f"{name}\t{marks_dict[name]}\t{grades_dict[name]}")
def export_to_csv(marks_dict, grades_dict, filename="output_grades.csv"):
      with open(filename, 'w', newline='') as file:
          writer = csv.writer(file)
          writer.writerow(["Name", "Marks", "Grade"])
          for name in marks_dict:
              writer.writerow([name, marks_dict[name], grades_dict[name]])
      print(f"Results exported to {filename}")
def main():
      while True:
          display_menu()
          choice = input("Enter choice (1/2/3): ")
          if choice == '1':
              marks = manual_input()
          elif choice == '2':
              filename = input("Enter CSV filename (e.g., grades.csv): ")
              marks = csv_input(filename)
          elif choice == '3':
              print("Exiting program.")
              break
          else:
              print("Invalid choice. Try again.")
              continue

          if not marks:
              continue

          # Task 3: Statistics
          avg = calculate_average(marks)
          med = calculate_median(marks)
          max_s = find_max_score(marks)
          min_s = find_min_score(marks)
          print(f"\nStatistics:\nAverage: {avg:.2f}\nMedian: {med:.2f}\nMax: {max_s}\nMin: {min_s}")

          # Task 4: Grades
          grades = assign_grades(marks)
          dist = grade_distribution(grades)
          print("\nGrade Distribution:")
          for grade, count in dist.items():
              print(f"{grade}: {count}")

          # Task 5: Pass/Fail
          passed, failed = pass_fail_filter(marks)
          print(f"\nPassed ({len(passed)}): {', '.join(passed)}")
          print(f"Failed ({len(failed)}): {', '.join(failed)}")

          # Task 6: Table
          print_table(marks, grades)

          # Bonus: Export
          export_choice = input("Export results to CSV? (y/n): ")
          if export_choice.lower() == 'y':
              export_to_csv(marks, grades)

          # Repeat or exit
          again = input("Analyze another set? (y/n): ")
          if again.lower() != 'y':
              break
if __name__ == "__main__":
      main()
  