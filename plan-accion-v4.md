# Plan de Acción — Correcciones meta-skill-architect v4.0.0

Basado en: `analisis-produccion-v4.md`

---

## 1. Corrección P1 (Alto) — Orden de pasos en auditoría+mejora

**Problema:** El flujo "audita y mejora" ejecuta Paso 5 → Paso 3. El orden correcto es Paso 3 → Paso 4 → Paso 5.

**Cambio en `task.md`:**
Actualizar la tabla de punto de entrada:
```markdown
| El usuario trae una skill existente | Ve directo al Paso 3 (Riesgos) → Paso 4 (Artefacto mejorado) → Paso 5 (Validación) |
| El usuario dice "audita esto" | Paso 5 (auditoría pura, solo reporte) |
| El usuario dice "mejora esto" tras auditoría | Paso 3 → Paso 4 → Paso 5 |
```

**Archivo a modificar:** `meta-skill-architect/task.md` (lineas ~22-29)

---

## 2. Corrección P2 (Medio) — Visibilidad del Protocolo S1

**Problema:** S1 se ejecuta implícitamente sin mostrar el árbol de salida al usuario.

**Cambio en `task.md`:**
Reemplazar la sección "3. Árbol de salida" en S1:
```markdown
### 3. Árbol de salida (SIEMPRE visible)

ANTES de generar archivos, presenta al usuario:
"Voy a generar/actualizar estos archivos:"
[árbol de directorios]
"¿Confirmas?"

Tras la confirmación, genera los archivos.
```

**Archivo a modificar:** `meta-skill-architect/task.md` (lineas ~192-204)

---

## 3. Corrección P3 (Medio) — Rúbrica de validación para código

**Problema:** La rúbrica evalúa el SKILL.md pero no verifica que el código de ejemplo implemente las mitigaciones.

**Cambio en `task.md`:**
Añadir criterio adicional al Paso 5:
```markdown
| Mitigación implementada | El código de ejemplo demuestra la mitigación, no solo la menciona | El riesgo está documentado pero no ejemplificado |
```

**Archivo a modificar:** `meta-skill-architect/task.md` (lineas ~121-131)

---

## 4. Corrección P4 (Bajo) — Historial de cambios simplificado

**Problema:** La regla tiene condiciones ambiguas que hacen que el agente no añada el historial en primera modificación.

**Cambio en `task.md`:**
Reemplazar la sección "Al modificar (ciclo iterativo)":
```markdown
**Al modificar (ciclo iterativo):**
SIEMPRE añade ## Historial de cambios al final del SKILL.md modificado.
- Si no existe la sección: creala con una fila para la versión actual
- Si existe: añade una fila con el cambio actual

Cada fila: qué cambió, qué criterio resuelve, fecha
```

**Archivo a modificar:** `meta-skill-architect/task.md` (lineas ~45-48)

---

## 5. Corrección P5 (Bajo) — Trigger del Knowledge Log

**Problema:** No hay trigger explícito para registrar patrones en knowledge-log.md.

**Cambio en `task.md`:**
Añadir sección nueva tras el Paso 5:
```markdown
## Trigger del Knowledge Log

Al terminar el Paso 5 de cualquier auditoría o modificación:
1. Evalúa si se descubrió un patrón no registrado en data/knowledge-log.md
2. Si sí → propón al usuario: "Encontré el patrón [X]. ¿Lo añado al knowledge-log?"
3. Si el usuario confirma → genera la fila y actualiza el archivo
```

**Archivo a modificar:** `meta-skill-architect/task.md` (añadir tras linea ~131)

---

## 6. Refactoring (Recomendado) — Reducir tamaño de task.md

**Problema:** task.md es demasiado grande (>500 líneas), violando las reglas que la skill valida.

**Cambio estructural:**
Mover protocolos avanzados a `references/`:
```
meta-skill-architect/
├── task.md              ← solo ciclo de 5 pasos + punto de entrada (≤200 líneas)
└── references/
    ├── protocols-advanced.md  ← S1, S3, S4, S6, S7, S8, S9, S10, S12
    └── protocols-core.md     ← Generalization, Executability, A/B, Trigger Opt, Metacritic
```

**Nota:** Este cambio es estructural y requiere crear archivos nuevos. Prioridad menor que P1-P5.

---

## Orden de implementación sugerido

1. **P1** (crítico - orden de pasos)
2. **P4** (sencillo - regla simplificada)
3. **P2** (visibilidad S1)
4. **P3** (rúbrica adicional)
5. **P5** (trigger knowledge-log)
6. **Refactoring** (opcional, para v4.1.0)

---

## Archivos a modificar

| Archivo | Cambios |
|---------|--------|
| `meta-skill-architect/task.md` | P1, P2, P3, P4, P5 |
| `meta-skill-architect/SKILL.md` | Actualizar versión a 4.1.0 tras cambios |
| `meta-skill-architect/system.md` | No requiere cambios |
| `meta-skill-architect/README.md` | Actualizar versión y cambios |

---

## Versión resultante

**v4.1.0** — Correcciones de producción (P1-P5)
**v5.0.0** — Refactoring estructural (si se ejecuta el punto 6)
