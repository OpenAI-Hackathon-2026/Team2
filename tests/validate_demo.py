"""Lightweight structural/privacy checks for synthetic project-nudge demo fixtures."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / ".agents/skills/project-nudge/demo"
EXPECTED = {"chat-only", "project-context", "quota-mixed"}


def main():
    files = sorted(CASES.glob("*.json"))
    assert {p.stem for p in files} == EXPECTED, "expected exactly three named demo files"
    cases = [json.loads(p.read_text()) for p in files]
    for case in cases:
        assert case["case"] and case["goal"] and case["expected"]
    chat = next(c for c in cases if c["case"] == "chat-only-no-quota-source")
    assert chat["capabilities"]["codexbar_source"] is False
    assert chat["expected"]["disclose_quota_aware_selection_unavailable"] is True
    assert chat["expected"]["do_not_substitute_generic_nudge"] is True
    project = next(c for c in cases if c["case"] == "project-context-no-quota-source")
    assert project["expected"]["optional_context_does_not_replace_quota"] is True
    mixed = next(c for c in cases if c["case"] == "multi-provider-quota")
    assert len(mixed["quota_snapshots"]) == 2
    assert len({q["provider"] for q in mixed["quota_snapshots"]}) == 2
    fresh_time = datetime.fromisoformat(mixed["quota_snapshots"][0]["generated_at"].replace("Z", "+00:00"))
    stale_time = datetime.fromisoformat(mixed["quota_snapshots"][1]["generated_at"].replace("Z", "+00:00"))
    assert (fresh_time - stale_time).total_seconds() > 3600
    forbidden = {"password", "access_token", "refresh_token", "api_key", "secret"}
    def keys(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                yield key.lower()
                yield from keys(value)
        elif isinstance(obj, list):
            for value in obj:
                yield from keys(value)
    assert not (set().union(*(set(keys(c)) for c in cases)) & forbidden)
    print("Validated quota-first behavior markers, 3 synthetic demo cases, stale sample, and credential-key privacy guard.")


if __name__ == "__main__":
    main()
