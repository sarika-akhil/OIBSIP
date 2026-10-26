import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
# Connect to the SQLite database
connection = sqlite3.connect("bmi_records.db")

# Create a cursor to execute SQL commands
cursor = connection.cursor()

# Create a table if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        height REAL NOT NULL,
        weight REAL NOT NULL,
        bmi REAL NOT NULL,
        category TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Save the table structure
connection.commit()

# Create the main window
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("400x400")
window.resizable(False, False)

# Heading
title = tk.Label(
    window,
    text="BMI Calculator",
    font=("Arial", 18, "bold")
)
title.pack(pady=15)
# Name input
name_label = tk.Label(window, text="Enter Your Name:")
name_label.pack()

name_entry = tk.Entry(window)
name_entry.pack(pady=5)

# Height input
height_label = tk.Label(window, text="Enter Height (cm):")
height_label.pack()

height_entry = tk.Entry(window)
height_entry.pack(pady=5)

# Weight input
weight_label = tk.Label(window, text="Enter Weight (kg):")
weight_label.pack()

weight_entry = tk.Entry(window)
weight_entry.pack(pady=5)

# Result label
result_label = tk.Label(
    window,
    text="Enter your details to calculate BMI",
    font=("Arial", 12),
    wraplength=350
)
result_label.pack(pady=15)


# BMI calculation function

def calculate_bmi():
    try:
        # Get user inputs
        name = name_entry.get().strip()

        if not name:
            result_label.config(
                text="Please enter your name!",
                fg="red"
            )
            return

        height = float(height_entry.get())
        weight = float(weight_entry.get())

        # Validate height and weight
        if height <= 0 or weight <= 0:
            result_label.config(
                text="Height and weight must be positive!",
                fg="red"
            )
            return

        # Convert centimetres to metres
        height = height / 100

        # Calculate BMI
        bmi = weight / (height * height)

        # Determine BMI category
        if bmi < 18.5:
            category = "Underweight"
            color = "blue"
        elif bmi < 25:
            category = "Normal"
            color = "green"
        elif bmi < 30:
            category = "Overweight"
            color = "orange"
        else:
            category = "Obese"
            color = "red"

        # Save the user's BMI record
        cursor.execute("""
            INSERT INTO bmi_records
            (name, height, weight, bmi, category)
            VALUES (?, ?, ?, ?, ?)
        """, (name, height * 100, weight, bmi, category))

        connection.commit()

        # Display the result
        result_label.config(
            text=f"Name: {name}\nBMI: {bmi:.2f}\nCategory: {category}",
            fg=color
        )

    except ValueError:
        result_label.config(
            text="Please enter valid numbers for height and weight!",
            fg="red"
        )

    except sqlite3.Error as e:
        result_label.config(
            text=f"Database error: {e}",
            fg="red"
        )


        

# Calculate button
calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    command=calculate_bmi
)
calculate_button.pack(pady=10)

def view_history():
    history_window = tk.Toplevel(window)
    history_window.title("BMI History")
    history_window.geometry("500x350")

    heading = tk.Label(
        history_window,
        text="Saved BMI Records",
        font=("Arial", 16, "bold")
    )
    heading.pack(pady=10)

    cursor.execute("""
        SELECT name, height, weight, bmi, category, created_at
        FROM bmi_records
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    if not records:
        tk.Label(
            history_window,
            text="No BMI records found."
        ).pack(pady=20)
        return

    records_text = tk.Text(
        history_window,
        width=58,
        height=15,
        font=("Consolas", 9)
    )
    records_text.pack(padx=10, pady=10)

    for record in records:
        name, height, weight, bmi, category, date = record

        records_text.insert(
            tk.END,
            f"Name: {name}\n"
            f"Height: {height:.1f} cm | Weight: {weight:.1f} kg\n"
            f"BMI: {bmi:.2f} | Category: {category}\n"
            f"Date: {date}\n"
            f"{'-' * 45}\n"
        )

    records_text.config(state="disabled")
history_button = tk.Button(
    window,
    text="View BMI History",
    command=view_history
)
history_button.pack(pady=5)

def show_bmi_graph():
    name = name_entry.get().strip()

    if not name:
        result_label.config(
            text="Enter a name to view the BMI graph!",
            fg="red"
        )
        return

    try:
        cursor.execute("""
            SELECT created_at, bmi
            FROM bmi_records
            WHERE name = ? COLLATE NOCASE
            ORDER BY id ASC
        """, (name,))

        records = cursor.fetchall()

        if not records:
            result_label.config(
                text=f"No BMI history found for {name}.",
                fg="red"
            )
            return

        dates = [record[0] for record in records]
        bmi_values = [record[1] for record in records]

        plt.figure(figsize=(8, 5))
        plt.plot(
            range(1, len(bmi_values) + 1),
            bmi_values,
            marker="o",
            label=name
        )
        plt.xticks(
            range(1, len(bmi_values) + 1),
            dates,
            rotation=45,
            ha="right"
        )

        plt.title(f"BMI History for {name}")
        plt.xlabel("Measurement date and time")
        plt.ylabel("BMI")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    except sqlite3.Error as e:
        result_label.config(
            text=f"Database error: {e}",
            fg="red"
        )

graph_button = tk.Button(
    window,
    text="Show BMI Graph",
    command=show_bmi_graph
)
graph_button.pack(pady=5)
# Start the application
window.mainloop()
