# cli/cli.py - Interfaccia Command Line (CLI) per la selezione e l'avvio delle azioni diagnostiche.
"""
Gestisce la user experience su terminale:
- Mostra il menu delle azioni disponibili (ping, traceroute, speedtest, stats, DNS, diagnosi avanzata, uscita)
- Valida l’input utente per sicurezza
- Chiama i moduli diagnostici specifici
- Integra logging e configurazione
"""

from network.ping import run_ping_diag
from network.traceroute import run_traceroute_diag
from network.speedtest import run_speedtest_diag
from network.stats import run_stats_diag
from network.dns import run_dns_diag
from security.security import validate_address
from logs.custom_logging import LogManager

class CliMenu:
    def __init__(self, config, logger: LogManager, os_type: str):
        self.config = config
        self.logger = logger
        self.os_type = os_type

    def show_menu(self):
        print("\n--- Tool Diagnostica Rete & Sicurezza ---")
        print("Seleziona un'azione:")
        print("1) Ping")
        print("2) Traceroute")
        print("3) Speedtest")
        print("4) Statistiche di rete")
        print("5) DNS Check")
        print("6) Diagnosi avanzata")
        print("7) Esci")
        choice = input("Inserisci il numero dell'azione: ").strip()
        mapping = {
            "1": "ping",
            "2": "traceroute",
            "3": "speedtest",
            "4": "network_stats",
            "5": "dns_check",
            "6": "advanced_diag",
            "7": "exit"
        }
        return mapping.get(choice, None)

    def get_target_address(self):
        address = input("Inserisci IP o dominio da diagnosticare: ").strip()
        if not validate_address(address):
            self.logger.error("Indirizzo non valido, riprovare.")
            print("ERRORE: Indirizzo non valido, riprovare.")
            return None
        return address

    def run_ping(self):
        addr = self.get_target_address()
        if addr:
            run_ping_diag(addr, self.logger, self.os_type)

    def run_traceroute(self):
        addr = self.get_target_address()
        if addr:
            run_traceroute_diag(addr, self.logger, self.os_type)

    def run_speedtest(self):
        run_speedtest_diag(self.logger)

    def run_network_stats(self):
        run_stats_diag(self.logger)

    def run_dns_check(self):
        addr = self.get_target_address()
        if addr:
            run_dns_diag(addr, self.logger)

    def run_advanced_diag(self):
        addr = self.get_target_address()
        if addr:
            # Parametri avanzati da config
            filename = self.config.get("diagnostics", "csvfile", fallback="diagnostics.csv")
            delay = self.config.getint("diagnostics", "delay", fallback=5)
            run_ping_diag(addr, self.logger, self.os_type, advanced=True, csvfile=filename, delay=delay)