import os
import shutil

# -----------------------------------------
# PROJECT SETUP SCRIPT FOR INVOICE AUTOMATION
# Creates folder structure, moves files safely,
# generates .env and requirements.
# -----------------------------------------

# Folders to create
folders = ["src", "data", "logs", "backup"]

# Files to move into src/
python_files = [
    "main.py",
    "day6_reminder_advanced.py",
    "csv_helper.py",
    "email_helper.py",
    "log_helper.py",
    "pdf_report.py",
    "dashboard.py",
    "auth.py"
]

# CSV files → data/
csv_files = [
    "invoices.csv",
    "invoices_updated.csv"
]

# Log files → logs/
log_files = [
    "sent_log.txt",
    "summary.pdf"
]


def safe_move(file, dest):
    """Move a file unless the destination already has the same name."""
    if not os.path.exists(file):
        print(f"Skipping {file}, not found.")
        return

    target = os.path.join(dest, os.path.basename(file))

    if os.path.exists(target):
        print(f"Skipping {file}, already in {dest}")
    else:
        shutil.move(file, dest)
        print(f"Moved: {file} → {dest}")


print("\n=== Setting Up Project Structure ===\n")

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Folder ready: {folder}")

print("\n=== Moving Python Source Files ===")
for file in python_files:
    safe_move(file, "src")

print("\n=== Moving Invoices (CSV Files) ===")
for file in csv_files:
    safe_move(file, "data")

print("\n=== Moving Log Files ===")
for file in log_files:
    safe_move(file, "logs")

# Create .env if not exists
if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write("EMAIL_USER=\nEMAIL_PASS=\n")
    print("\nCreated .env template")

# Create requirements.txt
requirements = """python-dotenv
colorama
reportlab
flask
pandas
"""

with open("requirements.txt", "w") as f:
    f.write(requirements)

print("Created requirements.txt")

print("\n=== Setup Complete! ===\nYour project is ready to run.\n")
