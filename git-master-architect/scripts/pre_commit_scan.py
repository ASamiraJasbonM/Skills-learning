#!/usr/bin/env python3
"""
pre_commit_scan.py - Escáner de seguridad para el área de stage de Git.

Busca patrones de secretos (keys, tokens, .env) en los archivos que están
listos para ser commiteados.
"""

import subprocess
import sys
import re

# Patrones sospechosos
SECRET_PATTERNS = [
    r"SECRET_KEY", r"API_KEY", r"PASSWORD", r"TOKEN",
    r"BEGIN RSA PRIVATE KEY", r"xox[p|b|o|a]-[0-9]",
    r"AKIA[0-9A-Z]{16}" # AWS Access Key
]

FORBIDDEN_FILES = [".env", ".pem", ".key", "id_rsa"]

def get_staged_files():
    result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_all=True, text=True)
    return result.stdout.strip().split("\n")

def check_files():
    files = get_staged_files()
    if not files or files == ['']:
        return True

    found_issues = []
    for file in files:
        # Check filename
        if any(f in file for f in FORBIDDEN_FILES):
            found_issues.append(f"ARCHIVO PROHIBIDO: {file}")
            continue

        # Check content
        try:
            diff = subprocess.run(["git", "diff", "--cached", file], capture_all=True, text=True).stdout
            for pattern in SECRET_PATTERNS:
                if re.search(pattern, diff, re.IGNORECASE):
                    found_issues.append(f"PATRÓN SOSPECHOSO en {file}: {pattern}")
        except Exception:
            pass

    if found_issues:
        for issue in found_issues:
            print(f"✗ {issue}")
        return False
    return True

if __name__ == "__main__":
    if check_files():
        print("✓ Escaneo de seguridad completado: No se detectaron secretos.")
        sys.exit(0)
    else:
        print("! ERROR: Se detectaron posibles secretos en el stage.")
        sys.exit(1)
