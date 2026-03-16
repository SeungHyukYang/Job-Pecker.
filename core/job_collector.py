import json
from pathlib import Path
from core.models import Job

DATA_PATH = Path("data/jobs/sample_jobs.json")
DECISIONS_PATH = Path("data/jobs/decisions.json")


def load_jobs():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Job(**job) for job in data]


def load_decisions():
    if not DECISIONS_PATH.exists():
        return {}

    with open(DECISIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_decision(job_id: str, action: str):
    decisions = load_decisions()
    decisions[job_id] = action

    with open(DECISIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(decisions, f, indent=2)