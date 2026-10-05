---
name: generate-changelog
description: Generate a structured CHANGELOG.md from git history
---
# Generate CHANGELOG Skill

## Usage
```bash
python3 generate_changelog.py          # all commits
python3 generate_changelog.py v1.0.0   # since tag
```

## Acceptance Criteria
- [x] Works via `python3 generate_changelog.py`
- [x] Fetches commits since the last git tag
- [x] Auto-categorizes into Added / Fixed / Changed / Removed
- [x] Outputs properly formatted CHANGELOG.md
- [x] Tested on real Git repository
