import csv

with open("invoices.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    print("All invoices:")
    for row in reader:
        print(row)
    