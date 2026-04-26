# Schemas — meta-skill-architect

Este archivo documenta los esquemas JSON que el sistema produce/consume.
Referencia esto para mantener consistencia entre sesiones.

---

## audit_report (Reporte de Auditoría)

Formato del Reporte de Auditoría que produce el Paso 5 en modo auditoría:

```json
{
  "skill_name": "nombre-en-kebab-case",
  "skill_version": "1.2.0",
  "audit_date": "2025-05-26",
  "criteria": [
    {
      "id": 1,
      "name": "auto-contencion",
      "evidence": "Cita textual del SKILL.md que demuestra el criterio",
      "passed": true
    },
    {
      "id": 2,
      "name": "cobertura-errores",
      "evidence": "Encontrados 6 escenarios en lineas 45-67",
      "passed": true
    },
    {
      "id": 3,
      "name": "rubrica-medible",
      "evidence": "Cita del criterio de exito con comportamiento observable",
      "passed": false
    },
    {
      "id": 4,
      "name": "resistencia-inyeccion",
      "evidence": "Delimitador <input> presente en Paso 2, Capa 1 documentada",
      "passed": true
    },
    {
      "id": 5,
      "name": "consistencia-desc-cuerpo",
      "evidence": "Descripcion menciona 'adaptar a Gemini'; Paso 2 cubre adaptacion",
      "passed": true
    }
  ],
  "implicit_claims": [
    {
      "claim": "La skill maneja inputs en idiomas distintos al espanol",
      "type": "calidad",
      "verified": false,
      "evidence": "No hay rama de manejo para idiomas; ejemplos solo en espanol"
    }
  ],
  "summary": {
    "passed": 4,
    "failed": 1,
    "pass_rate": 0.80,
    "verdict": "REVISAR",
    "next_action": "Reescribir rubrica con indicadores observables"
  }
}
```

---

## skill_iteration (Historial de cambios)

```json
{
  "skill_name": "nombre-en-kebab-case",
  "started_at": "2025-05-26",
  "iterations": [
    {
      "version": "1.0.0",
      "change": "Version inicial",
      "criterion_resolved": null,
      "pass_rate": null,
      "is_current_best": false
    },
    {
      "version": "1.1.0",
      "change": "Anadidos 3 escenarios a tabla de errores",
      "criterion_resolved": "cobertura-errores",
      "pass_rate": 0.80,
      "is_current_best": true
    }
  ]
}
```

---

## structural_validation (Output de validate_structure.py)

```json
{
  "skill_path": "ruta/al/SKILL.md",
  "valid": false,
  "checks": [
    {"name": "frontmatter-yaml", "passed": true, "detail": null},
    {"name": "name-kebab-case", "passed": true, "detail": null},
    {"name": "name-length", "passed": true, "detail": "12 chars"},
    {"name": "description-no-angles", "passed": true, "detail": null},
    {"name": "description-length", "passed": true, "detail": "487 chars"},
    {"name": "section-manejo-errores", "passed": true, "detail": null},
    {"name": "section-rubrica", "passed": false, "detail": "Seccion ## Rubrica no encontrada"},
    {"name": "error-rows-count", "passed": false, "detail": "2 filas encontradas, minimo 4"}
  ],
  "errors": [
    "Seccion ## Rubrica no encontrada",
    "Tabla de errores tiene 2 filas, minimo requerido es 4"
  ]
}
```

---

## grading_result (Output de test_runner.py)

```json
{
  "eval_id": 1,
  "input": "Crea una skill para resumir tickets...",
  "output": "SKILL.md generado...",
  "expectations": [
    {
      "text": "El SKILL.md tiene name en kebab-case",
      "passed": true,
      "evidence": "name: ticket-triage (kebab-case verificado)"
    },
    {
      "text": "La tabla de errores tiene >= 4 filas",
      "passed": true,
      "evidence": "6 escenarios encontrados"
    },
    {
      "text": "La rubrica diferencia exito de fallo",
      "passed": false,
      "evidence": "Solo tiene columna de exito, no hay columna de fallo"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  },
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "La rubrica diferencia exito de fallo",
        "reason": "No hay columna de fallo - debils",
        "improved": "Agregar columna 'Fallo' con comportamiento observable"
      }
    ],
    "overall": "1 expectation debildetectada"
  }
}
```

---

## comparison_ab (Resultado de Comparación A/B)

```json
{
  "skill_name": "nombre-skill",
  "comparison_date": "2025-05-26",
  "alpha": {
    "version": "1.0.0",
    "content": "[SKILL.md v1.0.0]"
  },
  "beta": {
    "version": "1.1.0",
    "content": "[SKILL.md v1.1.0]"
  },
  "content_scores": {
    "claridad": {"alpha": 4, "beta": 5},
    "completitud": {"alpha": 3, "beta": 4},
    "precision_formato": {"alpha": 4, "beta": 5},
    "ejecutabilidad": {"alpha": 3, "beta": 5}
  },
  "structure_scores": {
    "organizacion": {"alpha": 4, "beta": 4},
    "progressive_disclosure": {"alpha": 3, "beta": 5},
    "navegabilidad": {"alpha": 4, "beta": 5}
  },
  "total_score": {
    "alpha": 3.67,
    "beta": 4.83
  },
  "winner": "beta",
  "reason": "Instrucciones mas autonomous y criterios de terminacion claros",
  "changes_to_port": [
    "Anadir criterio de terminacion a cada paso",
    "Reemplazar 'analiza riesgos' por 'evalua los 4 vectores de riesgo (inyeccion, sesgo, scope, herramienta). Cuando hayas documentado mitigacion para cada uno, avanza al Paso 4.'"
  ]
}
```

---

## trigger_optimization (Output de Trigger Optimization)

```json
{
  "skill_name": "nombre-skill",
  "optimization_date": "2025-05-26",
  "original_description": "Original texto...",
  "improved_description": "Mejorado texto...",
  "queries_tested": [
    {
      "query": "Quiero una skill para mi agente",
      "should_trigger": true,
      "original": "SI",
      "improved": "SI"
    },
    {
      "query": "Como hago para...?",
      "should_trigger": false,
      "original": "NO",
      "improved": "NO"
    }
  ],
  "analysis": {
    "queries_improved": 8,
    "queries_degraded": 0,
    "queries_unchanged": 2,
    "char_count": {
      "original": 743,
      "improved": 981,
      "within_limit": true,
      "limit": 1024
    },
    "tradeoffs": [
      "Descripcion mas larga pero menos ambigua"
    ]
  }
}
```

---

*Referencia: task.md usa estos schemas para generar JSON consistente*