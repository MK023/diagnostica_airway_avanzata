# network/dns.py - Diagnostica DNS e sicurezza.
"""
Modulo di diagnostica DNS sicuro e robusto.
- Risoluzione nome, reverse, check record (A, AAAA, MX, TXT)
- Logging dettagliato per auditing
- Validazione e sanitizzazione input
- Gestione errori granulare
"""

import socket

from logs.custom_logging import LogManager
from security.security import validate_address


def run_dns_diag(address, logger: LogManager, record_types=None, dns_timeout=3):
    """
    Esegue diagnostica DNS:
    - Valida address per sicurezza
    - Risolve nome, reverse, record DNS
    - Log di ogni passo
    """
    if not validate_address(address):
        logger.error(f"Indirizzo/Dominio non valido: {address}")
        print("ERRORE: Indirizzo/Dominio non valido.")
        return

    logger.info(f"Avvio diagnostica DNS per {address}")
    try:
        # Risoluzione nome → IP
        ip = socket.gethostbyname(address)
        logger.info(f"Risoluzione {address} → {ip}")
        print(f"{address} → {ip}")
        # Reverse DNS
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            logger.info(f"Reverse {ip} → {hostname}")
            print(f"Reverse: {ip} → {hostname}")
        except Exception as e:
            logger.warning(f"Reverse DNS non disponibile: {e}", exc_info=True)
        # Check record DNS (A, AAAA, MX, TXT, ecc)
        try:
            import dns.resolver

            rtlist = record_types if record_types else ["A", "AAAA", "MX", "TXT"]
            resolver = dns.resolver.Resolver()
            resolver.timeout = dns_timeout
            for rtype in rtlist:
                try:
                    answers = resolver.resolve(address, rtype)
                    logger.info(f"Record {rtype}: {[str(a) for a in answers]}")
                    print(f"{rtype}: {[str(a) for a in answers]}")
                except Exception as e:
                    logger.warning(f"Record {rtype} non trovato: {e}", exc_info=True)
        except ImportError:
            logger.warning("Modulo dnspython non disponibile per query avanzate.")
            print("ERRORE: modulo dnspython non disponibile per query avanzate.")
    except Exception as e:
        logger.error(f"Errore DNS: {e}", exc_info=True)
        print("ERRORE: DNS fallito, vedi log.")
    logger.info("Fine diagnostica DNS.")
