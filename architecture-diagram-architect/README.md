# Architecture Diagram Architect

Módulo de capacidad para agentes de IA especializado en la generación de diagramas como código (Diagrams-as-Code) utilizando Python.

## Requisitos Previos

Para ejecutar el código generado por esta skill, necesitas:

1.  **Python 3.6+**
2.  **Graphviz:** El motor de renderizado.
    -   *Windows:* `choco install graphviz` o descarga desde [graphviz.org](https://graphviz.org/download/).
    -   *macOS:* `brew install graphviz`
    -   *Linux:* `sudo apt install graphviz`
3.  **Librería `diagrams`:**
    ```bash
    pip install diagrams
    ```

## Uso

1.  Proporciona a tu agente de IA (Gemini/Opencode) los requerimientos de tu arquitectura.
2.  El agente utilizará la skill para generar un script de Python.
3.  Ejecuta el script para generar la imagen (por defecto en formato `.png`).

```bash
python mi_arquitectura.py
```

## Ejemplo Incluido

He incluido un archivo `example.py` que representa una arquitectura web básica en AWS. Ejecútalo para probar tu instalación.
