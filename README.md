# Skills Learning

Colección de skills instalables para agentes de IA (OpenCode, Claude, etc.)

## Skills Included

### 1. Code Analysis
- **Descripción:** Analiza código fuente para identificar bugs, vulnerabilidades de seguridad, code smells y oportunidades de optimización de performance.
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill code-analysis`

### 2. Django-Shield 2026
- **Descripción:** Auditor de ciberseguridad senior para Django 5.x/6.x. Identifica vulnerabilidades lógicas, de configuración, y analiza superficie de ataque (Taint Flow).
- **Instalar:** `npx skills add ASamiraJasbonM/Skills-learning --skill django-shield`

---

## Cómo Instalar una Skill

### Opción 1: Con npx skills (recomendado)

```bash
# Instalar una skill específica
npx skills add ASamiraJasbonM/Skills-learning --skill <nombre-de-skill>

# Ejemplo: code-analysis
npx skills add ASamiraJasbonM/Skills-learning --skill code-analysis

# Ejemplo: django-shield
npx skills add ASamiraJasbonM/Skills-learning --skill django-shield

# Instalar todas las skills
npx skills add ASamiraJasbonM/Skills-learning --skill '*'
```

### Opción 2: Manual

```bash
# Clonar el repositorio
git clone https://github.com/ASamiraJasbonM/Skills-learning.git

# Copiar la skill deseada a tu directorio de skills
cp -r Skills-learning/<skill-name> ~/.config/opencode/skills/
```

---

## Estructura del Repositorio

```
Skills-learning/
├── code-analysis/
│   └── SKILL.md          # Skill de análisis de código
├── django-shield/
│   └── SKILL.md         # Skill de auditoría de seguridad Django
└── README.md
```

---

## Crear una Nueva Skill

```bash
# Inicializar una nueva skill
npx skills init mi-nueva-skill

# Editar el archivo SKILL.md generado
# Subir a GitHub y usar:
npx skills add TU-USUARIO/mi-nueva-skill
```

---

## Requisitos

- Node.js 18+
- Agente de IA compatible (OpenCode, Claude Code, etc.)

---

## License

MIT