import os
from datetime import datetime

def load_sent_log(path):
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Create file if not exists
    if not os.path.exists(path):
        open(path, "w").close()

    sent_ids = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if parts:
                sent_ids.add(parts[0].strip())
    return sent_ids

def save_sent_invoice(path, invoice_id):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{invoice_id} | {timestamp}\n")
