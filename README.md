# BMI Calculator — OASIS INFOBYTE Internship

## Project Overview
The BMI Calculator is a desktop application developed using Python as part of the OASIS INFOBYTE Python Programming Internship, Task 2.

It calculates Body Mass Index (BMI) using a user's height and weight and displays the corresponding BMI category.

## Features
- Enter the user's name, height, and weight.
- Calculate BMI automatically.
- Classify BMI as Underweight, Normal, Overweight, or Obese.
- Display color-coded results.
- Validate invalid and non-positive measurements.
- Store user records using SQLite.
- View saved BMI history.
- Display BMI history using a Matplotlib graph.

## Technologies Used
- Python
- Tkinter — graphical user interface
- SQLite — database storage
- Matplotlib — BMI history graph

## BMI Formula
BMI = Weight (kg) / Height (m)²

## Installation and Setup

### 1. Install Python
Install Python 3 if it is not already installed.

### 2. Install dependencies
Run this command in the terminal:

`python -m pip install -r requirements.txt`

### 3. Run the application
Run:

`python main.py`

## Database
The application uses SQLite to store names, heights, weights, BMI values, categories, and timestamps in `bmi_records.db`.

## Project Structure
- `main.py` — application code
- `bmi_records.db` — SQLite database
- `requirements.txt` — Python dependencies
- `screenshots/` — project screenshots

## Internship
Track: Python Programming  
Organization: OASIS INFOBYTE  
Task: Task 2 — BMI Calculator
