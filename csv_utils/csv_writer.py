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


def write_csv(filename, header, rows, max_bytes=5 * 1024 * 1024, folder="csv_utils"):
    """
    Scrive dati su CSV in una cartella dedicata.
    Se il file supera max_bytes, crea nuovo file con timestamp.
    """
    # Assicurati che la cartella esista
    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)

    # Percorso completo file
    full_path = os.path.join(folder, filename)

    # rollover: nuovo file se supera max_bytes
    if os.path.isfile(full_path) and os.path.getsize(full_path) > max_bytes:
        base, ext = os.path.splitext(full_path)
        full_path = f"{base}_{int(time.time())}{ext}"

    write_header = not os.path.isfile(full_path)
    with open(full_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(header)
        for row in rows:
            writer.writerow(row)
