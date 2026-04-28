#!/usr/bin/env python3
"""
validate_integrity.py - Verifica la integridad del código post-refactorización.

Compara el código extraído hacia los nuevos módulos con el fragmento original
para asegurar que no hubo pérdida de lógica, comentarios o variables.
"""

import argparse
import sys
from pathlib import Path

def compare_logic(original_snippet: str, refactored_code: str) -> bool:
    # Eliminar espacios en blanco extremos para comparación base
    orig = "".join(original_snippet.split())
    refac = "".join(refactored_code.split())
    return orig == refac

def main():
    parser = argparse.ArgumentParser(description="Validador de integridad para refactorizaciones.")
    parser.add_argument("--original", type=Path, required=True, help="Archivo con el snippet original.")
    parser.add_argument("--target", type=Path, required=True, help="Archivo refactorizado de destino.")
    
    args = parser.parse_args()
    
    if not args.original.exists() or not args.target.exists():
        print("ERROR: Uno de los archivos no existe.")
        sys.exit(1)
        
    orig_content = args.original.read_text()
    target_content = args.target.read_text()
    
    if compare_logic(orig_content, target_content):
        print("✓ INTEGRIDAD VERIFICADA: La lógica coincide 1:1.")
        sys.exit(0)
    else:
        print("✗ ERROR DE INTEGRIDAD: Se detectaron discrepancias en la lógica.")
        sys.exit(1)

if __name__ == "__main__":
    main()
