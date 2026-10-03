---
name: project-nudge
description: Help Kyle or a domain expert make grounded project progress with quota-aware pacing. Use directly for quota or project-priority questions, when explicitly asked to plan project work around usage limits, and selectively during relevant project conversations where resource availability can improve the next-step recommendation. Keep quota details unobtrusive unless requested or materially relevant.
---

# Project Nudge

Help a domain expert with limited coding experience choose worthwhile, bounded project work in light of coding-assistant resource availability. Quota is a core planning input when choosing project work, but it should not dominate unrelated conversation. Preserve capacity for customer and colleague interaction; never pressure the user to consume quota for its own sake.

## Choose the right mode

- **Direct quota or project-priority request:** Refresh quota now through the authorized local reader when available. Give clearly attributed current figures when asked, then relate them to actual candidate work.
- **Explicit project planning, including an already authorized scheduled invocation:** Use available fresh quota to shape the plan. A schedule may invoke this skill, but the skill does not create or manage schedules.
- **Ambient use:** When the host selects this skill during a relevant project conversation, quietly consider recent quota already available in the conversation/session. Let it inform scope or pacing when useful; usually omit numeric details. Do not launch a local quota read for every casual reply. Refresh only when the user is making a project-priority decision or a potentially material limit/reset makes freshness important.
- **Unrelated conversation:** Do not introduce quota or project nudges. Do not poll in the background, run as a daemon, or create an always-on process.

## Gather available inputs

1. Start with the user's goals and project information actually present in the current chat.
2. For a direct quota query or a project-planning decision that warrants a fresh read, inspect the tools/capabilities explicitly available in this host session for an authorized local executor. When available, run the bundled `bin/read_codex_quota.py` to query the installed Codex CLI app-server (`codex app-server --listen stdio://`). It uses JSON-RPC `initialize`, `initialized`, and `account/rateLimits/read`, times out and cleans up the child process, and never reads authentication files. Run only on the user-authorized computer where Codex CLI is installed and signed in. A repository file alone does not provide machine access. Never invent APIs, commands, paths, or credential access.
3. Email and GitHub may enrich project awareness when connected and exposed. Their absence must not block reasoning from chat plus quota. Never claim access to a connector the host did not provide.
4. CodexBar may optionally add awareness of subscriptions beyond Codex CLI. For a direct quota request or relevant project-planning decision, if an authorized local executor is available, run `python3 .agents/skills/project-nudge/bin/read_codexbar_usage.py` after the Codex CLI read. This adapter reads CodexBar usage JSON; it must not read credentials. Exit code 2 or unavailable data means CodexBar is simply unavailable: keep using any trustworthy Codex CLI result and do not fail the whole recommendation. CodexBar supplements Codex CLI quota, never replaces it. Ambiently, do not launch this extra read on every casual reply; use recent exposed data or refresh only when the decision warrants it.
5. Use computer activity context only if enabled by the user and actually exposed by the host. Never inspect inaccessible activity logs, credentials, or hidden machine state.

## Interpret quota

- Keep each provider/limit ID distinct. Identify the Codex source only as the currently signed-in local CLI account; do not read or log account IDs. Preserve CodexBar provider, account, windows, credits, and subscription dates as returned, without pooling. Accept CodexBar data only when its source timestamp is no more than one hour old; stale, malformed, or partial fields remain unknown. A CodexBar failure does not invalidate fresh Codex CLI quota.
- Interpret `primary` and `secondary` windows separately, including `usedPercent`, `windowDurationMins` (10080 minutes is weekly), and `resetsAt` where supplied. Keep `credits.balance` separate; do not infer an unprovided unit.
- Preserve each `rateLimitResetCredits.credits[]` entry and its reset type, status, grant time, and expiry separately from rate windows and balance. Do not imply a reset credit is fungible usage quota.
- Treat missing, malformed, partial, or more-than-one-hour-old data as unknown. Never infer missing values. Ambiently, unknown/unavailable quota quietly means no quota-specific claim or nudge; do not repeatedly prompt the user to configure access. For a direct quota request, plainly disclose that a trustworthy read is unavailable and ask for one way to obtain an authorized fresh read or offer to wait.
- Map trustworthy quota evidence to actual candidate projects and bounded tasks. Never pool providers, predict exact task cost, or pressure the user to exhaust capacity. Banked-reset expiry informs timing only; it is not eligibility fuel or a reason for busywork.
- Quota visibility alone grants no executor, subscription, or permission. Do not run project work or delegate across providers without a separately authorized executor and task permission.

## Respond gently

When project work is relevant, offer at most one useful next step, why it fits now, and a small observable completion goal. In ambient mode, let quota shape the size or pacing quietly; show exact numbers only when the user asks or a specific limit/reset/expiry materially affects the choice. Label inferences and ground claims in available context.

If no worthwhile step is supported, do not manufacture one. Honor deferrals and requests for no nudge across the accessible conversation history; do not repeat or rephrase a deferred suggestion as a workaround. If the user asks for no nudge, simply continue the conversation normally.

This skill does not schedule itself, create schedules, poll in the background, or run as an always-on service. An existing, user-authorized host schedule may invoke it.

## Synthetic demo cases

Use only the fictional JSON files in `demo/` to rehearse behavior. They are fixtures, not live connectors or a Codex CLI acquisition run. Never put personal messages, credentials, or real quota snapshots in the repository.
