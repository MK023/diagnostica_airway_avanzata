# config/config_manager.py - Gestione file di configurazione (.ini), parametri globali.
"""
Carica e gestisce il file di configurazione .ini:
- Accesso a sezioni e parametri
- Supporto a fallback/default
- API semplice: get(), getint(), getboolean()
"""

import configparser
import os


class ConfigManager:
    def __init__(self, ini_path):
        self.config = configparser.ConfigParser()
        if not os.path.isfile(ini_path):
            raise FileNotFoundError(f"File di configurazione '{ini_path}' non trovato!")
        self.config.read(ini_path)

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def getint(self, section, key, fallback=None):
        return self.config.getint(section, key, fallback=fallback)

    def getboolean(self, section, key, fallback=None):
        return self.config.getboolean(section, key, fallback=fallback)
