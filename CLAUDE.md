# Woodhouse Agency Turnkey Reports - AI Assistant Context

**Live:** https://woodhouseagencyturnkeyreports.vercel.app
**Repo:** https://github.com/heygregwood/woodhouse_agency_turnkey_perfomance

---

## Purpose

Ihrie Supply-specific dealer performance dashboard. Shows organic social media metrics for 6 HVAC dealers managed by Woodhouse Turnkey Social Media program.

**Primary User:** Ernie Carson (VP Sales, Ihrie Supply) -- shares results with dealers and uses it in sales meetings.
**Secondary User:** Josh Aycock (Territory Manager, Ihrie Supply)

---

## Current State

- **Data through:** February 19, 2026
- **Active dealers:** 6 (Elite A/C was removed Feb 2026 -- no longer in Ihrie Supply group)
- **Update script:** `update_data.py` at repo root (Python 3, no dependencies)
- **Last updated:** February 20, 2026

---

## How to Update Data

Full instructions in CHANGELOG.md under "How to Update the Dashboard." Quick version:

1. Export two CSVs from Sprout Social (Post Performance + Profile Performance) for the new date range
2. Run `python3 update_data.py --post-csv "..." --profile-csv "..." --dry-run` to preview
3. Run again without `--dry-run` to apply
4. Push to deploy: `git add -A && git commit -m "Update data through [DATE]" && git push`

---

## Stack

- **Static HTML** with Tailwind CSS (CDN) and Chart.js
- **Vanilla JavaScript** for dynamic rendering
- **Dealer data** stored as JSON files in `dealers/`
- **Dashboard data** hardcoded as JS array in `index.html` (patched by update script)
- **Hosted on:** Vercel (auto-deploys from `main` branch)
- **SQLite databases** exist but are not used by the live dashboard (legacy from initial data processing)

---

## Directory Structure

```
woodhouse_agency_turnkey_perfomance/
├── index.html              # Main dashboard (summary cards + dealer table)
├── update_data.py          # Reusable script to process Sprout Social CSV exports
├── CHANGELOG.md            # Update history and how-to-update instructions
├── CLAUDE.md               # This file (AI assistant context)
├── vercel.json             # Vercel config
├── package.json            # NPM config (minimal)
├── .gitignore              # Ignores *.db, *.bak, node_modules/
├── assets/
│   └── img/
│       ├── ihrie-supply.png
│       ├── woodhouse_logo.png
│       └── [dealer-slug].png   # One logo per dealer
├── dealers/                # Individual dealer pages (JSON data + HTML templates)
│   ├── airtech.json        # Dealer data: monthly array, before/after totals, audience
│   ├── airtech.html        # Dealer detail page (loads from JSON, renders chart)
│   ├── kennedys.json
│   ├── kennedys.html       # Has special note about Dec 2025 local content spike
│   ├── scott-plumbing.json / .html
│   ├── metro.json / .html
│   ├── advanced-air.json / .html
│   ├── nc-heating.json / .html
│   ├── elite-ac.json / .html   # Still exists but NOT shown on dashboard
│   └── ...
├── docs/
│   ├── DATABASE_SCHEMA.md
│   └── ...
├── ihrie_organic.db        # SQLite (legacy, not used by live site)
├── ihrie_dealers.db        # SQLite (legacy, not used by live site)
└── dealer/ distributor/ all/   # Empty legacy directories
```

---

## Data Architecture

### How data flows

