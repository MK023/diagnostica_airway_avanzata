# main.py - Entrypoint principale del tool di diagnostica di rete e sicurezza.
"""
Gestisce il flusso principale:
- Carica configurazione da .ini
- Inizializza logging evoluto
- Rileva OS e permessi
- Mostra CLI per selezione azioni
- Chiama i moduli richiesti in base alla scelta utente
- Gestisce errori critici e logging a livello globale
"""
import sys

from cli.cli import CliMenu
from config.config_manager import ConfigManager
from logs.custom_logging import LogManager
from os_manager.os_manager import OSManager


def main():
    # Carica configurazione
    config = ConfigManager("config.ini")

    # Inizializza logging evoluto
    logger = LogManager(config)

    # Rileva OS e gestisce permessi/admin
    os_manager = OSManager(logger)
    os_type = os_manager.detect_os()
    os_manager.require_admin_if_needed()

    # Mostra CLI e gestisce scelta utente
    cli = CliMenu(config, logger, os_type)

    while True:
        try:
            action = cli.show_menu()
            if action == "ping":
                cli.run_ping()
            elif action == "traceroute":
                cli.run_traceroute()
            elif action == "speedtest":
                cli.run_speedtest()
            elif action == "network_stats":
                cli.run_network_stats()
            elif action == "dns_check":
                cli.run_dns_check()
            elif action == "advanced_diag":
                cli.run_advanced_diag()
            elif action == "exit":
                logger.info("Chiusura tool richiesta dall'utente.")
                print("Arrivederci!")
                break
            else:
                logger.warning(f"Azione non riconosciuta: {action}")
        except Exception:
            logger.error("Errore critico nel main loop.", exc_info=True)
            print("Errore critico! Vedi log per dettagli.")
            sys.exit(1)


if __name__ == "__main__":
    main()
