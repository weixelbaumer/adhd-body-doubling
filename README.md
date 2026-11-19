# ADHD Body Doubling Skill v2.1 🐱⚡ — Hermes Agent port

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.1%2Bhermes.1-green)]()

> **Fork notice:** This is a fork of [jankutschera/adhd-body-doubling](https://github.com/jankutschera/adhd-body-doubling) by Jan Kutschera ([ADHD-founder.com](https://adhd-founder.com)), MIT-licensed. The body doubling protocol — micro-steps, check-ins, push-back, dopamine menu, emergency reset, autopsy — is his work. This fork removes the OpenClaw coupling and adapts the skill for [Hermes Agent](https://hermes-agent.nousresearch.com) — see [Changes in this fork](#changes-in-this-fork).

**A virtual body double for ADHD founders who struggle to start, stay focused, or finish tasks.** Built by [ADHD-founder.com](https://adhd-founder.com) -- German Engineering for the ADHD Brain.

> Body doubling is the practice of working alongside another person to reduce the friction of starting. This skill makes your AI agent your body double -- it gets you started with micro-steps, checks in every 15-25 minutes, pushes back on excuses, and tracks what actually works for your brain.

## Changes in this fork

- **Check-ins actually happen:** the original only announces them. Here every planned check-in is a one-shot Hermes cron job running `scripts/body_doubling_checkin.py` (no LLM call) → macOS notification + check-in message in the session chat. Jobs left over from ended sessions stay silent.
- **No OpenClaw coupling:** history in `~/.hermes/data/adhd-body-doubling/history/` (override: `BODY_DOUBLING_HISTORY_DIR`); OpenClaw metadata and install instructions removed.
- **Hermes runtime rules** (SKILL.md): slash-command mapping, short description, trigger phrases (incl. German), session language for check-in texts (de/en).
- **Button menu:** `/adhd-body-doubling` without arguments opens a Hermes `clarify` menu (duration + task, task choices from today's planner; during a session: status / stuck / done / abort). Commands with arguments run directly; without `clarify` a numbered list is shown.
- **Bug fix:** `scripts/start-session.sh` crashed without arguments ("unbound variable").

## Install (Hermes Agent)

```bash
hermes skills install weixelbaumer/adhd-body-doubling/ --category productivity
cp ~/.hermes/skills/productivity/adhd-body-doubling/scripts/body_doubling_checkin.py ~/.hermes/scripts/
```

Hermes cron only runs scripts from `~/.hermes/scripts/`; the agent also copies it there if missing.

## Quick Start

```
/adhd-body-doubling             # Button menu: pick duration + task (in a session: status / stuck / done / abort)
/adhd-body-doubling start 50    # 50 min deep dive
/adhd-body-doubling start 25    # Quick fire session
/adhd-body-doubling stuck       # When you can't move forward
/adhd-body-doubling done        # End session + learn from it
```

Plain language works too ("body double with me for 25 minutes").

Or run standalone:
```bash
chmod +x scripts/start-session.sh
./scripts/start-session.sh 50
```

## What Happens When You Start a Session

Instead of "let's go" (which never works), the **First Micro-Step Protocol** kicks in:

1. "What are you working on?"
2. "What's the FIRST micro-step?" (under 2 minutes)
3. "What's the SMALLEST possible version of that?"
4. "Do that NOW. I'll wait."

Then check-ins every 15-25 minutes -- with push-back if your answers are vague.

## Commands

| Command | What It Does |
|---------|-------------|
| `/adhd-body-doubling start [time]` | Start with First Micro-Step protocol |
| `/adhd-body-doubling status` | Check-in (expects specifics, not vibes) |
| `/adhd-body-doubling stuck [task]` | Auto micro-task breakdown |
| `/adhd-body-doubling menu` | Dopamine reset (2-5 min science-backed resets) |
| `/adhd-body-doubling done` | End session + autopsy + save to history |
| `/adhd-body-doubling abort` | Kill session (no shame) |
| `/adhd-body-doubling history` | View what worked in past sessions |
| `/adhd-body-doubling roi` | Track revenue vs. time |
| `/adhd-body-doubling founder` | ADHD-founder.com premium info |

## Key Features

- **First Micro-Step Protocol** -- bypasses "I don't know where to start" paralysis
- **Communicative Accountability** -- pushes back on excuses, demands specifics
- **Frequent Check-Ins** -- every 15-25 min, never hourly (ADHD brains need contact)
- **Auto Micro-Task Suggestions** -- when stuck, breaks tasks down automatically
- **Session History** -- tracks patterns so you learn what works for YOUR brain
- **Dopamine Menu** -- 7 quick resets backed by science, not procrastination
- **Emergency Reset** -- 6-step unblock in under 60 seconds

## Works Great With

Pair with [adhd-daily-planner](https://github.com/weixelbaumer/adhd-daily-planner) (Hermes port of [the original](https://github.com/jankutschera/adhd-daily-planner)) for a complete system:

```
/adhd-daily-planner plan        → Pick your ONE thing for the day
/adhd-body-doubling start 50    → Work on it with accountability
/adhd-body-doubling done        → Session autopsy
/adhd-daily-planner reflect     → Evening reflection
```

## Session History

Sessions are tracked in `~/.hermes/data/adhd-body-doubling/history/` (override: `BODY_DOUBLING_HISTORY_DIR`) so you can discover:
- What session lengths work best for your brain
- What time of day you focus best
- Which Dopamine Menu items actually help
- Completion rates by task category

## Philosophy

**"Start > Finish"** -- Every attempt counts.
**"No Shame Zone"** -- Struggles are data, not failure.
**"Communicate"** -- Push back, dig deeper, no excuses.

---

## About ADHD-founder.com (original author)

**"German Engineering for the ADHD Brain"**

This skill is a free, fully functional body doubling system. It's also a taste of what [ADHD-founder.com](https://adhd-founder.com) builds for founders 50+ who are done with generic productivity advice.

- **[Founder Circle Mastermind](https://adhd-founder.com/founder-circle)** -- High-ticket accountability for serious founders
- **Executive Consulting** -- Operational systems for ADHD entrepreneurs
- **Operating System Course** -- Build your own ADHD business framework

**No fluff. No shame. Just systems that work.**

🔗 **[adhd-founder.com](https://adhd-founder.com)**

---

## Contributing

Issues and PRs welcome. Ideas for the body doubling protocol itself are best shared with the original at [jankutschera/adhd-body-doubling](https://github.com/jankutschera/adhd-body-doubling).

## License

MIT -- see [LICENSE](LICENSE). Original work © 2026 ADHD-founder.com (Jan Kutschera); changes in this fork © 2026 Stefan Weixelbaumer.

---

*Body doubling is not about being perfect. It's about not being alone with the struggle.*
