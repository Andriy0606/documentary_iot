import csv
import random
from datetime import datetime, timedelta

def generate_random_date():
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2026, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_csv():
    male_names = ["Oleksandr", "Ivan", "Dmitro", "Serhiy", "Igor", "Andriy", "Volodymyr"]
    female_names = ["Maria", "Olena", "Anna", "Natalia", "Yulia", "Oksana", "Viktoria"]
    
    last_names = ["Melnyk", "Shevchenko", "Boyko", "Kovalenko", "Bondarenko", "Tkachenko", "Oliynyk"]
    positions = ["Junior Developer", "QA Engineer", "Data Analyst", "Project Manager", "DevOps Engineer", "Designer"]
    departments = ["IT", "HR", "Finance", "Sales", "Operations"]
    statuses = ["NEW", "ONBOARDING", "ACTIVE"]
    equipment_pool = ["Laptop", "Mouse", "Keyboard", "Headset", "Badge", "Monitor", "Docking station"]

    with open("employees.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["full_name", "email", "start_date", "position", "status", "equipment", "department"])

        for i in range(1000):
            gender = random.choice(["M", "F"])
            first_name = random.choice(male_names) if gender == "M" else random.choice(female_names)
            full_name = f"{first_name} {random.choice(last_names)}"
            start_date = generate_random_date()
            email = f"{first_name.lower()}.{i}@example.com"
            position = random.choice(positions)
            status = random.choice(statuses)
            department = random.choice(departments)

            equipment_count = random.randint(1, 3)
            equipment_items = random.sample(equipment_pool, equipment_count)
            equipment = ";".join(equipment_items)

            writer.writerow([full_name, email, start_date, position, status, equipment, department])

if __name__ == "__main__":
    generate_csv()
