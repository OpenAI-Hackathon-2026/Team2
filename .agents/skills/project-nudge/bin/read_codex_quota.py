#!/usr/bin/env python3
"""Read the signed-in Codex CLI rate-limit snapshot through app-server JSON-RPC.

No auth files are read. Authentication remains entirely inside the installed CLI.
"""
import argparse
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time

TIMEOUT_SECONDS = 8


class QuotaReadError(Exception):
    pass


def read_messages(stream, output):
    try:
        for line in iter(stream.readline, ""):
            output.put(line)
    finally:
        output.put(None)


def parse_response(lines, request_id):
    for line in lines:
        try:
            message = json.loads(line)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(message, dict) and message.get("id") == request_id:
            if "error" in message:
                detail = message["error"].get("message", "Codex app-server returned an error")
                raise QuotaReadError(str(detail))
            return message.get("result")
    raise QuotaReadError("Codex app-server closed before returning the quota response")


def request(proc, inbox, request_id, method, params=None):
    message = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        message["params"] = params
    try:
        proc.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
        proc.stdin.flush()
    except (BrokenPipeError, OSError) as exc:
        raise QuotaReadError("Codex app-server stopped while reading quota") from exc

    deadline = time.monotonic() + TIMEOUT_SECONDS
    lines = []
    while time.monotonic() < deadline:
        try:
            line = inbox.get(timeout=max(0.01, deadline - time.monotonic()))
        except queue.Empty:
            break
        if line is None:
            return parse_response(lines, request_id)
        lines.append(line)
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(msg, dict) and msg.get("id") == request_id:
            return parse_response(lines, request_id)
    raise QuotaReadError(f"Timed out waiting for Codex app-server method {method}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-bin", help="Codex executable (primarily useful for controlled tests)")
    args = parser.parse_args()
    codex = args.codex_bin or os.environ.get("CODEX_BIN") or shutil.which("codex")
    if not codex:
        raise QuotaReadError("Codex CLI was not found on PATH. Install/run Codex CLI and sign in, then retry.")

    try:
        proc = subprocess.Popen(
            [codex, "app-server", "--listen", "stdio://"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1,
        )
    except OSError as exc:
        raise QuotaReadError(f"Could not start Codex app-server: {exc}") from exc

    inbox = queue.Queue()
    reader = threading.Thread(target=read_messages, args=(proc.stdout, inbox), daemon=True)
    reader.start()
    try:
        request(proc, inbox, 1, "initialize", {
            "clientInfo": {"name": "quota-readonly", "version": "1"}
        })
        proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "initialized", "params": {}}) + "\n")
        proc.stdin.flush()
        result = request(proc, inbox, 2, "account/rateLimits/read", {})
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=1)
        if proc.stdin:
            proc.stdin.close()
        if proc.stdout:
            proc.stdout.close()
        if proc.stderr:
            proc.stderr.close()

    if not isinstance(result, dict):
        raise QuotaReadError("Codex returned no usable rate-limit data")
    # Preserve Codex's per-limit windows, balances, and resets without pooling or guessing.
    limits = result.get("rateLimitsByLimitId")
    if not isinstance(limits, dict) or not limits:
        limits = result.get("rateLimits")
    if not isinstance(limits, (dict, list)) or not limits:
        raise QuotaReadError("Codex returned no rate-limit windows; quota is unknown")
    output = {
        "source": "codex-cli-app-server",
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rateLimits": limits,
    }
    # Keep reset-credit entries and expiry timestamps individually attributed.
    # This response does not identify the local account; do not inspect auth state.
    if "rateLimitResetCredits" in result:
        output["rateLimitResetCredits"] = result["rateLimitResetCredits"]
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except QuotaReadError as exc:
        print(f"quota unavailable: {exc}", file=sys.stderr)
        raise SystemExit(2)
