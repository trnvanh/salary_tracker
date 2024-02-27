"""
**Introduction**

An app to track salary monthly and annually.
It can be developed to become a finance app to track incomes and spending/ saving.

**How to use?**

User can input hours of work, including evening, sunday, holiday, and tax rate in a period (a week,  a month.
User can also put the total amount working hours if they don’t want the program to calculate.
As a result the income (after tax) is shown.

Basic goals:
- Read input file to get days, hours, bonus, etc
- Calculate total hours of work
- Calculate gross salary and after tax salary
- Store monthly and annually incomes

Later goals:
- Build a GUI with a calendar to take input about hours of working

Classes:
- WorkDay: date, hours of work, evening_hours, sunday_hours, salary
- WorkMonth

"""
import datetime

SALARY_PER_HOUR = 12.77
EVENING_BONUS = 1.33
EXPECTED_WORKING_HOURS = 120
TAX_RATE = 0.05

annual_income = {}


class WorkDay:
    def __init__(self, date, starting_shift, ending_shift):
        self.date = date
        self.starting_shift = starting_shift
        self.ending_shift = ending_shift
        self.tot_working_hrs = ending_shift - starting_shift
        self.evening_hrs = self.cal_evening_hrs()
        self.is_sunday = self._is_sunday()

    def _is_sunday(self):
        return self.date.weekday() == 6

    def cal_evening_hrs(self):
        if self.ending_shift < 18:
            evening_hrs = 0
        else:
            evening_hrs = self.ending_shift - 18
        return evening_hrs


class WorkMonth:
    def __init__(self, month):
        self.month = month
        self.days = []
        self.tot_working_hrs = 0
        self.evening_hrs = 0
        self.sunday_working_hrs = 0

    def add_day(self, work_day):
        self.days.append(work_day)
        self.tot_working_hrs += work_day.tot_working_hrs
        self.evening_hrs += work_day.evening_hrs
        if work_day.is_sunday:
            self.sunday_working_hrs += work_day.tot_working_hrs

    def cal_gross_salary(self):
        return (self.tot_working_hrs + self.sunday_working_hrs) * SALARY_PER_HOUR + self.evening_hrs * EVENING_BONUS

    def cal_after_tax_income(self):
        return self.cal_gross_salary() * (1 - TAX_RATE)

    def has_enough_working_hrs(self):
        if self.tot_working_hrs >= EXPECTED_WORKING_HOURS:
            return True


def read_input_file(file):
    days = []
    with open(file, 'r') as f:
        for line in f:
            date, time_range = line.strip().split(':')
            day, month = map(int, date.split('.'))
            year = datetime.datetime.now().year
            date_object = datetime.datetime(year, month, day)
            starting_time, ending_time = map(int, time_range.split('-'))
            days.append(WorkDay(date_object, starting_time, ending_time))
    return days


days = read_input_file("input.txt")
for day in days:
    month = day.date.month
    if month not in annual_income:
        annual_income[month] = WorkMonth(month)
    annual_income[month].add_day(day)

# For example
if __name__ == "__main__":
    month_input = input("Enter the month (e.g., January, Jan, 1): ").lower()
    month = None
    if month_input in ("january", "jan", "1", "01"):
        month = 1
    elif month_input in ("february", "feb", "2", "02"):
        month = 2
    else:
        print("Invalid month input!")
        exit()

    if month in annual_income:
        print(f"Total working hours: {annual_income[month].tot_working_hrs}")
        print(f"Evening hours: {annual_income[month].evening_hrs}")
        print(f"Sunday hours: {annual_income[month].sunday_working_hrs}")
        print(f"Gross salary: {annual_income[month].cal_gross_salary()}")
        print(f"Income after tax: {annual_income[month].cal_after_tax_income()}")
        if annual_income[month].has_enough_working_hrs():
            print("Enough working hours!")
        else:
            print("Number of working hours less than expected: ", EXPECTED_WORKING_HOURS -
                  annual_income[month].tot_working_hrs)

    else:
        print(f"No data available for {month_input.capitalize()}.")
