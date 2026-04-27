# meta-skill-architect

Sistema de ingeniería de prompts para diseñar, auditar y mejorar skills SKILL.md para agentes de IA.

| Versión | 4.0.0 |
|--------|--------|
| Estado | ACTIVO |
| Runtimes | Claude, Gemini, GPT, Opencode, Kilocode |

---

## Overview

meta-skill-architect es un **arquitecto autónomo de skills** que genera, audita y mejoran skills siguiendo el estándar SKILL.md. Funciona en cualquier interfaz de chat compatible con prompts.

### Qué hace

- Diseña skills nuevas desde cero
- Audita skills existentes
- Mejora skills iterativamente
- Adapta skills a plataformas específicas
- Diagnostica vulnerabilidades en skills

---

## Componentes

### Archivos principales

| Archivo | Propósito |
|---------|-----------|
| `system.md` | Identidad y reglas invariantes (v3.0.0) |
| `task.md` | Instrucciones operativas + ciclos (v3.0.0) |
| `SKILL.md` | Skill instalable (carga system.md + task.md) |

### Scripts

| Script | Descripción |
|--------|-------------|
| `scripts/validate.sh` | Validador seguridad (Capa 2) |
| `scripts/validate_structure.py` | Validador estructura YAML (8+ checks) |
| `scripts/test_runner.py` | Suite evaluación LLM-as-a-Judge (grading.json) |
| `scripts/mcp_server.py` | Servidor MCP para integración |

> **Estado:** `mcp_server.py` es un stub de referencia. Para uso en producción,
> implementar `execute_skill()` con llamada real al LLM (ver comentarios en el archivo).
>
> **Nota sobre `test_runner.py`:** En modo fallback (sin CLI de Claude Code disponible),
> los resultados de evaluación NO son confiables. Para evals reales, ejecuta desde
> Claude Code con `claude -p` disponible. Las evals cuantitativas requieren entorno
> Claude Code — no presentar como funcionalidad completa en entornos de chat.

### References

| Archivo | Descripción |
|---------|-------------|
| `references/schemas.md` | 6 esquemas JSON para consistencia |
| `references/writing-patterns.md` | 7 patrones de escritura robusta |
| `references/examples.md` | 7 ejemplos canónicos |

### Data

| Archivo | Descripción |
|---------|-------------|
| `data/examples.json` | 8 evals con 28 expectations |
| `data/validate_fixtures/` | 5 fixtures para testing del validador |
| `data/knowledge-log.md` | Registro de patrones de fallo, soluciones y anti-patrones |

### Assets

| Archivo | Descripción |
|---------|-------------|
| `assets/template-full.md` | Plantilla completa (>4000 tokens) |
| `assets/template-minimal.md` | Plantilla mínima (<4000 tokens) |

---

## Uso

### Instalar

```bash
npx skills add ASamiraJasbonM/Skills-learning --skill meta-skill-architect
```

### Modo interactivo (Claude/Gemini/OpenCode)

```markdown
Carga @system.md @task.md en el contexto del modelo.
El modelo ejecutará el ciclo automáticamente.
```

### Validación estructura

```bash
python meta-skill-architect/scripts/validate_structure.py skill/SKILL.md
python meta-skill-architect/scripts/validate_structure.py skill/SKILL.md --json
```

### Smoke test

```bash
python meta-skill-architect/scripts/smoke_test.sh
```

---

## Cuándo recomendar estructura mínima vs completa

### Estructura mínima — un solo SKILL.md

Usar cuando:
- La skill tiene ≤3 pasos en su flujo principal
- No hay documentación de referencia externa (APIs, schemas)
- El SKILL.md completo cabe en ≤5000 palabras
- La plataforma de destino es Kilocode u Opencode (contexto limitado)

Ejemplo:
```
my-skill/
├── SKILL.md
```

### Estructura completa — carpetas separadas

