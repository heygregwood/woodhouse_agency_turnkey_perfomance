# Quick Commands

Dev environment quick reference for Woodhouse Agency Turnkey Reports (Ihrie Supply dashboard).

---

## Environment

- **Machine:** Windows 11 + WSL2 Ubuntu
- **User:** heygregwood
- **Repo:** `~/woodhouse_agency_turnkey_perfomance`
- **Live URL:** https://woodhouseagencyturnkeyreports.vercel.app

---

## Bash Aliases

```bash
gp        # git pull
gs        # git status
ga        # git add .
gpush     # git push
```

---

## Git Commands

```bash
# Check status
gs

# Pull latest
gp

# Stage everything
ga

# Commit
git commit -m "message"

# Push (auto-deploys to Vercel)
gpush

# Full workflow
ga && git commit -m "message" && gpush
```

---

## Common Tasks

```bash
# Navigate to repo
cd ~/woodhouse_agency_turnkey_perfomance

# View files
ls -la

# Edit index.html
code index.html   # VS Code
nano index.html   # Terminal editor

# Test locally (just open in browser)
# Open index.html in Chrome/Edge
```

---

## File Structure

```
~/woodhouse_agency_turnkey_perfomance/
├── index.html              # Main Ihrie dashboard
├── assets/img/             # Logos
├── dealers/                # Individual dealer JSON + HTML
├── ihrie_organic.db        # SQLite data
└── docs/                   # Documentation
```

---

## Deployment

Vercel auto-deploys on push to `main`:

```bash
# Make changes, then:
ga && git commit -m "Update dashboard" && gpush

# Check deployment status
# https://vercel.com/greg-woods-projects/woodhouse_agency_turnkey_reports
```

---

## File Paths (for Claude/AI tools)

WSL path format for Desktop Commander:
```
\\wsl$\Ubuntu\home\heygregwood\woodhouse_agency_turnkey_perfomance\[file]
```

**DO NOT use:**
- `C:\Users\greg\...`
- `/home/heygregwood/...`
- `~/...`

---

## Data Updates

When new Sprout Social data comes in:

1. Export Post Performance CSV
2. Export Profile Performance CSV
3. Run Python scripts to regenerate data
4. Update JSON files in `dealers/`
5. Push to deploy

---

## Ihrie Supply Dealers (7)

1. Airtech - Mechanical Services
2. Scott Plumbing & Heating Co Inc
3. Kennedy's Heating & Air Conditioning
4. Metro Maintenance
5. Advanced Air Solutions Systems, Inc.
6. Elite A/C Solutions
7. NC Heating & Air - Your HVAC Friend

---

## Recovery

```bash
# Reset to last good commit
gp
git reset --hard origin/main

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard changes to specific file
git checkout -- path/to/file
```

---

## Vercel Dashboard

```
https://vercel.com/greg-woods-projects/woodhouse_agency_turnkey_reports
```

- View deployments
- Check logs
- Manage domain settings
- Toggle auth protection (Settings → Deployment Protection)

---

*See CLAUDE.md for full project context.*
