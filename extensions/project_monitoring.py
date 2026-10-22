"""Transparent project monitoring and human review queue on synthetic inputs."""
import json
from pathlib import Path

def analyze(tasks):
    output = []
    for task in tasks:
        overdue = task["days_to_due"] < 0 and task["progress"] < 100
        blocked = bool(task["blocker"])
        high_risk = overdue or (blocked and task["criticality"] == "high")
        output.append({"id": task["id"], "owner": task["owner"],
                       "status": "escalate" if high_risk else ("watch" if blocked else "on_track"),
                       "reason": "overdue" if overdue else ("blocked" if blocked else "none"),
                       "requires_human_review": high_risk})
    return {"tasks": output, "escalations": sum(x["requires_human_review"] for x in output)}

if __name__ == "__main__":
    path = Path(__file__).resolve().parents[1] / "data" / "synthetic_project_tasks.json"
    print(json.dumps(analyze(json.loads(path.read_text())), indent=2))
