"""
Building a simple gui for salary_tracker.
Goals:
- There's a main page with 3 buttons: Input, Search, Statistics.
When they are pressed, gui switches to a particular function.
- Input: users type in date, starting time and ending time.
Then data file will update accordingly.
- Search: users search information about their salary monthly and annually.
Displayed information are total number of working hours, total number of evening hours,
total number of sunday working hours, gross salary and after tax income.
- Statistics: graphs
"""

import tkinter as tk
from tkinter import messagebox
from salary_tracker import annual_income, WorkDay, read_input_file, WorkMonth


class SalaryTrackerApp:
    def __init__(self, master):
        self.search_month_entry = None
        self.search_month_label = None
        self.statistics_label = None
        self.search_label = None
        self.submit_button = None
        self.end_time_entry = None
        self.end_time_label = None
        self.start_time_entry = None
        self.start_time_label = None
        self.date_entry = None
        self.date_label = None
        self.master = master
        master.title("Salary Tracker")

        # Create main page with buttons
        self.main_frame = tk.Frame(master)
        self.main_frame.pack()

        self.input_button = tk.Button(self.main_frame, text="Input", command=self.show_input)
        self.input_button.pack(pady=10)

        self.search_button = tk.Button(self.main_frame, text="Search", command=self.show_search)
        self.search_button.pack(pady=10)

        self.statistics_button = tk.Button(self.main_frame, text="Statistics", command=self.show_statistics)
        self.statistics_button.pack(pady=10)

        # Initialize frames for each function
        self.input_frame = tk.Frame(master)
        self.search_frame = tk.Frame(master)
        self.statistics_frame = tk.Frame(master)

        # Hide frames initially
        self.input_frame.pack_forget()
        self.search_frame.pack_forget()
        self.statistics_frame.pack_forget()

    def show_input(self):
        self.hide_frames()

        # Create input widgets
        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack()

        self.date_label = tk.Label(self.input_frame, text="Date (DD.MM):")
        self.date_label.grid(row=0, column=0, padx=10, pady=5)
        self.date_entry = tk.Entry(self.input_frame)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        self.start_time_label = tk.Label(self.input_frame, text="Starting Time:")
        self.start_time_label.grid(row=1, column=0, padx=10, pady=5)
        self.start_time_entry = tk.Entry(self.input_frame)
        self.start_time_entry.grid(row=1, column=1, padx=10, pady=5)

        self.end_time_label = tk.Label(self.input_frame, text="Ending Time:")
        self.end_time_label.grid(row=2, column=0, padx=10, pady=5)
        self.end_time_entry = tk.Entry(self.input_frame)
        self.end_time_entry.grid(row=2, column=1, padx=10, pady=5)

        self.submit_button = tk.Button(self.input_frame, text="Submit", command=self.update_data_file)
        self.submit_button.grid(row=3, columnspan=2, padx=10, pady=10)

    def update_data_file(self):
        date = self.date_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()

        # Format the input data
        data = f"{date}: {start_time}-{end_time}\n"

        # Append the data to the input file
        with open("input.txt", "a") as f:
            f.write(f"{data}")

        # Display a confirmation message
        tk.messagebox.showinfo("Success", "Data Updated Successfully!")

    def show_search(self):
        self.hide_frames()

        # Create search widgets
        self.search_frame = tk.Frame(self.master)
        self.search_frame.pack()

        self.search_label = tk.Label(self.search_frame, text="Search for Salary Information")
        self.search_label.grid(row=0, columnspan=2, padx=10, pady=5)

        self.search_month_label = tk.Label(self.search_frame, text="Month (MM):")
        self.search_month_label.grid(row=0, column=0, padx=10, pady=5)
        self.search_month_entry = tk.Entry(self.search_frame)
        self.search_month_entry.grid(row=0, column=1, padx=10, pady=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_result)
        self.search_button.grid(row=3, columnspan=2, padx=10, pady=10)

    def search_result(self):
        month = self.search_month_entry.get()
        # Check if the month is valid
        try:
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid month. Please enter a number between 1 and 12.")
            return
        
        # Reload data from input file
        global annual_income
        annual_income = {}
        days = read_input_file("input.txt")
        for day in days:
            month = day.date.month
            if month not in annual_income:
                annual_income[month] = WorkMonth(month)
            annual_income[month].add_day(day)

        # Check if data exists for the specified month
        if month not in annual_income:
            tk.messagebox.showinfo("Search Result", f"No data available for month {month}.")
            return

        # Retrieve data for the specified month
        work_month = annual_income[month]

        # Calculate total working hours, evening hours, and Sunday working hours
        total_working_hours = work_month.tot_working_hrs
        total_evening_hours = work_month.evening_hrs
        total_sunday_hours = work_month.sunday_working_hrs

        # Calculate gross salary and after-tax income (if needed)
        gross_salary = work_month.cal_gross_salary()
        after_tax_income = work_month.cal_after_tax_income()

        # Display the search result
        result_message = f"Total Working Hours: {total_working_hours}\n"
        result_message += f"Total Evening Hours: {total_evening_hours}\n"
        result_message += f"Total Sunday Working Hours: {total_sunday_hours}\n"
        result_message += f"Gross Salary: {gross_salary}\n"
        result_message += f"Income after tax: {after_tax_income}"

        tk.messagebox.showinfo("Search Result", result_message)

    def show_statistics(self):
        self.hide_frames()

        # Create statistics widgets
        self.statistics_frame = tk.Frame(self.master)
        self.statistics_frame.pack()

        self.statistics_label = tk.Label(self.statistics_frame, text="Statistics")
        self.statistics_label.pack(pady=10)

        # Add widgets for displaying graphs or charts
        # Use libraries like Matplotlib or seaborn to create and display graphs

    def hide_frames(self):
        self.input_frame.pack_forget()
        self.search_frame.pack_forget()
        self.statistics_frame.pack_forget()


# Create the Tkinter root window
root = tk.Tk()

# Initialize the SalaryTrackerApp class
app = SalaryTrackerApp(root)

root.mainloop()
