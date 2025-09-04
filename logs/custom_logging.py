# logs/logging.py - Logging avanzato con livelli, rollover, configurazione da .ini.
"""
Gestione logging centralizzata:
- Log su file e stdout
- Livelli: INFO, WARNING, ERROR, CRITICAL
- Rollover automatico (dimensione e giorni)
- Configurazione da file .ini (path, livelli, formato)
- API semplice: info(), warning(), error(), critical()
"""

import logging
import logging.handlers
import os


class LogManager:
    def __init__(self, config):
        log_path = config.get("logging", "file", fallback="logs/network_diag.log")
        log_level = config.get("logging", "level", fallback="INFO").upper()
        max_bytes = config.getint(
            "logging", "max_bytes", fallback=5 * 1024 * 1024
        )  # 5MB
        backup_count = config.getint("logging", "backup_count", fallback=5)

        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        self.logger = logging.getLogger("network_diag_tool")
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))

        # Rollover per dimensione
        handler = logging.handlers.RotatingFileHandler(
            log_path, maxBytes=max_bytes, backupCount=backup_count
        )
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Log su stdout
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, exc_info=False):
        self.logger.error(msg, exc_info=exc_info)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
