# Skill Creator - Documentación

Skill Creator es una herramienta para crear, mejorar y medir el rendimiento de skills (habilidades) en Claude Code.

---

## Estructura del Proyecto

```
skill-creator/
├── SKILL.md                          # Instrucciones principales del skill
├── LICENSE.txt                      # Licencia
├── scripts/                         # Scripts Python para automatización
│   ├── __init__.py
│   ├── utils.py                     # Utilidades compartidas
│   ├── run_loop.py                  # Loop de optimización de descripciones
│   ├── run_eval.py                  # Evaluación de triggers de skills
│   ├── improve_description.py      # Mejora de descripciones con IA
│   ├── quick_validate.py            # Validación rápida de skills
│   ├── generate_report.py           # Generación de reportes HTML
│   └── aggregate_benchmark.py       # Agregación de resultados de benchmark
├── agents/                          # Instrucciones para subagentes
│   ├── grader.md                    # Agente evaluador de expectativas
│   ├── comparator.md                # Agente comparador ciego A/B
│   └── analyzer.md                  # Agente analizador de resultados
├── eval-viewer/                     # Visor de evaluaciones
│   ├── viewer.html                  # Template HTML del visor
│   └── generate_review.py          # Generador del visor de evaluaciones
├── references/                      # Documentación de referencia
│   └── schemas.md                   # Esquemas JSON para estructuras de datos
└── assets/                          # Recursos adicionales
    └── eval_review.html             # Template para review de evaluaciones
```

---

## Scripts Principales

### 1. `run_eval.py`
**Función:** Evalúa si la descripción de un skill hace que Claude active (lea) el skill para un conjunto de queries.

**Uso:**
```bash
python -m scripts.run_eval --eval-set <archivo.json> --skill-path <ruta> --model <modelo>
```

**Características:**
- Crea archivos de comando temporales en `.claude/commands/`
- Ejecuta `claude -p` para probar cada query
- Detecta triggers mediante stream events
- Soporta múltiples ejecuciones por query para mayor reliability
- Retorna JSON con tasas de trigger y resultados

---

### 2. `run_loop.py`
**Función:** Combina `run_eval.py` e `improve_description.py` en un loop iterativo para optimizar automáticamente la descripción de un skill.

**Uso:**
```bash
python -m scripts.run_loop \
  --eval-set <archivo.json> \
  --skill-path <ruta> \
  --model <modelo> \
  --max-iterations 5 \
  --holdout 0.4
```

**Características:**
- Divide el eval set en train (60%) y test (40%)
- Itera hasta `max_iterations` o hasta que todos los queries pasen
- Genera reportes HTML en vivo con auto-refresh
- Selecciona la mejor descripción por puntuación de test (evita overfitting)
- Retorna JSON con `best_description` y historial completo

---

### 3. `improve_description.py`
**Función:** Solicita a Claude que mejore una descripción basándose en los resultados de evaluación.

**Uso:**
```bash
python -m scripts.improve_description \
  --eval-results <resultados.json> \
  --skill-path <ruta> \
  --model <modelo>
```

**Características:**
- Analiza queries que fallaron en trigger y falsos triggers
- Considera historial de intentos previos para evitar repeticiones
- Limita la descripción a 1024 caracteres (requisito del sistema)
- Registra transcripciones en `log_dir` para debugging
- Soporta reescritura automática si excede el límite

---

### 4. `quick_validate.py`
**Función:** Validación rápida de la estructura de un skill antes de empaquetarlo.

**Uso:**
```bash
python -m scripts.quick_validate <directorio-skill>
```

**Validaciones:**
- Existencia de `SKILL.md`
- Formato YAML frontmatter válido
- Propiedades permitidas en frontmatter
- Campo `name` en kebab-case (máx. 64 caracteres)
- Campo `description` sin ángulos brackets (máx. 1024 caracteres)
- Campo `compatibility` válido (opcional, máx. 500 caracteres)

---

### 5. `package_skill.py`
**Función:** Empaqueta una carpeta de skill en un archivo `.skill` (formato ZIP) para distribución.

**Uso:**
```bash
python -m scripts.package_skill <directorio-skill> [directorio-salida]
```

