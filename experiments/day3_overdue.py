import csv
from datetime import datetime

today = datetime.today().date()

with open("invoices.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    print("Overdue invoices:")
    for row in reader:
        due_date = datetime.strptime(row["DueDate"], "%Y-%m-%d").date()

        if due_date < today and row["Status"].lower() == "pending":
            print(
                "Invoice:", row["InvoiceID"],
                "| Client:", row["ClientName"],
                "| Amount:", row["Amount"],
                "| Due:", row["DueDate"]
            )
