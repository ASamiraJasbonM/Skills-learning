# Knowledge Log — meta-skill-architect

> Propósito: Registrar patrones de fallo recurrentes, soluciones exitosas y anti-patrones descubiertos a través de sesiones.
> Mantener actualizado al cerrar cada auditoría o modificación.

---

## Patrones de Fallo Recurrentes

| ID | Patrón | Señal | Solución probada | Fecha primer registro |
|----|--------|-------|------------------|-----------------------|
| P01 | Rúbrica vaga | "El output está completo" sin threshold | Añadir criterio cuantificable con ≥N | 2026-04-27 |
| P02 | Tabla errores < 4 filas | Skill pasa validación por secciones pero falla en conteo | validate_structure check D2 | 2026-04-27 |
| P03 | Instrucción no autónoma | "Procesa apropiadamente" | Reformular con input, criterio, señal de terminación | 2026-04-27 |
| P04 | Description con angle brackets | description contiene `< >` | Reemplazar con texto plano, validar en validate_structure | 2026-04-27 |
| P05 | Frontmatter dependencies como string | dependencies: "a, b, c" en vez de lista YAML | Cambiar a lista YAML, añadir validación | 2026-04-27 |
| P06 | SKILL.md sobrecargado | >5000 palabras o >500 líneas | Mover documentación estática a references/ | 2026-04-27 |
| P07 | Versión hardcoded en scripts | mcp_server.py en v3.0.0 cuando skill era v5.0.0 | Sincronizar versión de scripts con SKILL.md en cada release | 2026-04-28 |
| P08 | Fecha hardcoded en reportes | evaluation_date fija en test_runner.py | Usar datetime.date.today().isoformat() | 2026-04-28 |

---

## Soluciones Canónicas

| Problema | Solución canónica | Evidencia de éxito |
|----------|------------------|--------------------|
| Inyección en cuerpo de ticket | Delimitadores `<ticket>...</ticket>` + campo Alerta | Ejemplo 1 en examples.md |
| Scope creep en skills de clasificación | Restricción WON'T explícita: "No resuelve el problema" | Ejemplo 1, 2 en examples.md |
| Validador con bugs silenciosos | Tests con fixtures (valid, broken, missing) | validate_fixtures/ |
| Evals no confiables sin CLI | Warning explícito en test_runner.py y README | D1 implementado |
| Skill incompleta sin system.md | Fallback de contexto inline en SKILL.md | D3 implementado |

---

## Anti-patrones

- **Añadir reglas sobre modelo mental roto:** Si el mismo comportamiento falla tras 2 iteraciones quirúrgicas, no añadir más reglas — reescribir la metáfora completa.
- **Rúbrica de intención:** "El output es bueno" — no es medible. Siempre threshold cuantificable.
- **Placeholder en description:** description con `<brackets>` falla el validador.
- **Dependencies como string:** Otros parsers YAML esperan lista, no string separado por comas.
- **Scripts presentados como funcionales:** Un stub sin NotImplementedError genera confusión y bugs difíciles de diagnosticar.
- **Criterio de terminación implícito:** Si el agente no sabe cuándo ha completado un paso, el comportamiento es inconsistente entre sesiones.

---

## Actualizaciones de Estándar

| Fecha | Cambio | Archivos afectados | Estado |
|-------|--------|-------------------|--------|
| 2026-04-27 | v3.0.0 → v4.0.0: Editor estructural completo | task.md, SKILL.md, validate_structure.py | ✅ |
| 2026-04-27 | dependencies como lista YAML | SKILL.md | ✅ |
| 2026-04-27 | Check de peso en validate_structure.py | validate_structure.py | ✅ |
| 2026-04-28 | v4.1.0: correcciones producción (P1-P5): orden auditoría+mejora, visibilidad S1, rúbrica código, historial siempre, trigger knowledge-log | task.md, SKILL.md | ✅ |
| 2026-04-28 | v5.0.0: refactoring estructural — task.md reducido a ~200 líneas, protocolos movidos a references/protocols-advanced.md y protocols-core.md | task.md, references/ | ✅ |
