# Contribuire al progetto

Grazie per voler contribuire!  
Questo progetto adotta best practice di sicurezza, code style e automazione.

---

## 🚀 Setup ambiente

```bash
pip install -r requirements-dev.txt
pre-commit install
```
- **pre-commit** verrà eseguito automaticamente prima di ogni commit per controllare qualità e sicurezza del codice.

---

## 🧪 Test & Coverage

```bash
coverage run -m pytest
coverage report
coverage html
```

---

## 💡 Lint, Type-check, Sicurezza

```bash
pre-commit run --all-files
flake8 .
black --check .
isort --check .
mypy .
bandit -r .
pip-audit -r requirements.txt
```
- Questi controlli vengono eseguiti anche in CI/CD.
- **isort** verifica che gli import siano ordinati.
- **check-yaml** e **check-ini** verificano la sintassi di file YAML/INI.

---

## ✅ Regole Pull Request

- Coverage >90%
- Test automatici obbligatori
- Aggiorna documentazione se necessario
- Segui naming branch: `feature/...`, `fix/...`, ecc.
- Tutti i check pre-commit devono passare!
- Usa i template PR e issue

---

## 🛡️ Security

- Segnala vulnerabilità seguendo [SECURITY.md](SECURITY.md)
- Tutte le dipendenze vengono controllate con pip-audit in CI

---

## 🗂️ Issue e Feature

- Usa i template nelle issue
- Spiega chiaramente il problema o la richiesta

---

## 📦 Struttura progetto

```text
├── diagnostics.py
├── requirements.txt
├── requirements-dev.txt
├── .pre-commit-config.yaml
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── SECURITY.md
│   └── CONTRIBUTING.md
```

---

## 🎯 Buon coding!