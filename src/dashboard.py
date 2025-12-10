from flask import Flask, render_template_string
import csv
from datetime import datetime
from csv_helper import parse_due_date

app = Flask(__name__)

CSV_PATH = "data/invoices_updated.csv"

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Invoice Dashboard</title>
    <style>
        body { font-family: Arial; padding: 20px }
        table { border-collapse: collapse; width: 100% }
        th, td { border: 1px solid #ccc; padding: 8px }
        th { background: #f0f0f0 }
        .overdue { background: #ffdddd }
    </style>
</head>
<body>
    <h2>Invoice Status Dashboard</h2>
    <table>
        <tr>
            <th>ID</th><th>Client</th><th>Email</th>
            <th>Amount</th><th>Due Date</th><th>Status</th><th>Days Overdue</th>
        </tr>
        {% for row in rows %}
        <tr class="{{ 'overdue' if row.overdue else '' }}">
            <td>{{ row.id }}</td>
            <td>{{ row.name }}</td>
            <td>{{ row.email }}</td>
            <td>{{ row.amount }}</td>
            <td>{{ row.due }}</td>
            <td>{{ row.status }}</td>
            <td>{{ row.days_overdue }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def dashboard():
    today = datetime.today().date()
    rows = []

    with open(CSV_PATH, "r") as file:
        reader = csv.DictReader(file)
        for r in reader:
            due_date = parse_due_date(r["due_date"])
            overdue = due_date < today and r["status"].lower() == "pending"
            days = (today - due_date).days if overdue else 0

            rows.append({
                "id": r["invoice_id"],
                "name": r["client_name"],
                "email": r["client_email"],
                "amount": r["amount"],
                "due": r["due_date"],
                "status": r["status"],
                "overdue": overdue,
                "days_overdue": days
            })

    return render_template_string(TEMPLATE, rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
