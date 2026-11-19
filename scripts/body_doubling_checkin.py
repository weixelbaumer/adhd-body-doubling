#!/usr/bin/env python3
"""Body-doubling check-in ping for Hermes Agent cron (no_agent mode).

Part of the Hermes Agent port of adhd-body-doubling
(original: https://github.com/jankutschera/adhd-body-doubling, MIT).

The skill schedules one one-shot cron job per planned check-in minute. Cron
scripts take no arguments, so this script reads the newest session JSON and
pings only when one of its `checkin_minutes` is due now (+/- TOLERANCE_MIN).
Otherwise it prints nothing (= no delivery), so jobs left over from an ended
or aborted session never ping a later one.

Output: macOS notification with sound (live ping; skipped elsewhere) plus the
check-in text on stdout, which cron delivers. Text language follows the
session's `language` field (de/en, default en). Stdlib only; read-only.

Install: Hermes cron runs scripts only from ~/.hermes/scripts/ - copy it there.
Env: BODY_DOUBLING_HISTORY_DIR (history location), BODY_DOUBLING_NO_NOTIFY=1 (tests).
"""
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
HISTORY = Path(
    os.environ.get("BODY_DOUBLING_HISTORY_DIR")
    or HERMES_HOME / "data" / "adhd-body-doubling" / "history"
)
TOLERANCE_MIN = 3  # cron tick + gateway latency

TEXT = {
    "de": {
        "task": "deine Aufgabe",
        "end_title": "🐱⚡ Zeit um ({total} min)",
        "end_body": "{task} → Session-Autopsie",
        "end": (
            "⏱️ ZEIT UM ({total} min) — {task}\n\n"
            "Session-Autopsie (/adhd-body-doubling done):\n"
            "1. Was hat geholfen?\n"
            "2. Was hat den Fokus gekillt?\n"
            "3. Eine Sache fürs nächste Mal?\n"
            "4. Was hast du tatsächlich geschafft?"
        ),
        "ci_title": "⏰ Check-in ({minute}/{total} min)",
        "ci_head": "⏰ CHECK-IN ({minute} von {total} min) — {task}",
        "ci_step": "Dein erster Micro-Step war: {step}",
        "ci_body": (
            "Wo stehst du GENAU?\n"
            "- Was hast du erledigt?\n"
            "- Was blockiert gerade (falls was)?\n"
            "- Nächster Micro-Step?\n\n"
            "Antworte im Session-Chat oder tippe /adhd-body-doubling für Buttons.\n"
            "Feststecken → „stuck“, Reset → „menu“."
        ),
    },
    "en": {
        "task": "your task",
        "end_title": "🐱⚡ Time's up ({total} min)",
        "end_body": "{task} → session autopsy",
        "end": (
            "⏱️ TIME'S UP ({total} min) — {task}\n\n"
            "Session autopsy (/adhd-body-doubling done):\n"
            "1. What worked?\n"
            "2. What killed your focus?\n"
            "3. One thing for next time?\n"
            "4. What did you actually accomplish?"
        ),
        "ci_title": "⏰ Check-in ({minute}/{total} min)",
        "ci_head": "⏰ CHECK-IN ({minute} of {total} min) — {task}",
        "ci_step": "Your first micro-step was: {step}",
        "ci_body": (
            "Where are you at? SPECIFICALLY:\n"
            "- What did you complete?\n"
            "- What's the current blocker (if any)?\n"
            "- What's the next micro-step?\n\n"
            "Reply in the session chat or type /adhd-body-doubling for buttons.\n"
            'Stuck → "stuck", reset → "menu".'
        ),
    },
}


def newest_open_session():
    """Newest session file (session_id = YYYYMMDD_HHMMSS_x -> name order = time order)."""
    files = sorted(HISTORY.glob("*.json"))
    if not files:
        return None
    try:
        session = json.loads(files[-1].read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if session.get("duration_actual") is not None or session.get("aborted"):
        return None
    return session


def notify(title, body):
    if os.environ.get("BODY_DOUBLING_NO_NOTIFY"):
        return
    def esc(s):
        return s.replace("\\", "\\\\").replace('"', '\\"')
    script = f'display notification "{esc(body)}" with title "{esc(title)}" sound name "Glass"'
    try:
        subprocess.run(["osascript", "-e", script], check=False, timeout=10, capture_output=True)
    except (OSError, subprocess.SubprocessError):
        pass  # not macOS / no GUI session: the chat message still goes out


def main():
    session = newest_open_session()
    if not session or not session.get("checkin_minutes"):
        return
    started = datetime.fromisoformat(str(session["timestamp"]).replace("Z", "+00:00"))
    elapsed = (datetime.now(timezone.utc) - started).total_seconds() / 60
    due = [m for m in session["checkin_minutes"] if abs(elapsed - m) <= TOLERANCE_MIN]
    if not due:
        return
    minute = min(due, key=lambda m: abs(elapsed - m))
    total = session.get("duration_planned") or max(session["checkin_minutes"])
    t = TEXT.get(str(session.get("language") or "en").lower()[:2], TEXT["en"])
    task = (session.get("task_description") or t["task"]).strip()
    step = (session.get("smallest_step") or session.get("first_microstep") or "").strip()
    fmt = {"minute": minute, "total": total, "task": task, "step": step}

    if minute >= total:
        notify(t["end_title"].format(**fmt), t["end_body"].format(**fmt))
        print(t["end"].format(**fmt))
        return

    notify(t["ci_title"].format(**fmt), task)
    lines = [t["ci_head"].format(**fmt)]
    if step:
        lines.append(t["ci_step"].format(**fmt))
    lines += ["", t["ci_body"]]
    print("\n".join(lines))


if __name__ == "__main__":
    main()
