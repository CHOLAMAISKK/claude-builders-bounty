#!/usr/bin/env python3
"""Generate structured CHANGELOG.md from git history.
Usage: python3 generate_changelog.py [SINCE_TAG]
"""
import subprocess, sys, re
from datetime import datetime

CATEGORIES = {
    "feat": "Added", "add": "Added", "new": "Added",
    "fix": "Fixed", "bug": "Fixed",
    "change": "Changed", "update": "Changed", "refactor": "Changed",
    "remove": "Removed", "delete": "Removed",
}

def get_commits(since_tag=None):
    cmd = ["git", "log", "--no-merges", "--pretty=%H|%s|%ad", "--date=short"]
    if since_tag:
        cmd.append(f"{since_tag}..HEAD")
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    entries = []
    for line in out.splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            entries.append({"hash": parts[0][:7], "msg": parts[1], "date": parts[2]})
    return entries

def categorize(msg):
    m = re.match(r"^(\w+)(?:\(.*?\))?:\\s*(.+)", msg)
    if m:
        prefix, body = m.group(1).lower(), m.group(2)
        return CATEGORIES.get(prefix, "Changed"), body
    for kw, cat in CATEGORIES.items():
        if msg.lower().startswith(kw):
            return cat, msg
    return "Changed", msg

def generate(since_tag=None):
    commits = get_commits(since_tag)
    groups = {"Added": [], "Fixed": [], "Changed": [], "Removed": []}
    for c in commits:
        cat, desc = categorize(c["msg"])
        groups[cat].append(f"- {desc} ({c['hash']})")
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"# CHANGELOG\n\n## [Unreleased] - {today}\n"]
    for cat, items in groups.items():
        if items:
            lines.append(f"\n### {cat}\n\n")
            lines.extend(item + "\n" for item in items)
    return "".join(lines)

if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else None
    print(generate(tag))