**Características:**
- Valida el skill antes de empaquetar
- Excluye directorios como `evals/`, `__pycache__`, `node_modules`
- Excluye archivos como `.DS_Store`, `*.pyc`
- Genera archivo `.skill` (ZIP con extensión renombrada)

---

### 6. `aggregate_benchmark.py`
**Función:** Agrega resultados individuales de ejecuciones en estadísticas de benchmark.

**Uso:**
```bash
python -m scripts.aggregate_benchmark <directorio-benchmark> --skill-name <nombre>
```

**Genera:**
- `benchmark.json` con estadísticas agregadas (mean, stddev, min, max)
- `benchmark.md` con resumen legible
- Calcula delta entre configuraciones (with_skill vs without_skill)

**Estadísticas:**
- Pass rate (porcentaje de expectativas cumplidas)
- Time (segundos de ejecución)
- Tokens (uso de tokens)
- Tool calls (llamadas a herramientas)

---

### 7. `generate_report.py`
**Función:** Genera un reporte HTML visual desde la salida JSON de `run_loop.py`.

**Uso:**
```bash
python -m scripts.generate_report <input.json> -o <output.html>
```

**Características:**
- Muestra tabla con iteraciones y resultados por query
- Distingue entre queries de train (verde) y test (azul)
- Resalta la mejor iteración
- Incluye auto-refresh opcional

---

### 8. `eval-viewer/generate_review.py`
**Función:** Genera y sirve una página web interactiva para que usuarios revisen outputs de evaluaciones.

**Uso:**
```bash
python eval-viewer/generate_review.py <workspace> --skill-name <nombre>
```

**Características:**
- Servidor HTTP integrado (puerto 3117 por defecto)
- Dos pestañas: "Outputs" y "Benchmark"
- Navegación entre runs con prev/next
- Auto-guardado de feedback en `feedback.json`
- Soporta modo estático (`--static`) para entornos sin display
- Muestra outputs anteriores para comparación iterativa

---

## Subagentes (agents/)

### `grader.md`
Evalúa expectativas contra transcript y outputs. Genera `grading.json` con:
- Resultado de cada expectativa (pass/fail con evidencia)
- Métricas de ejecución (tool calls, pasos, errores)
- Claims extraídos y verificados
- Feedback sobre la calidad de las evals

### `comparator.md`
Compara dos outputs sin saber cuál skill los produjo (blind A/B). Genera `comparison.json` con:
- Ganador (A, B, o TIE)
- Rubrica de evaluación (content + structure)
- Fortalezas y debilidades de cada output
- Resultados de expectativas (si se proporcionan)

### `analyzer.md`
Analiza resultados de benchmark para identificar patrones. Genera notas como:
- Expectations que siempre pasan/fallan
- Alta varianza en ejecuciones
- Delta en métricas entre configuraciones

---

## Referencias (references/)

### `schemas.md`
Define los esquemas JSON para todas las estructuras de datos:

| Archivo | Propósito |
|---------|-----------|
| `evals.json` | Definición de evaluaciones para un skill |
| `history.json` | Seguimiento de versiones durante mejora |
| `grading.json` | Resultado de evaluar expectativas |
| `metrics.json` | Métricas de ejecución del executor |
| `timing.json` | Tiempos de ejecución |
| `benchmark.json` | Estadísticas agregadas de benchmark |
| `comparison.json` | Resultado de comparación ciega |
| `analysis.json` | Análisis post-hoc de comparaciones |

---

## Flujo de Trabajo Típico

```
1. Crear skill → Escribir SKILL.md con name y description
2. Probar → Crear eval queries y ejecutar run_eval.py
3. Revisar → Generar visor con generate_review.py
4. Iterar → Mejorar basándose en feedback del usuario
5. Optimizar → Ejecutar run_loop.py para optimizar description
6. Empaquetar → package_skill.py para distribución
```

---

## Notas de Implementación

- Todos los scripts usan solo bibliotecas estándar de Python (stdlib)
- Los scripts que llaman a Claude usan `claude -p` via subprocess
- El puerto por defecto para el visor es 3117
- Los archivos temporales se limpian automáticamente
- Los reportes HTML usan Google Fonts (Poppins, Lora)