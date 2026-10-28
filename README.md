# TaskPilot AI 🎯

An explainable intelligent task prioritization demo built with **Python, Streamlit, and FastAPI**. Scores tasks based on business impact, effort, due date, and keywords in the task title/description. **No paid API keys needed.**

> Despite the name, this is an explainable rule-based system, **not a trained machine learning model**. It is a decision-support prototype; review its output before making real decisions.

## Features
- Rank tasks by transparent 0–100 priority score
- Critical / High / Medium / Low classifications
- Human-readable reasons for every score
- CSV upload and ranked CSV/JSON export
- Interactive dashboard and REST API
- Sample tasks, unit tests, GitHub Actions

## Quickstart (Windows / VS Code)
```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app/dashboard.py
```
Visit http://localhost:8501. Run from the project root.

## Start API
```powershell
.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

## Run tests
```powershell
.venv\Scripts\python.exe -m pytest -q
```

## Scoring logic
- **Impact (1–5):** +12 points per level
- **Effort (1–5):** +4 points per inverse effort unit (quick wins earn more)
- **Due date:** overdue +30; due today +25; next 2 days +18; next 7 days +8
- **Keywords:** bonus up to 30 for operational urgency signals such as outage, security and blocked
- **Score capped at 100**; Critical ≥85, High ≥65, Medium ≥45, Low <45

This scoring is a configurable heuristic and does not estimate a statistically calibrated risk probability. The sample due dates are illustrative; feel free to edit them.

## Example API request
```bash
curl -X POST http://localhost:8000/prioritize -H "Content-Type: application/json" -d '{"title":"Production outage","description":"Checkout blocked","impact":5,"effort":2,"due_date":"2026-10-28"}'
```

## Files
- `taskpilot/core.py` — prioritization engine
- `app/dashboard.py` — Streamlit UI
- `api/main.py` — FastAPI endpoints
- `data/sample_tasks.csv` — demonstration data
- `tests/test_core.py` — unit tests
- `.github/workflows/tests.yml` — CI

## Security & privacy
Data processing runs locally. There is no user account system; don't expose the demo API publicly without adding authentication, rate limits and appropriate controls.

## License
MIT.
