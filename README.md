# Skills Learning

Collection of installable skills for AI agents (OpenCode, Claude, etc.)

## Skills Included

### 1. Code Analysis
- **Description:** Analyzes source code to identify bugs, security vulnerabilities, code smells, and performance optimization opportunities.
- **Install:** `npx skills add ASamiraJasbonM/Skills-learning --skill code-analysis`

### 2. Django-Shield 2026
- **Description:** Senior cybersecurity auditor for Django 5.x/6.x. Identifies logic and configuration vulnerabilities, analyzes attack surface (Taint Flow).
- **Install:** `npx skills add ASamiraJasbonM/Skills-learning --skill django-shield`

---

## How to Install a Skill

### Option 1: Using npx skills (recommended)

```bash
# Install a specific skill
npx skills add ASamiraJasbonM/Skills-learning --skill <skill-name>

# Example: code-analysis
npx skills add ASamiraJasbonM/Skills-learning --skill code-analysis

# Example: django-shield
npx skills add ASamiraJasbonM/Skills-learning --skill django-shield

# Install all skills
npx skills add ASamiraJasbonM/Skills-learning --skill '*'
```

### Option 2: Manual

```bash
# Clone the repository
git clone https://github.com/ASamiraJasbonM/Skills-learning.git

# Copy the desired skill to your skills directory
cp -r Skills-learning/<skill-name> ~/.config/opencode/skills/
```

---

## Repository Structure

```
Skills-learning/
├── code-analysis/
│   └── SKILL.md          # Code analysis skill
├── django-shield/
│   └── SKILL.md         # Django security audit skill
└── README.md
```

---

## Creating a New Skill

```bash
# Initialize a new skill
npx skills init my-new-skill

# Edit the generated SKILL.md file
# Push to GitHub and use:
npx skills add YOUR_USERNAME/my-new-skill
```

---

## Requirements

- Node.js 18+
- Compatible AI agent (OpenCode, Claude Code, etc.)

---

## License

MIT