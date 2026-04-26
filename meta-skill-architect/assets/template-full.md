---
name: template-full
version: 1.0.0
description: Plantilla completa de SKILL.md para meta-skill-architect
---

# [Nombre]

[Descripción: qué hace, cuándo activa, qué NO hace.]

## Supuestos
[Si hubo ambigüedad, documenta. Si no, "Ninguno."]

## Riesgos Identificados
- **[Tipo]:** [Descripción] → [Mitigación]

## Instrucciones Operativas

### Rol
[2-4 oraciones: identidad y límites.]

### Contexto
[Entorno, herramientas, restricciones.]

### Tarea
[Pasos numerados con output esperado. Delimitadores donde aplique.]

### Formato de Salida
[Estructura exacta. Ejemplo con valores reales.]

### Restricciones
- MUST: [obligatorio]
- SHOULD: [recomendado]
- WON'T: [fuera de alcance]

## Manejo de Errores

| Escenario | Diagnóstico | Acción | Señal de recuperación |
|-----------|------------|--------|----------------------|
| [1] | [causa probable] | [acción concreta] | [cuándo se resuelve o —] |
| [2] | [causa probable] | [acción concreta] | [cuándo se resuelve o —] |
| [3] | [causa probable] | [acción concreta] | [cuándo se resuelve o —] |
| [4] | [causa probable] | [acción concreta] | [cuándo se resuelve o —] |

## Rúbrica de Validación

| Criterio | Éxito | Fallo |
|----------|-------|-------|
| Fidelidad al dominio | [observable] | [observable] |
| Densidad semántica | [métrica] | [señal] |
| Resistencia inyección | [comportamiento] | [fallo] |
| Completitud | [contenido real] | [vacío/placeholder] |
| Consistencia desc↔cuerpo | [todo en descripción está en cuerpo] | [ausente o extra en cuerpo] |