1. **Sprout Social** -- Greg exports CSVs (Post Performance + Profile Performance)
2. **update_data.py** -- Parses CSVs, merges into existing JSON files, patches index.html
3. **dealers/*.json** -- Each dealer has a JSON file with:
   - `profile`, `slug`, `first_post` -- identity fields
   - `monthly[]` -- array of `{month, posts, impressions, engagements}` entries
   - `before` / `after` -- cumulative totals for pre/post Woodhouse partnership
   - `audience_start` / `audience_end` -- follower counts
4. **index.html** -- Main dashboard reads from a hardcoded JS `dealers` array (patched by the script)
5. **dealers/*.html** -- Detail pages fetch their own `[slug].json` at runtime via `fetch()`

### Key data rules

- All impressions are **organic only** (excludes paid/boosted)
- "Before" = metrics from before the dealer's `first_post` date (never changes)
- "After" = cumulative metrics since joining Woodhouse (grows with each update)
- % Change = `((after - before) / before) * 100`
- Monthly array only tracks posts, impressions, engagements (not messages or video views)
- Messages and video views are only in the before/after totals

---

## Ihrie Supply Dealers (6 Active)

| Dealer | Slug | Partner Since | Notes |
|--------|------|---------------|-------|
| Airtech - Mechanical Services | airtech | Apr 2023 | |
| Scott Plumbing & Heating Co Inc | scott-plumbing | May 2023 | |
| Kennedy's Heating & Air Conditioning | kennedys | Jun 2023 | Dec 2025: started adding own local content |
| Metro Maintenance | metro | Aug 2023 | No pre-Woodhouse presence (footnote 1) |
| Advanced Air Solutions Systems, Inc. | advanced-air | Feb 2024 | Limited pre-Woodhouse activity (footnote 2) |
| NC Heating & Air - Your HVAC Friend | nc-heating | Jan 2024 | |

**Removed:** Elite A/C Solutions (elite-ac) -- removed from dashboard Feb 2026. Files still exist in `dealers/` but are not displayed or updated.

---

## Special Notes on the Dashboard

- **Index.html footnotes:**
  1. Metro Maintenance had no social media presence before partnering with Woodhouse
  2. Advanced Air Solutions had limited social media activity before Woodhouse (1 post, 12 impressions)
- **Kennedy's dealer page:** Has a note explaining that Kennedy's began supplementing Turnkey posts with local content in late Dec 2025, driving a significant impression spike. Chart has a "See Note" annotation at Dec 2025.

---

## Key Metrics Definitions (shown on dashboard)

- **Posts** -- Total content published to social media accounts
- **Impressions** -- Number of times posts appeared in feeds (organic reach only)
- **Engagements** -- Total interactions including likes, comments, shares, and clicks
- **Leads** -- Messages received through social media (potential customer inquiries)
- **% Change** -- Compares current Woodhouse-managed performance to pre-Woodhouse baseline
- **Video Views** -- Number of times videos were watched (dealer detail pages only)
- **Followers** -- People who subscribe to see updates (dealer detail pages only)

---

## Deployment

```bash
cd ~/woodhouse_agency_turnkey_perfomance
git add -A && git commit -m "message" && git push
```

Vercel auto-deploys from `main` branch. Live within ~30 seconds.

**Local preview:**
```bash
npx serve . -l 3001
```

---

## Vercel Project

- **Team:** Greg Wood's projects (`team_zVkY6Ze5orj251f2M3TrURxZ`)
- **Project ID:** `prj_G2vQYK12wBh1zkEtE95qDfD4bBO9`
- **Domains:**
  - woodhouseagencyturnkeyreports.vercel.app (primary)
  - woodhouseagencyturnkeyreports-greg-woods-projects.vercel.app
  - woodhouseagencyturnkeyreports-git-main-greg-woods-projects.vercel.app
- **Deployment Protection:** Disabled (public URL, no login required)
- **Note:** Ernie hit a "link has been locked" error in Dec 2025 due to Vercel protection being enabled. This was resolved and protection is now off.

---

## Related Repos

| Repo | Purpose |
|------|---------|
| `woodhouse_dealer_dashboard` | Full Allied Air dashboard (110 dealers, 17 distributors) |
| `dealer_reports` | Legacy V1 dashboard (deprecated) |
| `woodhouse_social` | Main SaaS platform |
| `prospect_engine` | National HVAC contractor database |

---

## Development Notes

- Static site -- no build step required
- Edit HTML/CSS directly
- All dealer detail pages share the same HTML template (each page loads its own slug.json)
- The `kennedys.html` page has custom logic for the "See Note" chart annotation
- The `elite-ac.html` page has custom logic for an Elite-specific note (now inactive since Elite is hidden)
