"""Protocol smoke test with a synthetic Codex app-server; makes no network/auth calls."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READER = ROOT / ".agents/skills/project-nudge/bin/read_codex_quota.py"


FAKE = r'''#!/usr/bin/env python3
import json, os, sys
for line in sys.stdin:
    msg = json.loads(line)
    method = msg.get("method")
    if method == "initialize":
        print(json.dumps({"jsonrpc":"2.0", "id":msg["id"], "result":{}}), flush=True)
    elif method == "account/rateLimits/read":
        key = "rateLimits" if os.environ.get("FAKE_FALLBACK") else "rateLimitsByLimitId"
        print(json.dumps({"jsonrpc":"2.0", "id":msg["id"], "result":{
            key:{
                "codex":{"primary":{"usedPercent":58,"windowDurationMins":300,"resetsAt":1900000000},
                         "secondary":{"usedPercent":12,"windowDurationMins":10080,"actuallyResetsAt":1900100000},
                         "credits":{"balance":9,"resetsAt":1900200000}}
            },
            "rateLimitResetCredits":{"availableCount":1,"credits":[{"resetType":"codexRateLimits","status":"available","grantedAt":1900000000,"expiresAt":1900300000,"title":"Full reset"}]}
        }}), flush=True)
        break
'''


def main():
    with tempfile.TemporaryDirectory() as td:
        fake = Path(td) / "fake-codex"
        fake.write_text(FAKE)
        fake.chmod(0o700)
        proc = subprocess.run([sys.executable, str(READER), "--codex-bin", str(fake)], capture_output=True, text=True, timeout=12)
        assert proc.returncode == 0, proc.stderr
        data = json.loads(proc.stdout)
        assert data["source"] == "codex-cli-app-server"
        limit = data["rateLimits"]["codex"]
        assert limit["primary"]["windowDurationMins"] == 300
        assert limit["secondary"]["windowDurationMins"] == 10080
        assert limit["secondary"]["actuallyResetsAt"] == 1900100000
        assert limit["credits"]["resetsAt"] == 1900200000
        reset = data["rateLimitResetCredits"]["credits"][0]
        assert reset["resetType"] == "codexRateLimits" and reset["expiresAt"] == 1900300000
        env = dict(os.environ, FAKE_FALLBACK="1")
        fallback = subprocess.run([sys.executable, str(READER), "--codex-bin", str(fake)], env=env, capture_output=True, text=True, timeout=12)
        assert fallback.returncode == 0, fallback.stderr
        assert "codex" in json.loads(fallback.stdout)["rateLimits"]
        missing = subprocess.run([sys.executable, str(READER), "--codex-bin", str(Path(td) / "missing")], capture_output=True, text=True, timeout=12)
        assert missing.returncode == 2 and "Could not start Codex app-server" in missing.stderr
    print("Codex app-server reader protocol smoke test passed with synthetic account/rate-limit data.")


if __name__ == "__main__":
    main()
