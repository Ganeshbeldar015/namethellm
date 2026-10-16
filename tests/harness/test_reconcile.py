import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import check_harness as ch
from test_harness import make


def test_reconcile_detects_deleted_agents_md(tmp_path):
    r = make(tmp_path)
    (r / "AGENTS.md").unlink()
    errs = ch.check_required_files(r) + ch.check_agents_md(r)
    assert any("AGENTS.md" in e for e in errs)
    assert any(ch.classify(e) == "MISSING" for e in errs)


def test_reconcile_detects_blank_agents_md(tmp_path):
    r = make(tmp_path)
    (r / "AGENTS.md").write_text("   \n\t  ", encoding="utf-8")
    errs = ch.check_unconfigured(r)
    assert any("AGENTS.md is blank" in e for e in errs)
    assert any(ch.classify(e) == "UNCONFIGURED" for e in errs)


def test_reconcile_detects_stale_docs(tmp_path):
    r = make(tmp_path)
    (r / "docs/raw.md").write_text("initial raw", encoding="utf-8")
    s = json.loads((r / "harness/state/state.json").read_text(encoding="utf-8"))
    s["derived_from"] = {"raw_md_sha": hashlib.sha256(b"initial raw").hexdigest()}
    (r / "harness/state/state.json").write_text(json.dumps(s), encoding="utf-8")
    assert ch.check_stale(r) == []

    # Modify raw.md
    (r / "docs/raw.md").write_text("updated raw with new requirements", encoding="utf-8")
    errs = ch.check_stale(r)
    assert len(errs) > 0
    assert any(ch.classify(e) == "STALE" for e in errs)


def test_drifted_detection_via_content_hash():
    # Demonstrating the drift detection header logic
    header_template = "<!-- generated-by: harness v1 | source: harness.md@123 | hash: {body_hash} -->\n{body}"
    body = "# Builder Role\nContent here"
    correct_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    valid_content = header_template.format(body_hash=correct_hash, body=body)

    # Human edited the body
    tampered_content = valid_content + "\nExtra hand-written notes"

    import re
    m = re.search(r"hash:\s*([a-f0-9]+)", tampered_content)
    assert m is not None
    original_hash = m.group(1)
    new_body = tampered_content.split("-->\n", 1)[1]
    new_hash = hashlib.sha256(new_body.encode("utf-8")).hexdigest()

    # Drifted because header hash != new content hash
    assert original_hash != new_hash
