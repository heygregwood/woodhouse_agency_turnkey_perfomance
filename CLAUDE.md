# Woodhouse Agency Turnkey Reports - AI Assistant Context

**Live:** https://woodhouseagencyturnkeyreports.vercel.app  
**Repo:** https://github.com/heygregwood/woodhouse_agency_turnkey_perfomance

---

## Purpose

Ihrie Supply-specific dealer performance dashboard. Shows organic social media metrics for 7 HVAC dealers managed by Woodhouse Turnkey Social Media program.

**Primary User:** Ernie Carson (Ihrie Supply) - uses this to share results with dealers like Kennedy's.

---

## File Access (CRITICAL for Desktop Commander)

Use this path format:
```
\\wsl$\Ubuntu\home\heygregwood\woodhouse_agency_turnkey_perfomance\[file_path]
```

**DO NOT use:** `C:\Users\...`, `/home/heygregwood/...`, or `~/...`

---

## Stack

- **Static HTML** with Tailwind CSS (CDN)
- **SQLite databases** for data storage
- **Vanilla JavaScript** for dynamic rendering
- **Hosted on:** Vercel

---

## Directory Structure

```
woodhouse_agency_turnkey_perfomance/
├── index.html              # Main Ihrie Supply dashboard
├── vercel.json             # Vercel config
├── package.json            # NPM config (minimal)
├── .gitignore
├── ihrie_organic.db        # SQLite - Organic impressions data
├── ihrie_dealers.db        # SQLite - Dealer performance data
├── assets/
│   └── img/
│       ├── ihrie-supply.png
│       ├── woodhouse_logo.png
│       └── [dealer logos]
├── dealers/                # Individual dealer JSON + HTML files
│   ├── airtech.json
│   ├── airtech.html
│   ├── kennedys.json
│   ├── kennedys.html
│   └── ...
├── dealer/                 # (empty or legacy)
├── distributor/            # (empty or legacy)
└── all/                    # (empty or legacy)
```

---

## Data Sources

Data pulled from Sprout Social exports:
- `Post_Performance_ALL_DEALERS_*.csv` - Individual post metrics
- `Profile_Performance_ALL_DEALERS_*.csv` - Aggregate profile metrics

**Key metrics tracked:**
- Posts (count)
- Organic Impressions (excludes paid/boosted)
- Engagements (likes, comments, shares, clicks)
- Leads (received messages)
- % Change (before vs after Woodhouse partnership)

---

## SQLite Database Schema

### ihrie_organic.db

```sql
CREATE TABLE monthly_metrics (
    id INTEGER PRIMARY KEY,
    dealer_name TEXT,
    month TEXT,           -- YYYY-MM format
    posts INTEGER,
    organic_impressions INTEGER,
    engagements INTEGER,
    organic_video_views INTEGER,
    messages INTEGER
);

CREATE TABLE dealer_summary (
    id INTEGER PRIMARY KEY,
    dealer_name TEXT UNIQUE,
    first_post_date TEXT,
    total_posts INTEGER,
    total_impressions INTEGER,
    total_engagements INTEGER,
    total_video_views INTEGER,
    total_messages INTEGER,
    before_posts INTEGER,
    before_impressions INTEGER,
    before_engagements INTEGER,
    before_video_views INTEGER,
    before_messages INTEGER,
    after_posts INTEGER,
    after_impressions INTEGER,
    after_engagements INTEGER,
    after_video_views INTEGER,
    after_messages INTEGER,
    pct_change REAL
);
```

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

## Key Metrics Definitions (shown on dashboard)

- **Posts** — Total content published to social media accounts
- **Impressions** — Number of times posts appeared in feeds (organic reach only)
- **Engagements** — Total interactions including likes, comments, shares, and clicks
- **Leads** — Messages received through social media (potential customer inquiries)
- **% Change** — Compares current Woodhouse-managed performance to pre-Woodhouse baseline

---

## Special Notes

- **Elite A/C Solutions** has asterisk note: Pre-partnership metrics include memorial posts for "Big John" which drove unusual engagement spike
- All impressions are **organic only** - paid/boosted posts excluded
- Data through December 15, 2025

---

## Deployment

```bash
cd ~/woodhouse_agency_turnkey_perfomance
ga && git commit -m "message" && gpush
```

Vercel auto-deploys from `main` branch.

---

## Related Repos

| Repo | Purpose |
|------|---------|
| `woodhouse_dealer_dashboard` | Full Allied Air dashboard (110 dealers, 17 distributors) |
| `dealer_reports` | Legacy V1 dashboard (deprecated) |
| `woodhouse_social` | Main SaaS platform |
| `prospect_engine` | National HVAC contractor database |

---

## Git Workflow

```bash
# Push changes
ga && git commit -m "message" && gpush

# Pull changes locally
gp
```

---

## Development Notes

- Static site - no build step required
- Edit HTML/CSS directly
- Test locally by opening index.html in browser
- Vercel protection was blocking external access (now disabled)
