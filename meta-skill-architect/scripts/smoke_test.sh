#!/bin/bash
# smoke_test.sh — verifica que validate_structure.py funciona correctamente
# Uso: ./scripts/smoke_test.sh

PASS=0
FAIL=0

echo "=== Smoke Test: validate_structure.py ==="

#should pass
for fixture in data/validate_fixtures/valid-*.md; do
    echo -n "Testing $fixture... "
    python scripts/validate_structure.py "$fixture" --quiet 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "PASS"
        ((PASS++))
    else
        echo "FAIL (should pass)"
        ((FAIL++))
    fi
done

#should fail
for fixture in data/validate_fixtures/broken-*.md data/validate_fixtures/missing-*.md data/validate_fixtures/short-*.md; do
    echo -n "Testing $fixture... "
    python scripts/validate_structure.py "$fixture" --quiet 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "PASS"
        ((PASS++))
    else
        echo "FAIL (should fail)"
        ((FAIL++))
    fi
done

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ $FAIL -eq 0 ] && exit 0 || exit 1