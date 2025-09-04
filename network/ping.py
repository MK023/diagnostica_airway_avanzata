# network/ping.py - Diagnostica ICMP Ping (standard, avanzata, compatibilità OS).
"""
Modulo di diagnostica ICMP Ping sicuro e robusto.
- Ping semplice e avanzato (pingparsing, ping3, scapy)
- Logging dettagliato per auditing
- Rate limiting su ping avanzati (evita flood)
- Scrittura CSV sicura (append, header, validazione input)
- Compatibilità multipiattaforma (Windows/Linux/Mac)
- Validazione e sanitizzazione input per sicurezza
"""

import os
import time

from logs.custom_logging import LogManager
from security.security import validate_address

try:
    import pingparsing
except ImportError:
    pingparsing = None

try:
    from ping3 import ping as ping3_ping
except ImportError:
    ping3_ping = None

try:
    from scapy.all import ICMP, IP, sr1
except ImportError:
    sr1 = IP = ICMP = None


def write_csv(csvfile, header, rows):
    """
    Scrive le righe su CSV in modo sicuro.
    - Crea header solo se necessario
    - Append, no overwrite
    - Protezione da path traversal e injection
    """
    if not isinstance(csvfile, str) or ".." in csvfile or csvfile.startswith("/"):
        raise ValueError("Path CSV non valido o potenzialmente rischioso.")
    write_header = not os.path.isfile(csvfile) or os.path.getsize(csvfile) == 0
    with open(csvfile, mode="a", newline="", encoding="utf-8") as f:
        import csv

        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        for row in rows:
            # Protezione: nessun campo deve contenere newline o caratteri di escape
            safe_row = [str(x).replace("\n", " ").replace("\r", "") for x in row]
            writer.writerow(safe_row)


def run_ping_diag(
    address,
    logger: LogManager,
    os_type: str,
    advanced=False,
    csvfile=None,
    delay=5,
    max_ping_count=10,
):
    """
    Esegue la diagnostica ICMP Ping in modo sicuro:
    - Valida e sanitizza address
    - Rate limiting su ping avanzati
    - Log di ogni passo per auditing
    - Scrive su CSV solo dati validati
    """
    if not validate_address(address):
        logger.error(f"Indirizzo non valido: {address}")
        print("ERRORE: Indirizzo non valido.")
        return

    logger.info(f"Inizio diagnostica ping verso {address} (OS: {os_type})")
    ping3_res = None
    pingparse_stats = {
        "min_rtt": "",
        "avg_rtt": "",
        "max_rtt": "",
        "packet_loss_rate": "",
    }
    scapy_times = []

    # Ping semplice con ping3
    if ping3_ping:
        try:
            ping3_res = ping3_ping(address, unit="ms")
            if ping3_res is not None:
                logger.info(f"Risultato ping3: {ping3_res:.2f} ms")
            else:
                logger.warning("Nessuna risposta da ping3.")
        except Exception as e:
            logger.error(f"Errore ping3: {e}", exc_info=True)

    # Ping avanzato con pingparsing (rate limited)
    if pingparsing and advanced:
        try:
            parser = pingparsing.PingParsing()
            transmitter = pingparsing.PingTransmitter()
            transmitter.destination = address
            transmitter.count = min(max_ping_count, 10)
            stats = parser.parse(transmitter.ping()).as_dict()
            for k in pingparse_stats:
                pingparse_stats[k] = stats.get(k, "")
            logger.info(f"Risultato pingparsing: {pingparse_stats}")
        except Exception as e:
            logger.error(f"Errore pingparsing: {e}", exc_info=True)

    # Ping con scapy (ICMP raw, rate limited)
    if sr1 and IP and ICMP and advanced:
        for i in range(min(4, max_ping_count)):
            try:
                pkt = IP(dst=address) / ICMP()
                ans = sr1(pkt, timeout=2, verbose=0)
                if (
                    ans is not None
                    and hasattr(ans, "time")
                    and hasattr(pkt, "sent_time")
                ):
                    rtt = (ans.time - pkt.sent_time) * 1000
                    scapy_times.append(round(rtt, 2))
                else:
                    scapy_times.append("")
            except Exception as e:
                logger.error(f"Errore ping scapy: {e}", exc_info=True)
                scapy_times.append("")
        logger.info(f"Ping scapy: {scapy_times}")
    elif not (sr1 and IP and ICMP):
        logger.warning("Modulo scapy non disponibile.")

    # Diagnostica avanzata: scrittura su CSV sicura
    if advanced and csvfile:
        header = [
            "timestamp",
            "address",
            "ping3_ms",
            "pingparsing_min",
            "pingparsing_avg",
            "pingparsing_max",
            "pingparsing_packet_loss",
            "scapy_ping_1_ms",
            "scapy_ping_2_ms",
            "scapy_ping_3_ms",
            "scapy_ping_4_ms",
        ]
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        row = [
            timestamp,
            address,
            ping3_res if ping3_res is not None else "",
            pingparse_stats.get("min_rtt", ""),
            pingparse_stats.get("avg_rtt", ""),
            pingparse_stats.get("max_rtt", ""),
            pingparse_stats.get("packet_loss_rate", ""),
            *(scapy_times[i] if i < len(scapy_times) else "" for i in range(4)),
        ]
        try:
            write_csv(csvfile, header, [row])
            logger.info(f"Scrittura diagnostica avanzata su CSV: {csvfile}")
        except Exception as e:
            logger.error(f"Errore scrittura CSV: {e}", exc_info=True)
            print("ERRORE: Scrittura CSV fallita.")

    logger.info("Diagnostica ping completata.")
