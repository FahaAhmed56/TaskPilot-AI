"""Explainable task urgency scoring, designed as a decision-support demo."""
from datetime import date
from typing import Any

KEYWORDS = {"outage": 20, "security": 18, "production": 16, "deadline": 8, "blocked": 10, "urgent": 8, "customer": 5}


def prioritize(task: dict[str, Any], today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    title = str(task.get("title", "")).strip()
    if not title:
        raise ValueError("Task title cannot be empty")
    impact = int(task.get("impact", 3))
    effort = int(task.get("effort", 3))
    if impact not in range(1, 6) or effort not in range(1, 6):
        raise ValueError("Impact and effort must be between 1 and 5")
    description = str(task.get("description", ""))
    due = task.get("due_date")
    days_left = None
    if due:
        due_date = date.fromisoformat(str(due))
        days_left = (due_date - today).days
    reasons = []
    score = impact * 12 + (6-effort)*4
    reasons.append(f"Impact level {impact}/5")
    if days_left is not None:
        if days_left < 0:
            score += 30; reasons.append("Overdue")
        elif days_left == 0:
            score += 25; reasons.append("Due today")
        elif days_left <= 2:
            score += 18; reasons.append("Due within 2 days")
        elif days_left <= 7:
            score += 8; reasons.append("Due this week")
    matching = [word for word in KEYWORDS if word in (title + " " + description).lower()]
    if matching:
        score += min(sum(KEYWORDS[w] for w in matching), 30)
        reasons.append("Signals: " + ", ".join(matching))
    score = min(score, 100)
    label = "Critical" if score >= 85 else "High" if score >= 65 else "Medium" if score >= 45 else "Low"
    return {**task, "score": score, "priority": label, "reasons": reasons, "days_left": days_left}


def rank_tasks(tasks: list[dict], today: date | None = None) -> list[dict]:
    return sorted((prioritize(task, today) for task in tasks), key=lambda t: t["score"], reverse=True)
