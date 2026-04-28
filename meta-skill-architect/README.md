# meta-skill-architect

Sistema de ingeniería de prompts para diseñar, auditar y mejorar skills SKILL.md para agentes de IA.

| Versión | 4.0.0 |
|--------|--------|
| Estado | ACTIVO |
| Runtimes | Claude, Gemini, GPT, Opencode, Kilocode |

---

## Overview

meta-skill-architect es un **arquitecto autónomo de skills** que genera, audita y mejora skills siguiendo el estándar SKILL.md. Funciona en cualquier interfaz de chat compatible con prompts, sin requerir Claude Code.

### Qué hace

- Diseña skills nuevas desde cero
- Audita skills existentes con reporte estructurado
- Mejora skills iterativamente con análisis post-modificación
- Adapta skills a plataformas específicas (Claude, Gemini, GPT, Opencode, Kilocode)
- Diagnostica vulnerabilidades (inyección de prompt, scope creep)
- Genera recursos asociados (references, scripts, assets) mediante enriquecimiento estructural
- Ejecuta autoevaluación y ciclo de automejoramiento
- Migra prompts informales al estándar SKILL.md
- Genera evals y compara versiones A/B

---

## Componentes

### Archivos principales

| Archivo | Propósito |
|---------|-----------|
| `system.md` | Identidad, reglas invariantes, constraints MoSCoW, arquitectura de defensa en capas (v4.0.0) |
| `task.md` | Instrucciones operativas, ciclo de 5 pasos, protocolos avanzados, plantillas (v4.0.0) |
| `SKILL.md` | Skill instalable (carga system.md + task.md, v4.0.0) |

### Scripts

| Script | Descripción |
|--------|-------------|
| `scripts/validate.sh` | Validador de seguridad (Capa 2 de defensa) |
| `scripts/validate_structure.py` | Validador de estructura YAML (10+ checks: frontmatter, secciones obligatorias, tablas de errores) |
| `scripts/test_runner.py` | Suite de evaluación LLM-as-a-Judge usando evals de `data/examples.json` |
| `scripts/mcp_server.py` | Servidor MCP stub para integración (requiere implementar `execute_skill()` con LLM real) |
| `scripts/smoke_test.sh` | Smoke test rápido para validar la integridad de la skill |

> **Nota sobre `test_runner.py`:** En modo fallback (sin CLI de Claude Code disponible), los resultados de evaluación NO son confiables. Para evals reales, ejecuta desde Claude Code con `claude -p` disponible. Las evals cuantitativas requieren entorno Claude Code — no presentar como funcionalidad completa en entornos de chat.

### References

| Archivo | Descripción |
|---------|-------------|
| `references/schemas.md` | 6 esquemas JSON para reportes de auditoría, validación, evals, comparaciones A/B, trigger optimization e iteraciones |
| `references/writing-patterns.md` | 7 patrones de escritura robusta para instrucciones autónomas y verificables |
| `references/examples.md` | 7 ejemplos canónicos de ciclos completos, auditorías, comparaciones A/B y optimización de triggers |

### Data

| Archivo | Descripción |
|---------|-------------|
| `data/examples.json` | 8 evals con 28 expectations para validar skills generadas |
| `data/knowledge-log.md` | Registro de patrones de fallo, soluciones y anti-patrones detectados |
| `data/validate_fixtures/` | 5 fixtures de prueba para el validador estructural |

### Assets

| Archivo | Descripción |
|---------|-------------|
| `assets/template-full.md` | Plantilla completa (>4000 tokens) para skills con múltiples pasos o referencias |
| `assets/template-minimal.md` | Plantilla mínima (<4000 tokens) para skills simples o plataformas con contexto limitado (Kilocode/Opencode) |

---

## Uso

### Instalar

```bash
npx skills add ASamiraJasbonM/Skills-learning --skill meta-skill-architect
```

### Modo interactivo (Claude/Gemini/OpenCode)

```markdown
Carga @system.md @task.md en el contexto del modelo.
El modelo ejecutará el ciclo de 5 pasos automáticamente.
```

### Validación estructura

```bash
python meta-skill-architect/scripts/validate_structure.py skill/SKILL.md
python meta-skill-architect/scripts/validate_structure.py skill/SKILL.md --json
```

### Smoke test

```bash
bash meta-skill-architect/scripts/smoke_test.sh
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
└── SKILL.md
```

### Estructura completa — carpetas separadas

Usar cuando:
- `references/`: documentación de API, schemas o guías >5000 palabras
- `scripts/`: tareas determinísticas y repetibles (validación, formateo)
- `assets/`: plantillas de output, templates JSON, imágenes
- `data/`: conjuntos de evaluación, fixtures de prueba

El protocolo S1 (Enriquecimiento Estructural) genera estos recursos automáticamente si la skill lo requiere.

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

### Modificación iterativa
```
Punto de entrada → Riesgos → Validación → Mejoras → Historial de cambios
```

### Auditoría
```
Punto de entrada → Reporte estructurado (5 criterios formales + claims implícitos)
```

### Iteración (≥2)
```
Análisis post-modificación → Comparación A/B → Trigger Optimization
```

### Autoevaluación (S6)
```
Carga SKILL.md → Validación (Paso 5) → Análisis de ejecutabilidad → Reporte de cumplimiento
```

