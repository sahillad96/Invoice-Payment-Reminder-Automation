import csv
from datetime import datetime

def load_invoices(path: str):
    with open(path, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def parse_due_date(date_str: str):
    # CSV uses DD-MM-YYYY
    return datetime.strptime(date_str, "%d-%m-%Y").date()
