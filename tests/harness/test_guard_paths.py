import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import guard_paths as gp


def test_allowed_paths_for_builder():
    files = ["src/namethellm/data.py", "harness/artifacts/T-0001/05-build-main.md", "harness/artifacts/T-0001/handoff-builder-to-reviewer.json"]
    violations = gp.check_paths("builder", files)
    assert violations == []


def test_builder_cannot_touch_tests():
    files = ["tests/unit/test_data.py"]
    violations = gp.check_paths("builder", files)
    assert len(violations) == 1
    assert "outside allow-list" in violations[0]


def test_test_author_can_touch_tests():
    files = ["tests/unit/test_data.py", "harness/artifacts/T-0001/04-tests.md"]
    violations = gp.check_paths("test-author", files)
    assert violations == []


def test_test_author_cannot_touch_src():
    files = ["src/namethellm/data.py"]
    violations = gp.check_paths("test-author", files)
    assert len(violations) == 1


def test_po_spec_allowed_files():
    files = ["harness/artifacts/T-0001/01-spec.md", "harness/artifacts/T-0001/handoff-po-to-tech-lead.json"]
    assert gp.check_paths("po-spec", files) == []


def test_po_spec_cannot_write_code():
    assert len(gp.check_paths("po-spec", ["src/main.py"])) == 1
