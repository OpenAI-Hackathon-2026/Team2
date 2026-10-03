#!/usr/bin/env python3
"""Optionally read non-Codex subscriptions from CodexBar's documented JSON CLI.

CodexBar is an additive source only: Codex records are excluded because the
Codex CLI app-server reader remains primary. No credentials are accessed here.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

MAX_AGE_SECONDS = 3600


class CodexBarReadError(Exception):
    pass


def parse_time(value):
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def fresh(timestamp, now):
    parsed = parse_time(timestamp)
    age = (now - parsed).total_seconds() if parsed else None
    return parsed is not None and 0 <= age <= MAX_AGE_SECONDS


def normalize(payload, now=None):
    """Return per-account non-Codex records without filling missing fields."""
    now = now or datetime.now(timezone.utc)
    if not isinstance(payload, list):
        raise CodexBarReadError("CodexBar JSON must be an array of provider records")

    providers = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        provider = item.get("provider")
        if not isinstance(provider, str) or not provider.strip():
            continue
        provider = provider.strip()
        if provider.casefold() == "codex":
            continue

        usage = item.get("usage") if isinstance(item.get("usage"), dict) else {}
        updated_at = usage.get("updatedAt")
        record = {
            "provider": provider,
            "account": item.get("account") if isinstance(item.get("account"), str) else None,
            "source": item.get("source") if isinstance(item.get("source"), str) else None,
            "updatedAt": updated_at,
            "fresh": fresh(updated_at, now),
            "windows": {},
        }
        if isinstance(item.get("error"), dict):
            error = item["error"]
            # Preserve provider-local errors without leaking unrelated payload fields.
            record["error"] = {
                key: error[key] for key in ("code", "message", "kind") if key in error
            }
        else:
            for key in ("primary", "secondary", "tertiary"):
                window = usage.get(key)
                if isinstance(window, dict):
                    record["windows"][key] = {
                        field: window[field]
                        for field in ("usedPercent", "windowMinutes", "resetsAt", "resetDescription")
                        if field in window
                    }
            extras = usage.get("extraRateWindows")
            if isinstance(extras, list):
                record["windows"]["extraRateWindows"] = [
                    {field: value[field] for field in ("id", "title", "window", "usageKnown") if field in value}
                    for value in extras if isinstance(value, dict)
                ]
            credits = item.get("credits")
            if isinstance(credits, dict):
                # Balance is useful only with its timestamp and stays provider/account scoped.
                record["credits"] = {
                    key: credits[key] for key in
                    ("remaining", "updatedAt", "balanceReadSucceeded", "creditsAvailable", "balanceIsWorkspace")
                    if key in credits
                }
                record["creditsFresh"] = fresh(credits.get("updatedAt"), now)
            for field in ("subscriptionExpiresAt", "subscriptionRenewsAt"):
                if field in usage:
                    record[field] = usage[field]
        providers.append(record)

    return {
        "source": "codexbar-cli",
        "generatedAt": now.isoformat().replace("+00:00", "Z"),
        "maxAgeSeconds": MAX_AGE_SECONDS,
        "providers": providers,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codexbar-bin", help="CodexBar executable (useful for controlled tests)")
    args = parser.parse_args()
    executable = args.codexbar_bin or os.environ.get("CODEXBAR_BIN") or shutil.which("codexbar")
    if not executable:
        raise CodexBarReadError("CodexBar is not installed or not on PATH; optional provider data is unavailable")
    try:
        result = subprocess.run(
            [executable, "usage", "--format", "json", "--provider", "all"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CodexBarReadError(f"Could not read CodexBar usage: {exc}") from exc
    if result.returncode:
        raise CodexBarReadError(f"CodexBar exited with status {result.returncode}")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise CodexBarReadError("CodexBar did not return valid JSON on stdout") from exc
    json.dump(normalize(payload), sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except CodexBarReadError as exc:
        print(f"optional CodexBar data unavailable: {exc}", file=sys.stderr)
        raise SystemExit(2)
