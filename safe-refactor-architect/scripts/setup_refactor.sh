#!/bin/bash
# setup_refactor.sh - Prepara el entorno para la refactorización segura.

DEST_DIR=$1

if [ -z "$DEST_DIR" ]; then
    echo "Uso: ./setup_refactor.sh <ruta_destino>"
    exit 1
fi

echo "Iniciando preparación de entorno en: $DEST_DIR"

# Crear directorio si no existe
mkdir -p "$DEST_DIR"

# Verificar permisos de escritura
if [ -w "$DEST_DIR" ]; then
    echo "✓ Directorio destino listo y escribible."
else
    echo "✗ ERROR: No hay permisos de escritura en $DEST_DIR"
    exit 1
fi

echo "Entorno preparado para Safe Refactor Architect."
exit 0
