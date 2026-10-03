# Project Nudge examples

Five short, fictional scenarios for presenting Project Nudge. Every name, project, prompt, quota snapshot, and response below is synthetic; none is a live account or personal data. Responses are illustrative, not guaranteed wording.

The implemented primary path is a fresh read from the currently signed-in local Codex CLI through its app-server, when the host provides an authorized executor. Project context is limited to what the host actually exposes. CodexBar is an optional adapter for separately exposed additional providers; it supplements Codex CLI and is not live-verified in these examples. No example schedules work or runs a task. A future daily invocation would require a separately authorized host scheduler; any schedule shown below is only a planning request in chat.

## 1. A quota-aware, bounded task

**For:** Someone deciding what small project task to tackle now.

**Scenario / prompt:** With permission, the host supplies a fresh synthetic Codex CLI snapshot: the current session window is 42% used and resets in 25 minutes; the weekly window is 35% used. Chat says a colleague can verify a draft fitment note. “What’s one useful thing I can do before I check this with my colleague?”

**Sample response:** “Draft a one-paragraph fitment note for your colleague to check. The project context points to a real review path, and the fresh session window resets soon; a short draft is a reasonable next step, though quota percentages can’t predict its cost. Done when the note is ready for review.”

**Why helpful:** Connects a real project need to one observable step without promising how much quota it will use.

## 2. Planning a few days ahead

**For:** Someone balancing project work with customer and colleague time.

**Scenario / prompt:** “Help me plan the next three days around one small project task, time for customer calls, and a colleague review.” The host has the same fresh synthetic Codex CLI reading as above. This asks for a plan in the current conversation; it does not create calendar events, schedule an invocation, or perform work.

**Sample response:** “Day 1: draft the fitment note and send it for review. Day 2: leave room for customer calls; capture any new questions. Day 3: revise the note if your colleague responds. The quota read is only a current snapshot, so check it again before choosing later coding work.”

**Why helpful:** Turns a near-term goal into a light plan while making clear that today’s quota data does not predict future availability.

## 3. A gentle contextual suggestion

**For:** Someone who appreciates an occasional nudge but does not want quota pressure.

**Scenario / prompt:** The user asks, “Anything useful I can do next?” Chat mentions that fitment questions recur and a colleague offered to review a note. Fresh synthetic Codex CLI quota is available, but the user has not asked to maximize usage.

**Sample response:** “If it fits your day, you could jot down the fitment details you already know and mark anything your colleague should confirm. That gives the review a useful starting point. No need to start a coding task just because quota is available.”

**Why helpful:** Uses project context gently and treats quota as planning context, not a reason to manufacture work.

## 4. Optional additional providers

**For:** Someone who has more than one coding-assistant subscription and wants the sources kept clear.

**Scenario / prompt:** The host has a fresh synthetic Codex CLI reading and, separately, an authorized CodexBar adapter snapshot for another provider. The second provider’s weekly reading is more than an hour old. “Could this affect which small task I choose?”

**Sample response:** “The fresh Codex CLI reading can inform a small task. The other provider’s snapshot is stale, so its quota is unknown. I’d keep the fitment note as a reasonable option based on your project context; I can’t combine the providers or infer a task cost.”

**Why helpful:** Shows how the optional adapter can add context while keeping providers separate and stale data unknown. CodexBar support is optional and not live-verified here.

## 5. Missing quota: defer or get a fresh read

**For:** Someone whose host cannot currently provide an authorized quota reading.

**Scenario / prompt:** “Help me pick a small coding task for the belt reference.” No authorized executor or fresh Codex CLI snapshot is available. The chat contains project context, but no usable quota evidence.

**Sample response:** “I can’t make a quota-aware task choice without a fresh authorized Codex CLI reading. You can enable an authorized read in this host or come back later. I’ll wait; I won’t guess from project context alone.”

**Why helpful:** Makes the limitation plain and avoids presenting a generic suggestion as quota-aware.
