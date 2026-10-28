from datetime import date
import pytest
from taskpilot.core import prioritize, rank_tasks

TODAY = date(2026, 10, 28)

def test_missing_title():
    with pytest.raises(ValueError): prioritize({"title": " "}, TODAY)

def test_invalid_impact():
    with pytest.raises(ValueError): prioritize({"title": "A", "impact": 6}, TODAY)

def test_overdue_is_more_urgent():
    base = {"title": "Write report", "impact": 3, "effort": 3}
    overdue = prioritize({**base, "due_date": "2026-10-27"}, TODAY)
    later = prioritize({**base, "due_date": "2026-12-20"}, TODAY)
    assert overdue["score"] > later["score"]

def test_sorted():
    tasks = [{"title": "Minor chore", "impact": 1, "effort": 5}, {"title": "Production outage", "impact": 5, "effort": 1}]
    assert rank_tasks(tasks, TODAY)[0]["title"] == "Production outage"

def test_score_cap():
    result = prioritize({"title": "Production outage urgent security blocked", "impact": 5, "effort": 1, "due_date": "2020-01-01"}, TODAY)
    assert result["score"] == 100

def test_bad_date():
    with pytest.raises(ValueError): prioritize({"title": "A", "due_date": "tomorrow"}, TODAY)
