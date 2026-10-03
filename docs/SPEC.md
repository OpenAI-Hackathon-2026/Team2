# Project Specification (working title TBD)

## Purpose

Help people with deep domain knowledge and limited coding experience make steady progress on a project. Offer one grounded next step, explain why it matters now, and define a small completion goal. Suggestions should support the user's own judgment and preserve capacity for conversations with colleagues and customers.

## Intended users and context

The initial use case is Kyle's hardware business: experienced colleagues hold valuable customer, product, and workflow knowledge, while Kyle is building project work around that expertise. The assistant should turn available context and user goals into a manageable next action, not assume coding fluency or replace conversations with colleagues.

## MVP

- Implement a ChatGPT dot skill in the Team2 repository. Treat the host as the source of the current chat and use only context and capabilities it actually exposes.
- Start with the user's stated goal and available chat context. Email and GitHub project context may enrich suggestions when connected and exposed; their absence must not block a useful chat-only response.
- Return a single useful next step, a brief reason it matters now, and a small, observable completion goal. Use gentle, plain language and ground suggestions in evidence. Acknowledge uncertainty rather than inventing project facts.
- Respect a user's deferral, avoid repeating the same nudge, and allow the user to request no nudge. The skill does not schedule itself.
- If optional computer activity context is enabled and actually exposed by the host, use only the exposed information. Never inspect inaccessible activity logs, credentials, or hidden machine state.
- Query the signed-in local Codex CLI through its app-server when an authorized executor is available. Codex quota is a core input to project selection, not optional context. Keep limit windows, reset times, raw credit balance (unit unknown unless supplied), and each banked-reset grant/expiry distinct. Never pool values or promise task cost. CodexBar may optionally add awareness of additional subscriptions; it supplements Codex CLI and is not required.
- Keep host capability adapters and unavailable-source behavior explicit without inventing APIs. The repository is the source and fixture-based tests run in the OpenAI-hosted environment. A repository skill file is not an installation: after validation, install and test the actual skill with dot in a separate step. This environment does not inherit dot's email or chat connectors.

## Out of scope for MVP

- A dashboard, web server, background service, or always-on server.
- Automatic daily invocation or any other scheduler. A host-provided daily invocation can be considered later only with separate user authorization.
- Cross-provider task delegation. This is an advanced later capability requiring a supported executor, permission for the task, and correct subscription billing; seeing quota does not grant access.
- Reading personal email, chats, real quota snapshots, credentials, or inaccessible computer logs into repository fixtures. Use synthetic demo data only.
- Nightwatch dependency. Kyle dropped it to keep scope small.
- Treating the separate Codex skill target as the ChatGPT dot product. The existing local `~/Code/shift` skill is inspiration only; its runtime was not tested and its fuel thresholds/heuristics are not approved requirements.

## Acceptance scenarios

1. **No quota source:** Given a stated goal and useful chat context but no authorized Codex CLI quota read, the skill states quota-aware selection is unavailable and asks for one action to obtain fresh quota or wait; it does not substitute a generic nudge.
2. **Connected project context:** Given exposed email or GitHub context relevant to the goal, the suggestion reflects that evidence and distinguishes observed facts from inference.
3. **Missing, stale, or partial quota:** If no trustworthy fresh Codex CLI quota is available, the skill blocks quota-aware selection, says why, and asks for an authorized fresh read or waits. Within an otherwise usable multi-provider read, stale/missing windows remain unknown and do not invalidate separately fresh data. No missing value is filled in by inference.
4. **Multiple providers and balances:** When fresh Codex CLI data and optional additional-provider data are available, provider/limit/window/reset, raw credit balance, and banked-reset details remain separately attributed. No cross-provider sum or guaranteed task-cost prediction is shown. Banked-reset expiry is awareness only, not eligibility fuel.
5. **Deferred suggestion:** If the user defers a suggestion or asks for no nudge, the assistant acknowledges that choice without repeating the same nudge in the current interaction.
6. **No useful suggestion:** If available context is insufficient or no action is justified, the assistant says so plainly and can ask one focused question or wait; it does not fabricate a task or quota urgency.
7. **Privacy boundary:** Optional activity context is used only when enabled and exposed. No inaccessible logs or credentials are read; fixtures and demo use synthetic project and quota data.
