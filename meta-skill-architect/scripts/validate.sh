#!/bin/bash
# validate.sh - Static validation for prompt_v22 skill outputs
# Usage: ./scripts/validate.sh "model_output_text"
# Exit codes: 0=OK, 1=REJECT (SOSPECHOSO), 2=WARN (PENDIENTE)

OUTPUT="$1"

if [ -z "$OUTPUT" ]; then
    echo "[ERROR] No output provided for validation."
    exit 1
fi

echo "Running static validation..."

# 1. Injection Detection (Hard stop)
if echo "$OUTPUT" | grep -qi "SOSPECHOSO"; then
    echo "[REJECT] Model detected and flagged a prompt injection attempt."
    exit 1
fi

# 2. Orphaned Placeholders
if echo "$OUTPUT" | grep -q "\[PENDIENTE:"; then
    echo "[WARN] Unresolved placeholders detected. Agent requested more context."
    exit 2
fi

# 3. Check for empty output
if [ -z "$(echo "$OUTPUT" | tr -d '[:space:]')" ]; then
    echo "[WARN] Empty output received."
    exit 2
fi

echo "[OK] Static validation passed."
exit 0