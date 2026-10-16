import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import validate_handoff as vh


def test_valid_handoff(tmp_path):
    # Setup artifact and harness.md
    art = tmp_path / "harness/artifacts/T-0001/01-spec.md"
    art.parent.mkdir(parents=True, exist_ok=True)
    art.write_text("# Spec", encoding="utf-8")
    harness_md = tmp_path / "docs/harness.md"
    harness_md.parent.mkdir(parents=True, exist_ok=True)
    harness_md.write_text("AC-001-a AC-001-b", encoding="utf-8")

    data = {
        "task_id": "T-0001",
        "from": "po-spec",
        "to": "tech-lead",
        "artifact": "harness/artifacts/T-0001/01-spec.md",
        "status": "complete",
        "summary": "Spec complete",
        "inputs_consumed": [],
        "acceptance_refs": ["AC-001-a"],
        "files_touched": ["harness/artifacts/T-0001/01-spec.md"],
        "checks_run": [],
    }
    ok, errs = vh.validate_handoff(data, root=tmp_path)
    assert ok, errs


def test_reject_incomplete_status(tmp_path):
    data = {"status": "in_progress", "artifact": "fake.md"}
    ok, errs = vh.validate_handoff(data, root=tmp_path)
    assert not ok
    assert any("status must be 'complete'" in e for e in errs)


def test_reject_missing_artifact(tmp_path):
    data = {"status": "complete", "artifact": "nonexistent.md"}
    ok, errs = vh.validate_handoff(data, root=tmp_path)
    assert not ok
    assert any("does not exist" in e for e in errs)


def test_reject_invalid_acceptance_ref(tmp_path):
    art = tmp_path / "art.md"
    art.write_text("art", encoding="utf-8")
    harness_md = tmp_path / "docs/harness.md"
    harness_md.parent.mkdir(parents=True, exist_ok=True)
    harness_md.write_text("AC-001-a", encoding="utf-8")

    data = {
        "status": "complete",
        "artifact": "art.md",
        "acceptance_refs": ["AC-999-z"],
    }
    ok, errs = vh.validate_handoff(data, root=tmp_path)
    assert not ok
    assert any("not found in docs/harness.md" in e for e in errs)


def test_reject_files_outside_allowlist(tmp_path):
    art = tmp_path / "art.md"
    art.write_text("art", encoding="utf-8")
    data = {
        "status": "complete",
        "artifact": "art.md",
        "from": "po-spec",
        "files_touched": ["src/main.py"],
    }
    ok, errs = vh.validate_handoff(data, root=tmp_path)
    assert not ok
    assert any("outside allow-list" in e for e in errs)


def test_reject_mandatory_check_roles_with_no_checks(tmp_path):
    art = tmp_path / "art.md"
    art.write_text("art", encoding="utf-8")
    data = {
        "status": "complete",
        "artifact": "art.md",
        "from": "builder",
        "checks_run": [],
    }
    ok, errs = vh.validate_handoff(data, root=tmp_path)
    assert not ok
    assert any("must provide at least one check" in e for e in errs)
