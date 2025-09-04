# network/traceroute.py - Diagnostica Traceroute (compatibilità OS, scapy, sicurezza).
"""
Modulo di diagnostica Traceroute sicuro e robusto.
- Traceroute con scapy (ICMP)
- Compatibilità multipiattaforma (Windows/Linux/Mac)
- Validazione e sanitizzazione input (no injection)
- Logging dettagliato per auditing
- Gestione errori granulare
"""

from logs.custom_logging import LogManager
from security.security import validate_address

try:
    from scapy.all import traceroute
except ImportError:
    traceroute = None

def run_traceroute_diag(address, logger: LogManager, os_type: str, max_hops=20, timeout=2):
    """
    Esegue diagnostica Traceroute:
    - Valida address per sicurezza
    - Usa scapy, limita max_hops e timeout per evitare abusi
    - Log di ogni passo
    """
    if not validate_address(address):
        logger.error(f"Indirizzo non valido: {address}")
        print("ERRORE: Indirizzo non valido.")
        return

    logger.info(f"Inizio traceroute verso {address} (OS: {os_type})")
    if traceroute:
        try:
            res, _ = traceroute([address], maxttl=max_hops, timeout=timeout, verbose=0)
            hops = []
            for idx, (snd, rcv) in enumerate(res):
                hop_ip = rcv.src if rcv else '*'
                rtt = (rcv.time - snd.sent_time)*1000 if rcv else None
                hops.append((hop_ip, round(rtt,2) if rtt is not None else None))
            logger.info(f"Traceroute hops: {hops}")
            print("--- Traceroute ---")
            for hop in hops:
                print(f"{hop[0]} ({hop[1]} ms)" if hop[1] is not None else f"{hop[0]} (timeout)")
        except Exception as e:
            logger.error(f"Errore traceroute: {e}", exc_info=True)
            print("ERRORE: Traceroute fallito.")
    else:
        logger.error("Modulo traceroute/scapy non disponibile.")
        print("ERRORE: modulo traceroute non disponibile.")
    logger.info("Fine diagnostica traceroute.")