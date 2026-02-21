# Changelog

All notable changes to the Ihrie Supply Dealer Performance Dashboard.

---

## 2026-02-20 — Data Update Through February 19, 2026

**Commit:** `f7227c2`

### What Changed
- Updated all 6 dealer JSON files with new Sprout Social data (Dec 16, 2025 - Feb 19, 2026)
- Updated index.html dashboard with new totals and "Data through February 19, 2026"
- Removed Elite A/C Solutions from the dashboard (no longer in the Ihrie Supply group)
- Changed dealer count from 7 to 6
- Added footnotes on index.html explaining % Change outliers:
  1. Metro Maintenance had no social media presence before Woodhouse
  2. Advanced Air Solutions had limited social media activity before Woodhouse
- Added a note on Kennedy's dealer page explaining the Dec 2025 impression spike (dealer started supplementing Turnkey posts with local content)
- Added "See Note" chart annotation on Kennedy's monthly performance chart at Dec 2025

### New: Reusable Update Script
- Created `update_data.py` -- a Python script to process Sprout Social CSV exports and update the dashboard automatically (see "How to Update" below)

### Data Summary (After Totals, Cumulative Since Partnership)
| Dealer | Posts | Impressions | Engagements | Leads |
|--------|-------|-------------|-------------|-------|
| Airtech | 346 | 4,123 | 136 | 68 |
| Scott Plumbing | 390 | 37,178 | 2,923 | 123 |
| Kennedy's | 409 | 68,402 | 5,774 | 334 |
| Metro Maintenance | 527 | 22,978 | 2,848 | 304 |
| Advanced Air | 228 | 1,298 | 17 | 14 |
| NC Heating | 200 | 6,820 | 249 | 42 |

---

## 2025-12-15 — Initial Dashboard Build

**Commits:** `65d53de` through `7fd626a`

### What Was Built
- Static HTML dashboard with Tailwind CSS and Chart.js
- Main index.html with summary cards and dealer performance table
- Individual dealer detail pages (HTML + JSON) with before/after comparison tables, audience growth, and monthly performance charts
- Ihrie Supply + Woodhouse co-branding in header and footer
- Dark theme (slate-900) with Woodhouse blue (#12ace2) accents
- Clickable dealer rows linking to individual dealer pages
- "Woodhouse Start" annotation line on monthly charts
- Deployed to Vercel at woodhouseagencyturnkeyreports.vercel.app

### Dealers Included (7 at launch)
1. Airtech - Mechanical Services
2. Scott Plumbing & Heating Co Inc
3. Kennedy's Heating & Air Conditioning
4. Metro Maintenance
5. Advanced Air Solutions Systems, Inc.
6. Elite A/C Solutions
7. NC Heating & Air - Your HVAC Friend

### Data
- Covered through December 15, 2025
- All metrics organic only (excludes paid/boosted)
- Data sourced manually from Sprout Social exports

---

# How to Update the Dashboard

## What You Need

1. **Two CSV exports from Sprout Social** covering the new date range (from the day after the last update through today):
   - **Post Performance** -- export for all Ihrie/Turnkey dealers. Must include: Profile, Date, Organic Impressions, Engagements, Organic Video Views
   - **Profile Performance** -- export for all Ihrie/Turnkey dealers. Must include: Profile, Date, Received Messages (Total), Audience

2. **Python 3** (already installed in WSL)

## Steps

### 1. Export from Sprout Social

In Sprout Social, go to Reports:

**Post Performance:**
- Report type: Post Performance
- Sources: Select all 6 Ihrie/Turnkey dealer profiles
- Date range: Day after last update through today
- Export as CSV

**Profile Performance:**
- Report type: Profile Performance
- Sources: Same 6 profiles
- Date range: Same as above
- Export as CSV

### 2. Run the Update Script

```bash
cd ~/woodhouse_agency_turnkey_perfomance

# Preview first (no files changed)
python3 update_data.py \
  --post-csv "/mnt/c/Users/GregWood/Downloads/Post Performance.csv" \
  --profile-csv "/mnt/c/Users/GregWood/Downloads/Profile Performance.csv" \
  --dry-run

# If the numbers look right, run for real
python3 update_data.py \
  --post-csv "/mnt/c/Users/GregWood/Downloads/Post Performance.csv" \
  --profile-csv "/mnt/c/Users/GregWood/Downloads/Profile Performance.csv"
```

The script will:
- Create `.bak` backups of all files before modifying them
- Add new monthly entries to each dealer's JSON file
- Update cumulative "after" totals (posts, impressions, engagements, video views, messages)
- Update audience follower counts
- Patch index.html with new dealer data and "Data through" date
- Print a before/after summary so you can verify the numbers

### 3. Review and Deploy

```bash
# Check the site locally
npx serve . -l 3001

# If it looks good, push to deploy
git add -A && git commit -m "Update data through [DATE]" && git push
```

Vercel auto-deploys from main. The live site updates within ~30 seconds.

## Script Options

| Flag | Description |
|------|-------------|
| `--post-csv PATH` | (Required) Path to Post Performance CSV |
| `--profile-csv PATH` | (Required) Path to Profile Performance CSV |
| `--data-through "March 15, 2026"` | Override the display date (auto-detected from CSV if omitted) |
| `--dry-run` | Preview changes without writing any files |

## Important Notes

- The script **merges** new data into existing data. It does not replace anything.
- If the last month in the existing data overlaps with the new CSV (e.g., you're adding Dec 16-31 to a file that already has Dec 1-15), the script adds the new values to the existing month. No double-counting.
- "Before" totals are never changed -- all new data is post-partnership.
- `.bak` files are created but gitignored. They're there if you need to roll back.
- Elite A/C JSON and HTML still exist in `dealers/` but are not shown on the dashboard or updated by the script.

## Sprout Social Export Tips

- Make sure "Sources" in Sprout Social includes exactly the 6 active Ihrie dealers
- The Post Performance CSV has one row per post -- the script counts posts automatically
- The Profile Performance CSV has one row per day per profile
- If the last day's Audience column is blank, that's normal -- the script handles it
