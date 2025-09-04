# network/stats.py - Statistiche di rete (psutil, sicurezza).
"""
Modulo di diagnostica statistiche di rete sicuro e robusto.
- Statistiche per interfaccia (bytes, pacchetti, errori, drop)
- Logging dettagliato per auditing
- Gestione errori granulare
"""

from logs.custom_logging import LogManager

try:
    import psutil
except ImportError:
    psutil = None


def run_stats_diag(logger: LogManager):
    """
    Raccoglie statistiche di rete:
    - Per interfaccia
    - Log di ogni passo
    """
    logger.info("Raccolta statistiche di rete (psutil).")
    if psutil:
        try:
            net_io = psutil.net_io_counters(pernic=True)
            for iface, data in net_io.items():
                logger.info(
                    f"Interface: {iface} | Bytes sent: {data.bytes_sent} | Bytes recv: {data.bytes_recv} | Packets sent: {data.packets_sent} | Packets recv: {data.packets_recv}"
                )
                print(
                    f"{iface}: Bytes sent={data.bytes_sent}, recv={data.bytes_recv}, Packets sent={data.packets_sent}, recv={data.packets_recv}, Err in/out={data.errin}/{data.errout}, Drop in/out={data.dropin}/{data.dropout}"
                )
        except Exception as e:
            logger.error(f"Errore stats psutil: {e}", exc_info=True)
            print("ERRORE: Statistiche di rete fallite.")
    else:
        logger.error("Modulo psutil non disponibile.")
        print("ERRORE: modulo psutil non disponibile.")
