---
name: adhd-body-doubling
version: 2.1.1+hermes.2
description: "Use when user wants body doubling/focus help. ADHD sessions."
homepage: https://github.com/weixelbaumer/adhd-body-doubling
author: "Jan Kutschera / ADHD-founder.com (original); Stefan Weixelbaumer (Hermes port)"
license: MIT
keywords: [adhd, body-doubling, focus-session, accountability, pomodoro, productivity, founders, neurodivergent, executive-function, task-initiation, procrastination, focus, micro-steps, dopamine]
metadata:
  hermes:
    tags: [adhd, body-doubling, focus, accountability, productivity]
    related_skills: [adhd-daily-planner]
  upstream: "https://github.com/jankutschera/adhd-body-doubling (v2.1.1, Jan Kutschera / ADHD-founder.com, MIT)"
---

# ADHD Body Doubling Skill v2.1 🐱⚡

**Hermes Agent port of [adhd-body-doubling](https://github.com/jankutschera/adhd-body-doubling) by Jan Kutschera / [ADHD-founder.com](https://adhd-founder.com) (MIT)**
*"German Engineering for the ADHD Brain"*

---

## What This Skill Does

Provides punk-style body doubling sessions for ADHD founders that:
- Gets you started with micro-steps (not just "let's go")
- Keeps you accountable -- pushes back on excuses, asks follow-ups
- Breaks tasks into micro-steps when you're stuck
- Checks in every 15-25 minutes (never hourly)
- Tracks session history so you learn what works for YOUR brain

## Core Philosophy

**"Start > Finish"** - Every attempt counts
**"No Shame Zone"** - Struggles are data, not failure
**"Communicate"** - Push back, dig deeper, don't let excuses slide

---

## Hermes Agent Runtime (read first)

This fork runs on [Hermes Agent](https://hermes-agent.nousresearch.com). Where the sections below differ, this one wins.

**When to use:** body doubling, focus session, accountability while working, help starting a task, pomodoro-style work; "I can't focus", "I'm stuck", "help me start", "I keep procrastinating" — in any language (German, e.g.: "komm nicht in die Gänge", "kann nicht anfangen", "Fokus-Session").

- **Invoke:** `/adhd-body-doubling` alone opens the button menu (next rule); with a command (`/adhd-body-doubling start 50`, `done`, …) it runs directly, no menu. Hermes registers the skill name as the slash command, so every `/body-doubling <cmd>` below means `/adhd-body-doubling <cmd>`. Plain language works too.
- **Button menu:** when the invocation carries no instruction, or the user asks for body doubling without naming a duration, call `clarify` instead of asking in prose. Labels in the session language.
  - *Active session* (newest history JSON with `duration_actual: null`, not `aborted`, started less than `duration_planned` + 30 min ago): one single-select question, choices status · stuck · done · abort (de: `Stand melden` · `Ich hänge` · `Fertig` · `Abbrechen`). The free-text row covers the rest (e.g. `menu`). Then run that command.
  - *Otherwise:* ONE `clarify` call with two questions. (1) Duration: `25 min` · `50 min` · `15 min – just start` · `90 min` (de: `25 Min` · `50 Min` · `15 Min – nur anfangen` · `90 Min`). The first choice is shown as recommended: 25, unless at least 3 finished sessions in history show a better average `completion_rate` for another length. The free-text row takes any other length. (2) Task: choices = today's planner ★ plus up to three open ⚡ quick wins (Planner sync), each ≤ 60 characters; without a planner file, ask it open (no choices). Then continue the session flow at question 2 (first micro-step).
  - Buttons are for choices only. Micro-step questions, push-back, check-in answers and the autopsy stay free text: the user's own words are the method.
  - Fallback: `clarify` unavailable or outcome `undelivered` / `timed_out` → the same options as a numbered list, the user replies with the number. Outcome `cancelled` = not now: one short line, no push-back.
- **Language:** answer in the user's language and store it as `language` (ISO code, e.g. `de`) in the session JSON; the check-in messages use it. Keep the push-back; no shaming.
- **History:** `$BODY_DOUBLING_HISTORY_DIR`, default `~/.hermes/data/adhd-body-doubling/history/`, one `<session_id>.json` per session, schema = the JSON in `scripts/start-session.sh`. `session_id` = `YYYYMMDD_HHMMSS_<4 hex>` (file-name order = time order). Hermes adds `language`, `checkin_minutes` and `cron_job_ids`.
- **Planner sync** (if today's `adhd-daily-planner` file exists — `$ADHD_PLANNER_DIR`, default `~/.hermes/data/adhd-daily-planner/daily/YYYY-MM-DD.md`): at `start`, offer its ★ and open ⚡ quick wins as answers to question 1 (picking beats inventing); at `done`, apply the planner's `done <task>` rule to the session task.
- **Objection to the task itself** (the user does not want its outcome) is a decision, not an excuse: skip the push-back and ask who requires it and what happens if it is skipped. Optional → drop it or switch to another planned task. Required → shrink it to "correct and minimal, no polish" (never deliberately bad — that backfires) and continue with question 2.
- **Check-ins are real cron jobs. Never announce a check-in that is not scheduled.** After micro-step 3, before "Do that NOW":
  1. Write the session JSON: `timestamp` = now (UTC ISO), `duration_planned`, `checkin_minutes`, `language`, `duration_actual: null`, `aborted: false`, rest per schema.
  2. Per minute `m` in `checkin_minutes`: `cronjob_manage` action=create, `schedule="in {m}m"`, `name="body-doubling {session_id} @{m}"`, `script="body_doubling_checkin.py"`, `no_agent=true`, `wrap_response="off"`, `prompt="body-doubling check-in ping"` (required on create, ignored by no_agent), no `deliver` (= this chat). Store the returned job IDs in `cron_job_ids`.
  3. Then announce the timer with the real check-in times.
- **checkin_minutes** (last entry = end ping): 15 → `[10, 15]` · 25 → `[15, 25]` · 50 → `[15, 35, 50]` · 90 → `[20, 45, 70, 90]` · otherwise every ≤ 25 min plus the end.
- **What fires:** a macOS notification with sound (other systems: chat only) + the check-in text as a note in the session chat. No LLM call, so it also works when model quota is exhausted. The script stays silent unless a planned minute of the newest open session is due (±3 min), so leftover jobs never ping a later session.
- **User answers a check-in:** run the check-in / push-back protocol; append to `check_ins`, increment `check_ins_completed`.
- **done / abort:** `cronjob_manage` remove every ID in `cron_job_ids` (fired one-shots too, keeps the job list clean); then fill `duration_actual`, `energy_end`, `completion_rate`, `what_worked`, `what_didnt`, `dopamine_menu_used` and run the autopsy (done), or set `aborted: true` (abort). Infer what you can (duration, completion) instead of asking; ask the autopsy once as one optional block — if the user moves on, drop it.
- **`done` ends the session, not the day.** "Enough for today" right after a task means enough of that kind of task: offer a dopamine-menu reward, then the next open task from today's plan. Never offer to carry open tasks over from here — that belongs to the planner's evening `reflect`.
- **history:** read the JSON files and report patterns: best session length, time of day, completion by category, which dopamine items helped.
- **Script install:** Hermes cron runs scripts only from `~/.hermes/scripts/`. Canonical copy: `scripts/body_doubling_checkin.py` in this skill; if `~/.hermes/scripts/body_doubling_checkin.py` is missing or differs, copy it there before scheduling.

---

## Commands

| Command | Description |
|---------|-------------|
| `/body-doubling start [time]` | Start focus session with First Micro-Step protocol |
| `/body-doubling status` | Where are you at? (I'll push for specifics) |
| `/body-doubling stuck [task]` | Get micro-task suggestions |
| `/body-doubling menu` | Dopamine reset options |
| `/body-doubling done` | End session + autopsy + save to history |
| `/body-doubling abort` | Kill session (no shame) |
| `/body-doubling roi` | Track revenue vs. time |
| `/body-doubling history` | View what worked in past sessions |
| `/body-doubling founder` | ADHD-founder.com premium info |

---

## Session Flow (How to Behave)

**This is how a session MUST play out. Follow this exactly.**

**User:** `/body-doubling start 50`

**Response:**
```
🐱⚡ BODY DOUBLING SESSION (50 min)

1️⃣ What are you working on?
> [User replies]

2️⃣ What's the FIRST micro-step?
   (Something under 2 minutes)
> [User replies]

3️⃣ That's good, but what's the SMALLEST possible version of that?
> [User replies]

4️⃣ Perfect. Do that NOW. I'll wait.

   ⚡ Timer started. Check-ins at 15 and 35 min.
```

**At 15 min check-in:**
```
⏰ CHECK-IN (15 min)

Where are you at? SPECIFICALLY:
- What did you complete?
- What's the current blocker (if any)?
- What do you need to finish the micro-step?

Be honest. I'll know if you're making excuses.
```

**When user says "I'm stuck":**
```
🛑 STOP. Let's break this down.

You're not stuck - you just haven't found the entry point yet.

MICRO-TASK OPTIONS:
1. Write ONE sentence/line of the thing
2. Open the file/app and stare at it for 60 seconds
3. List 3 things you DON'T need to do for this task
4. Do the part you know how to do, skip the hard part
5. Set a timer for 5 min and promise to stop after

Which one? Pick NOW.
```

---

## Check-In Schedule

- **15 min sessions:** 1 check-in at 10 min
- **25 min sessions:** 1 check-in at 15 min
- **50 min sessions:** Check-ins at 15 and 35 min
- **90+ min sessions:** Check-ins every 20-25 min
- **NEVER** go more than 25 minutes without contact

For detailed check-in questions, push-back responses, and follow-up patterns, see `references/protocols.md`.

---

## When User Is Stuck: Auto Micro-Task Protocol

When the user says they're stuck, automatically offer:
1. **Break it down** - "What's the smallest component?"
2. **Entry points** - "Where could you start even if you don't finish?"
3. **2-minute version** - "What could you do in 120 seconds?"
4. **Pre-mortem** - "What would make this fail? Let's prevent that."
5. **Delegation check** - "Do YOU need to do this?"

For full micro-task suggestion protocol, see `references/protocols.md`.

---

## Dopamine Menu (Quick Resets)

When user needs a reset, offer ONE of these (2-5 min):
1. Physical Reset - jumping jacks, stretch, walk
2. Sensory Swap - change environment, different music
3. Micro-Win - complete one tiny task
4. External Input - 1 min of motivating content
5. Brain Dump - write everything in head for 2 min
6. Hydrate - water, splash face
7. Permission Slip - 5 min of nothing, then back

**Rule: Pick ONE. Do it. Back to work.**

---

## Emergency Reset Protocol

When TOTALLY blocked:
1. Stop (30 sec) - hands off keyboard
2. Breathe (30 sec) - 3 deep breaths
3. Ask (1 min) - "What's the ONE thing I'm avoiding?"
4. Shrink (1 min) - make the task 10x smaller
5. Promise (30 sec) - "I will do this for 5 minutes only"
6. Go - start the tiny task

**If still blocked after 5 min → End session. No shame.**

---

## Session History

Sessions are tracked in: `~/.hermes/data/adhd-body-doubling/history/` (override: `$BODY_DOUBLING_HISTORY_DIR`)

Tracks: task category, time of day, energy levels, completion rate, what worked/didn't, dopamine menu usage.

For the full JSON schema, see `references/protocols.md`.

---

## Session Autopsy (End of Session)

After every session, ask:
1. What worked? (What helped you focus?)
2. What didn't? (What killed your focus?)
3. One thing for next time?
4. What did you actually accomplish?

---

## Best Practices

1. **Be honest** - I can't help if you lie to me
2. **Start small** - 25 minutes is a valid session
3. **Answer follow-ups** - The more specific, the better
4. **Embrace the push-back** - I'm not being mean, I'm being useful
5. **Let me break tasks down** - Micro-steps are magic
6. **Review history monthly** - Patterns reveal your optimal setup

---

## About ADHD-founder.com

**"German Engineering for the ADHD Brain"**

This skill is a free, fully functional body doubling system. It's also part of what [ADHD-founder.com](https://adhd-founder.com) builds for founders 50+ who need systems, not life hacks.

🎯 **Founder Circle Mastermind** - High-ticket accountability for serious founders
💼 **Executive Consulting** - Operational systems for ADHD entrepreneurs
📚 **Operating System Course** - Build your own ADHD business framework

🔗 **[ADHD-founder.com](https://adhd-founder.com)** | **[Founder Circle](https://adhd-founder.com/founder-circle)**

---

*Body doubling is not about being perfect. It's about not being alone with the struggle.*
