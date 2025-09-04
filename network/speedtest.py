# network/speedtest.py - Diagnostica Speedtest (banda, ping, sicurezza).
"""
Modulo di diagnostica Speedtest sicuro e robusto.
- Download, upload, ping
- Logging dettagliato per auditing
- Limitazione richieste (no flood)
- Gestione errori granulare
"""

from logs.logging import LogManager

try:
    import speedtest
except ImportError:
    speedtest = None

def run_speedtest_diag(logger: LogManager, max_attempts=2):
    """
    Esegue speedtest diagnostico:
    - Limita tentativi per evitare abusi
    - Log di ogni passo
    """
    logger.info("Avvio speedtest diagnostico.")
    if speedtest:
        attempt = 0
        while attempt < max_attempts:
            try:
                st = speedtest.Speedtest()
                st.get_best_server()
                results = {
                    "download_bps": round(st.download(), 2),
                    "upload_bps": round(st.upload(), 2),
                    "ping_ms": round(st.results.ping, 2)
                }
                logger.info(f"Speedtest: {results}")
                print(f"Download: {results['download_bps'] / 1e6:.2f} Mbps")
                print(f"Upload:   {results['upload_bps'] / 1e6:.2f} Mbps")
                print(f"Ping:     {results['ping_ms']} ms")
                break
            except Exception as e:
                logger.error(f"Errore speedtest: {e}", exc_info=True)
                attempt += 1
                print(f"ERRORE: Speedtest fallito (tentativo {attempt}).")
        if attempt == max_attempts:
            logger.error("Speedtest non riuscito dopo tentativi massimi.")
            print("ERRORE: Speedtest non riuscito.")
    else:
        logger.error("Modulo speedtest non disponibile.")
        print("ERRORE: modulo speedtest non disponibile.")
    logger.info("Fine diagnostica speedtest.")