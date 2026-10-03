"""Synthetic compatibility tests for CodexBar usage JSON; no account or network access."""
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / ".agents/skills/project-nudge/bin/read_codexbar_usage.py"
FIXTURE = ROOT / "tests/fixtures/codexbar-usage-synthetic.json"
NOW = datetime(2030, 1, 2, 9, 30, tzinfo=timezone.utc)


def main():
    payload = json.loads(FIXTURE.read_text())
    # Pin time via direct import so freshness boundaries are deterministic.
    import importlib.util
    spec = importlib.util.spec_from_file_location("codexbar_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    normalized = module.normalize(payload, NOW)
    providers = normalized["providers"]
    assert [p["provider"] for p in providers] == ["claude", "gemini", "cursor"]
    claude = providers[0]
    assert claude["account"] == "Synthetic Claude profile A"
    assert claude["fresh"] is True and claude["creditsFresh"] is True
    assert claude["windows"]["primary"]["windowMinutes"] == 300
    assert claude["windows"]["secondary"]["windowMinutes"] == 10080
    assert claude["credits"]["remaining"] == 12
    gemini = providers[1]
    assert gemini["error"]["message"] == "Synthetic provider fetch failure"
    assert "windows" in gemini and not gemini["windows"]
    cursor = providers[2]
    assert cursor["windows"]["extraRateWindows"][0]["id"] == "fast"
    assert cursor["subscriptionExpiresAt"] == "2030-01-31T00:00:00Z"

    stale = module.normalize([{"provider": "claude", "usage": {"updatedAt": "2030-01-02T08:00:00Z"}}], NOW)
    assert stale["providers"][0]["fresh"] is False
    missing = module.normalize([{"provider": "claude", "usage": {}}], NOW)
    assert missing["providers"][0]["fresh"] is False
    naive = module.normalize([{"provider": "claude", "usage": {"updatedAt": "2030-01-02T09:00:00"}}], NOW)
    assert naive["providers"][0]["fresh"] is False

    fake_payload = json.dumps(payload)
    fake = "#!/usr/bin/env python3\nimport sys\nprint(" + repr(fake_payload) + ")\n"
    with tempfile.TemporaryDirectory() as td:
        fake_bin = Path(td) / "codexbar"
        fake_bin.write_text(fake)
        fake_bin.chmod(0o700)
        proc = subprocess.run([sys.executable, str(READER), "--codexbar-bin", str(fake_bin)], capture_output=True, text=True, timeout=5)
        assert proc.returncode == 0, proc.stderr
        cli_data = json.loads(proc.stdout)
        assert len(cli_data["providers"]) == 3
        assert "codex" not in [p["provider"] for p in cli_data["providers"]]
        absent = subprocess.run([sys.executable, str(READER), "--codexbar-bin", str(Path(td) / "missing")], capture_output=True, text=True, timeout=5)
        assert absent.returncode == 2
        assert "optional CodexBar data unavailable" in absent.stderr

    print("CodexBar adapter synthetic schema, provider separation, freshness, and optional failure checks passed.")


if __name__ == "__main__":
    main()
