from extensions.project_monitoring import analyze

def test_escalation_and_review():
    rows = [{"id":"a","owner":"test","days_to_due":-1,"progress":50,"blocker":False,"criticality":"high"}]
    r = analyze(rows)
    assert r["escalations"] == 1
    assert r["tasks"][0]["requires_human_review"]

def test_completed_task_not_overdue():
    rows = [{"id":"b","owner":"test","days_to_due":-1,"progress":100,"blocker":False,"criticality":"high"}]
    assert analyze(rows)["escalations"] == 0
