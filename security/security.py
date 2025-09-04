# security/security.py - Validazione input, protezione da abusi, sanitizzazione.
"""
Security layer:
- Validazione IP e domini (regex robusta)
- Protezione da injection e abusi nei comandi
- API: validate_address(address)
"""

import re


def validate_address(address):
    # IP v4
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    # Dominio (semplificato)
    domain_pattern = (
    r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(?:\.[A-Za-z0-9-]{1,63}(?<!-))*"
    r"\.[A-Za-z]{2,}$"
    )   
    return bool(re.match(ip_pattern, address) or re.match(domain_pattern, address))

