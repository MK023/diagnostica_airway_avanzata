# os_manager/os_manager.py - Rilevamento OS, gestione permessi e funzioni specifiche.
"""
Gestione OS:
- Rileva Windows, Linux, macOS
- Richiede permessi amministrativi dove necessario
- API: detect_os(), require_admin_if_needed()
"""

import os
import platform
import sys


class OSManager:
    def __init__(self, logger):
        self.logger = logger

    def detect_os(self):
        sysname = platform.system().lower()
        if "windows" in sysname:
            return "windows"
        elif "linux" in sysname:
            return "linux"
        elif "darwin" in sysname or "mac" in sysname:
            return "macos"
        else:
            self.logger.warning("OS non riconosciuto, default: linux")
            return "linux"

    def require_admin_if_needed(self):
        os_type = self.detect_os()
        if os_type == "windows":
            try:
                import ctypes

                if not ctypes.windll.shell32.IsUserAnAdmin():
                    self.logger.critical("Esegui il programma come Amministratore!")
                    print("Esegui come Amministratore!")
                    sys.exit(99)
            except Exception:
                self.logger.critical(
                    "Impossibile verificare permessi amministratore su Windows."
                )
                sys.exit(99)
        elif os_type in ["linux", "macos"]:
            if hasattr(os, "geteuid") and os.geteuid() != 0:
                self.logger.critical("Esegui il programma come root (sudo)!")
                print("Esegui come root (sudo)!")
                sys.exit(99)