### Automejoramiento (S7)
```
Diagnóstico → Cambio quirúrgico → Aprobación → SKILL.md actualizado + Historial
```

### Migración (S9)
```
Lectura de archivo no estándar → Mapeo a SKILL.md → Validación → Reporte de supuestos
```

### Generación de Evals (S10)
```
Lectura de rúbrica/errores/riesgos → Generación de 4-8 evals → Metacrítica de expectations
```

---

## Protocolos avanzados (v4.0.0)

### S1: Enriquecimiento Estructural
Diagnostica necesidades de recursos (references, scripts, assets) y los genera automáticamente tras el Paso 4 (Artefacto) si la skill lo requiere.

### Protocolo de Generalización
Diagnostica problemas antes de modificar:
- Instrucción ambigua → reubicar
- Instrucciones compiten → eliminar contradicción
- Overfitting → generalizar principio
- 2 fallos → cambio de metáfora

### Análisis de Ejecutabilidad
4 preguntas para cada instrucción:
1. ¿Es autónoma?
2. ¿Existe criterio de terminación?
3. ¿Hay instrucciones que compiten?
4. ¿Son demasiado específicas (narrow)?

### Comparación A/B (sin ejecución)
Evalúa Alpha vs Beta con rúbrica ciega de contenido y estructura, calcula score ponderado y declara ganadora.

### Trigger Optimization (Optimización de Descripción)
Genera 10 queries de prueba (5 que deben disparar, 5 que no), evalúa la descripción actual y reescribe para maximizar activación correcta.

### Metacrítica de Expectations
Detecta expectations débiles (triviales o no discriminantes) y las fortalece con thresholds cuantificables.

### S3: Catálogo de Scripts por Dominio
Evalúa si la skill requiere scripts típicos (validación, procesamiento, API, reportes) y genera esqueletos con docstring y argparse.

### S4: Generación de Plantillas
Genera `assets/template.[ext]` con placeholders `{{ campo }}` para outputs de estructura fija.

### S6: Autoevaluación
La skill audita su propio SKILL.md contra los 5 criterios formales y propone correcciones.

### S7: Ciclo de Automejoramiento
Tras autoevaluación, propone cambios quirúrgicos (máximo 2 por ciclo) y solicita aprobación antes de aplicar.

### S8: Protocolo de Actualización de Estándar
Gestiona cambios en el formato SKILL.md: actualiza plantillas, validadores, ejemplos y registra en `data/knowledge-log.md`.

### S9: Modo Migración
Convierte prompts informales, Actions de GPT o configuraciones de Gemini al estándar SKILL.md.

### S12: Modo Suite de Skills
Diseña múltiples skills relacionadas con orquestación y recursos compartidos.

---

## Versiones

| Version | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2025-05-09 | Initial release (clasificación seguridad) |
| 2.3.0 | 2025-05-26 | Sugerencias originales implementadas |
| 2.4.0 | 2025-05-26 | Mejoras v2.4.0 (scripts, auditoría) |
| 3.0.0 | 2026-04-26 | Mejoras v3.0.0 (protocolos avanzados, post-evaluación senior) |
| 4.0.0 | 2026-04-27 | Editor estructural completo: enriquecimiento (S1), autoevaluación (S6), migración (S9), evals (S10), knowledge log, suite de skills (S12) |

---

## Comparación con skill-creator

| Aspecto | skill-creator | meta-skill-architect v4.0.0 |
|---------|--------------|-------------------|
| Requiere Claude Code | ✅ | ❌ (funciona en chat) |
| Patrones escritura | Implícitos | **Explícitos (7)** |
| Comparación A/B | Subagentes | **Inline** |
| Trigger optimization | run_loop.py | **Razonamiento sin ejecución** |
| Multiplataforma | ❌ | **5 runtimes** |
| Enriquecimiento estructural | ❌ | **S1 automático** |
| Autoevaluación | ❌ | **S6 integrado** |

---

## Estructura completa

```
meta-skill-architect/
├── SKILL.md                   # Instalable (v4.0.0)
├── system.md                 # Identidad y reglas invariantes (v4.0.0)
├── task.md                   # Instrucciones operativas y protocolos (v4.0.0)
├── assets/
│   ├── template-full.md       # Plantilla completa
│   └── template-minimal.md  # Plantilla mínima
├── scripts/
│   ├── validate.sh          # Validador seguridad (Capa 2)
│   ├── validate_structure.py # Validador estructura YAML (10+ checks)
│   ├── test_runner.py        # Suite de evaluación LLM-as-a-Judge
│   ├── mcp_server.py        # Servidor MCP stub
│   └── smoke_test.sh        # Smoke test
├── data/
│   ├── examples.json        # 8 evals con 28 expectations
│   ├── knowledge-log.md     # Registro de patrones de fallo y soluciones
│   └── validate_fixtures/  # 5 fixtures para validación
│       ├── valid-full.md
│       ├── valid-minimal.md
│       ├── broken-frontmatter.md
│       ├── missing-rubrica.md
│       └── short-errors.md
├── references/
│   ├── schemas.md          # 6 esquemas JSON
│   ├── writing-patterns.md  # 7 patrones de escritura
│   └── examples.md         # 7 ejemplos canónicos
└── README.md
```

---

## Licencia

MIT
