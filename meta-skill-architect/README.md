# prompt_v22 — Meta-Skill Architect

Sistema de ingeniería de prompts para diseñar, auditar y mejorar skills SKILL.md para agentes de IA.

| Versión | 3.0.0 |
|--------|--------|
| Estado | ACTIVO |
| Runtimes | Claude, Gemini, GPT, Opencode, Kilocode |

---

## Overview

prompt_v22 es un **arquitecto autónomo de skills** que genera, audita y mejora skills siguiendo el estándar SKILL.md. A diferencia de skill-creator (que requiere Claude Code), prompt_v22 funciona en cualquier interfaz de chat compatible con prompts.

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

### Scripts

| Script | Descripción |
|--------|-------------|
| `scripts/validate.sh` | Validador seguridad (Capa 2) |
| `scripts/validate_structure.py` | Validador estructura YAML (8+ checks) |
| `scripts/test_runner.py` | Suite evaluación LLM-as-a-Judge (grading.json) |
| `scripts/mcp_server.py` | Servidor MCP para integración |

### References

| Archivo | Descripción |
|---------|-------------|
| `references/schemas.md` | 6 esquemas JSON para consistencia |
| `references/writing-patterns.md` | 7 patrones de escritura robusta |
| `references/examples.md` | 5 ejemplos canónicos |

### Data

| Archivo | Descripción |
|---------|-------------|
| `data/examples.json` | 8 evals con 28 expectations |

---

## Uso

### Modo interactivo (Claude/Gemini/OpenCode)

```markdown
Carga system.md + task.md en el contexto del modelo.
El modelo ejecutará el ciclo automáticamente.
```

### Validación estructura

```bash
python prompt_v22/scripts/validate_structure.py skill/SKILL.md
python prompt_v22/scripts/validate_structure.py skill/SKILL.md --json
```

### Suite de evaluación

```bash
python prompt_v22/scripts/test_runner.py --data data/examples.json
python prompt_v22/scripts/test_runner.py --json
```

### Servidor MCP

```bash
python prompt_v22/scripts/mcp_server.py
```

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

## Protocolos avanzados

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
| 3.0.0 | 2025-05-26 | Mejoras v3.0.0 (protocolos avanzados) |

---

## Comparación con skill-creator

| Aspecto | skill-creator | prompt_v22 v3.0.0 |
|---------|--------------|-------------------|
| Requiere Claude Code | ✅ | ❌ (funciona en chat) |
| Patrones escritura | Implícitos | **Explícitos (7)** |
| Comparación A/B | Subagentes | **Inline** |
| Trigger optimization | run_loop.py | **Razonamiento** |
| Multiplataforma | ❌ | **5 runtimes** |

---

## Estructura

```
prompt_v22/
├── system.md                 # v3.0.0
├── task.md                   # v3.0.0
├── scripts/
│   ├── validate.sh          
│   ├── validate_structure.py # v2
│   ├── test_runner.py        # v2
│   └── mcp_server.py       
├── data/
│   └── examples.json        # 8 evals
├── references/
│   ├── schemas.md          # 6 schemas
│   ├── writing-patterns.md  # 7 patrones
│   └── examples.md         
└── README.md
```

---

## Licencia

See `LICENSE.txt` in parent directory.