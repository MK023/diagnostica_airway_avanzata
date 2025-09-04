# csv/csv_writer.py - Scrittura CSV con rollover automatico.
"""
Gestione scrittura CSV:
- Scrittura righe e header
- Rollover per dimensione (nuovo file con timestamp)
- Configurabile da .ini
- API: write_csv(filename, header, rows)
"""

import csv
import os
import time


def write_csv(filename, header, rows, max_bytes=5 * 1024 * 1024):
    # rollover: nuovo file se supera max_bytes
    if os.path.isfile(filename) and os.path.getsize(filename) > max_bytes:
        base, ext = os.path.splitext(filename)
        filename = f"{base}_{int(time.time())}{ext}"

    write_header = not os.path.isfile(filename)
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)
