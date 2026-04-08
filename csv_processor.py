import csv
import logging
from collections import defaultdict

class InvalidDataFormatError(Exception):
    pass
logging.basicConfig(
    filename="processor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def read_csv(file_name):
    
    employees = []
    required_columns = ["id", "name", "dept", "salary"]

    try:
        with open(file_name, mode='r', newline='') as file:

            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                raise ValueError("Empty CSV file")
            if reader.fieldnames != required_columns:
                raise InvalidDataFormatError(
                    "Invalid Data Format: Incorrect headers"
                )

            for line_no, row in enumerate(reader, start=2):
                if len(row) != len(required_columns):
                    raise InvalidDataFormatError(
                        f"Invalid Data Format at line {line_no}"
                    )
                if any(row[col] is None or row[col] == "" for col in required_columns):
                    raise InvalidDataFormatError(
                        f"Missing value at line {line_no}"
                    )
                try:
                    row["salary"] = float(row["salary"])
                except ValueError:
                    raise InvalidDataFormatError(
                        f"Invalid salary format at line {line_no}"
                    )

                employees.append(row)

        logging.info("CSV file read successfully")
        return employees

    except FileNotFoundError:
        logging.error("File not found")
        print("Error: employees.csv not found")

    except ValueError as e:
        logging.error(str(e))
        print(e)

    except InvalidDataFormatError as e:
        logging.error(str(e))
        print(e)

    except Exception as e:
        logging.error(str(e))
        print("Unexpected Error:", e)

    return []
def analyze_salary(employees):

    dept_salary = defaultdict(list)

    for emp in employees:
        dept_salary[emp["dept"]].append(emp["salary"])

    dept_avg = {
        dept: sum(salaries)/len(salaries)
        for dept, salaries in dept_salary.items()
    }

    highest_paid = {}

    for dept in dept_salary:
        highest_paid[dept] = max(
            [e for e in employees if e["dept"] == dept],
            key=lambda x: x["salary"]
        )

    logging.info("Salary analysis completed")

    return dept_avg, highest_paid
def add_bonus(employees):
    for emp in employees:
        emp["bonus_salary"] = round(emp["salary"] * 1.10, 2)

    logging.info("Bonus salary added")
def employees_above_average(employees, dept_avg):
    filtered = [
        emp for emp in employees
        if emp["salary"] > dept_avg[emp["dept"]]
    ]

    logging.info("Filtering completed")
    return filtered
def write_csv(file_name, employees):

    fieldnames = ["id", "name", "dept", "salary", "bonus_salary"]

    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(employees)

    logging.info("Updated CSV written successfully")
def display_results(dept_avg, highest_paid, filtered):

    print("\nDepartment-wise Average Salary:")
    for dept, avg in dept_avg.items():
        print(f"{dept} -> {int(avg)}")

    print("\nHighest Paid Employee per Department:")
    for dept, emp in highest_paid.items():
        print(f"{dept} -> {emp['name']} ({int(emp['salary'])})")

    print("\nEmployees Above Department Average:")
    for emp in filtered:
        print(f"{emp['name']} ({emp['dept']}, {int(emp['salary'])})")
def main():

    employees = read_csv("employees.csv")

    if not employees:
        return

    dept_avg, highest_paid = analyze_salary(employees)

    add_bonus(employees)

    filtered = employees_above_average(employees, dept_avg)

    write_csv("updated_employees.csv", employees)

    display_results(dept_avg, highest_paid, filtered)

    logging.info("Processing completed successfully")
if __name__ == "__main__":
    main()