Usar cuando:
- `references/`: documentación de API, schemas o guías >5000 palabras
- `scripts/`: tareas determinísticas y repetibles (validación, formateo)
- `assets/`: plantillas de output, templates JSON, imágenes
- `data/`: conjuntos de evaluación, fixtures de prueba

Ejemplo:
```
my-skill/
├── SKILL.md
├── references/
│   └── api-docs.md
├── scripts/
│   └── validate.py
├── assets/
│   └── template.json
└── data/
    └── evals.json
```

### Regla de decisión rápida

- ¿El SKILL.md necesita cargar contexto externo bajo demanda? → estructura completa
- ¿Funciona autónomamente con un solo archivo? → estructura mínima

---

## Ciclos de operación

### Nueva skill
```
Punto de entrada → Intención → Ambigüedad → Riesgos → Artefacto → Validación
```

### Modificación
```
Punto de entrada → Riesgos → Validación → Mejoras → Historial
```

### Auditoría
```
Punto de entrada → Reporte estructurado (5 criterios)
```

### Iteración (≥2)
```
Análisis post-modificación → Comparación A/B → Trigger optimization
```

---

## Protocolos avanzada

### Protocolo de Generalización
Diagnostica problemas antes de modificar:
- Instructional ambigua → reubicar
- Instrucciones compiten → eliminar contradicción
- Overfitting → generalizar principio
- 2 fallos → cambio de metáfora

### Análisis de Ejecutabilidad
4 preguntas para cada instrucción:
1. ¿Es autónoma?
2. ¿Existe criterio de terminación?
3. ¿Hay instrucciones que compiten?
4. ¿Son demasiado narrow?

### Comparación A/B (sin ejecución)
Evalúa Alpha vs Beta con rúbrica Ciega.

### Trigger Optimization
Genera 10 queries de prueba y razona sobre triggering.

### Metacrítica de Expectations
Detecta expectations débiles (triviales o no discriminantes).

---

## Versiones

| Version | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2025-05-09 | Initial release (clasificación seguridad) |
| 2.3.0 | 2025-05-26 | Sugerencias originales implementadas |
| 2.4.0 | 2025-05-26 | Mejoras v2.4.0 (scripts, auditoría) |
| 3.0.0 | 2026-04-26 | Mejoras v3.0.0 (protocolos avanzados, post-evaluación senior) |
| 4.0.0 | 2026-04-27 | Editor estructural completo: enriquecimiento, autoevaluación, migración, evals, knowledge log |

---

## Comparación con skill-creator

| Aspecto | skill-creator | meta-skill-architect v3.0.0 |
|---------|--------------|-------------------|
| Requiere Claude Code | ✅ | ❌ (funciona en chat) |
| Patrones escritura | Implícitos | **Explícitos (7)** |
| Comparación A/B | Subagentes | **Inline** |
| Trigger optimization | run_loop.py | **Razonamiento** |
| Multiplataforma | ❌ | **5 runtimes** |

---

## Estructura

```
meta-skill-architect/
├── SKILL.md                   # Instalable
├── system.md                 # v3.0.0
├── task.md                   # v3.0.0
├── assets/
│   ├── template-full.md       # Plantilla completa
│   └── template-minimal.md  # Plantilla mínima
├── scripts/
│   ├── validate.sh          
│   ├── validate_structure.py # v2 (10 checks)
│   ├── test_runner.py        # v2
│   ├── mcp_server.py       
│   └── smoke_test.sh       # Smoke test
├── data/
│   ├── examples.json        # 8 evals
│   └── validate_fixtures/  # 5 fixtures
│       ├── valid-full.md
│       ├── valid-minimal.md
│       ├── broken-frontmatter.md
│       ├── missing-rubrica.md
│       └── short-errors.md
├── references/
│   ├── schemas.md          # 6 schemas
│   ├── writing-patterns.md  # 7 patrones
│   └── examples.md         # 7 ejemplos
└── README.md
```

---

## Licencia

MIT