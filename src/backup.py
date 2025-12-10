import shutil
import os
from datetime import datetime

DATA_DIR = "data"
LOG_DIR = "logs"
BACKUP_DIR = "backup"

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def backup_file(src, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    name = os.path.basename(src)
    new_name = f"{name}_{timestamp()}"
    shutil.copy(src, os.path.join(dest_dir, new_name))
    print("Backed up:", new_name)

def run_backup():
    backup_file("data/invoices_updated.csv", BACKUP_DIR)
    backup_file("logs/sent_log.txt", BACKUP_DIR)
    print("Backup completed.")

if __name__ == "__main__":
    run_backup()
