# Implementation Plan

## Constraints and decisions

- Work in `Team2`; use fixture-based development and checks in the OpenAI-hosted environment. Preserve teammate changes and keep secrets and personal data out of fixtures.
- Build for a ChatGPT dot skill. A repo file alone does not install the skill, and this environment does not inherit dot's email/chat connectors. Validate the repository version first; install and test the actual skill with dot separately afterward.
- Describe capability adapters against host-exposed context; do not guess host capabilities. Read quota through the local Codex CLI app-server on Kyle's authorized MacBook M1 Pro; CodexBar is optional for additional subscriptions. Keep credentials local; MVP does not need an always-on server.
- Keep project naming neutral until Kyle chooses a name. `Pace` was only a suggestion, not an agreed name.
- Hackathon ends around 3pm America/New_York; optimize for a narrow end-to-end vertical slice. Defer scheduler and cross-provider execution pending separate authorization and prerequisites.

## Vertical slices

1. **Grounded chat-only response:** Define the input/output contract and prompt behavior around user goals, available chat, one next step, its current relevance, and a small completion goal. Add synthetic fixtures and checks for chat-only success, insufficient context, deferral, and no-nudge behavior.
2. **Optional project context:** Add capability checks for email/GitHub only where the host exposes connected data. Exercise connected, absent, and partially available source fixtures; ensure chat-only usefulness remains intact and observed facts are distinguishable from inference.
3. **Quota-aware pacing:** Use the Codex CLI app-server reader; optionally add separate CodexBar data only for additional subscriptions; use synthetic multi-provider fixtures for provider/window/reset/credits/banked expiry, missing windows, invalid timestamps, and stale (>1 hour) snapshots. Require fresh usable Codex CLI quota for quota-aware selection; keep unknown values unknown and never pool providers.
4. **Privacy and review:** Check that no fixture contains real personal data or credentials and that optional activity context is gated by enablement and host exposure. Review outputs against the acceptance scenarios; revise the concise skill instructions and repository docs as needed.
5. **Dot handoff:** After the repository version is validated, install and exercise it with dot using only the permissions and connections dot actually exposes. Record host-specific gaps as follow-up decisions rather than inventing interfaces.

## 60–90 second demo

- **0–15s:** State Kyle's project goal in chat and show a concrete, small next step with why it matters now and a completion check.
- **15–35s:** Add synthetic GitHub or email project context and show how the grounded suggestion changes; mention chat-only still works when sources are absent.
- **35–60s:** Show synthetic fresh quota data for two configured providers with separate windows/resets, then show stale or missing data staying unknown without blocking the suggestion.
- **60–90s:** Defer the suggestion or request no nudge, demonstrate the assistant honoring that choice, and close on privacy boundaries and what remains out of scope.

## Decisions to settle during implementation

- Which project name Kyle wants, if any.
- The exact dot skill packaging and invocation contract, confirmed by actual installation rather than assumed from repository files.
- Which source capabilities and data shapes dot exposes in the later skill test, and which remain unavailable.
- Whether dot can invoke the quota reader through its authorized executor and how optional CodexBar data can expose additional providers; unsupported fields must stay unknown.
