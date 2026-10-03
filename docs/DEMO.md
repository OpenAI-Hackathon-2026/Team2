# Project Nudge demo (60–90 seconds)

Run `python3 tests/validate_demo.py` from Team2. The JSON files are fictional fixtures, not live quota acquisition. In dot, check for an authorized local executor. The helper must run on Kyle's authorized computer where Codex CLI is installed and signed in; this test environment has no access to that machine.

1. **No quota source:** Open `demo/chat-only.json`. The skill should say quota-aware selection is unavailable and ask for one action to supply authorized fresh data or wait. It must not pass off a generic project nudge as quota-aware.
2. **Project context:** Open `demo/project-context.json`. Email/GitHub summaries enrich the candidate work but do not substitute for quota. Disclose missing quota source.
3. **Quota mapping:** Open `demo/quota-mixed.json`. Relate Provider A's fresh, separately attributed session/credits/reset details to the listed bounded candidate tasks. Provider B's older-than-one-hour snapshot stays unknown. Explain uncertainty; do not pool providers or predict task cost.
4. **Close:** Confirm deferral/no-nudge behavior. Test actual Codex CLI app-server acquisition on Kyle's Mac and confirm dot can invoke the helper through an authorized executor.

Fixtures contain no real personal data. Never add personal messages, credentials, or real quota snapshots to the repository.
