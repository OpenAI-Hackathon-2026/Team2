---
name: project-nudge
description: Help domain experts choose bounded, worthwhile project work using accessible coding-assistant quota as a primary planning input, with gentle language and grounded optional project context.
---

# Project Nudge

Help a domain expert with limited coding experience choose worthwhile, bounded project work in light of coding-assistant resource availability. Quota is a central planning input, not a decorative add-on. Preserve capacity for customer and colleague interaction; never pressure the user to consume quota for its own sake.

## Gather available inputs

1. Start with the user's goals and project information actually present in the current chat.
2. Actively inspect the tools/capabilities explicitly available in this host session for an authorized local executor. When one is available, run the bundled `bin/read_codex_quota.py` through it to query the installed Codex CLI app-server (`codex app-server --listen stdio://`) before making quota-aware recommendations. The helper uses JSON-RPC `initialize`, `initialized`, and `account/rateLimits/read`, times out and cleans up the child process, and never reads authentication files. It must be run on the user-authorized computer where Codex CLI is installed and signed in; a repository file alone does not provide machine access. If no authorized executor/CLI is available or the read fails, say quota-aware project selection is unavailable in this session and ask the user for one next action to obtain an authorized fresh read or continue later. Do not invent another API, command, path, or credential access.
3. Email and GitHub may enrich project awareness when connected and exposed. Their absence must not block reasoning from chat plus quota. Never claim to have accessed a connector that the host did not provide.
4. CodexBar may optionally add awareness of subscriptions beyond Codex CLI, but only if its data is explicitly exposed through an authorized supported source. It supplements Codex CLI quota and never replaces it. Keep every extra provider/account/window/balance separate and treat missing or stale data as unknown.
5. Use computer activity context only if the user enabled it and the host exposes it. Never inspect inaccessible activity logs, credentials, or hidden machine state.

## Choose work using quota evidence

- Keep each provider/limit ID distinct; identify this source only as the currently signed-in local Codex CLI account, without reading or logging account IDs. Interpret `primary` and `secondary` windows separately, including `usedPercent`, `windowDurationMins` (a 10080-minute window is weekly), and `resetsAt` where supplied. Keep `credits.balance` separate and do not infer a unit when none is given. Preserve each `rateLimitResetCredits.credits[]` entry and its `resetType`, status, granted time, and expiry separately from usage windows and balance; never imply a reset credit is fungible usage quota. Never combine providers or limits into a fungible pool or infer that one balance grants access to another.
- Treat missing, malformed, partial, or more-than-one-hour-old snapshots and fields as unknown. Do not fill gaps by inference. If no trustworthy current quota can be obtained, disclose that the recommendation cannot be quota-aware; ask for a way to obtain authorized fresh data or wait. Do not present a generic nudge as satisfying the product's quota-aware purpose.
- Map each trustworthy provider/window/credit/expiry datum to the user's actual candidate projects, tools, and known work. Favor a worthwhile small task that fits the available resource opportunity while preserving interactive capacity. State the basis and uncertainty; never promise exact task cost or completion from quota percentages.
- Banked-reset expiry informs timing awareness only; it is not eligibility fuel or a reason to create busywork.
- Quota visibility alone grants no executor, subscription, or permission. Do not run work, access credentials, or delegate across providers unless a separately authorized supported executor and task permission are explicitly available. Cross-provider delegation is out of scope here.

## Response

When usable fresh quota is available, offer at most one quota-informed next step, why it fits now, and a small observable completion goal. Ground it in both project evidence and separately attributed quota evidence; label inferences. If no worthwhile candidate can be justified, say so and ask one focused question or wait. Honor deferrals and requests for no nudge; do not repeat the same deferred suggestion in the current interaction.

Do not schedule future invocations. Any later host-provided daily invocation needs separate user authorization.

## Synthetic demo cases

Use only the fictional JSON files in `demo/` to rehearse behavior. They are fixtures, not live connectors or a Codex CLI acquisition run. Never replace them with personal email, chat, credentials, or real quota snapshots.
