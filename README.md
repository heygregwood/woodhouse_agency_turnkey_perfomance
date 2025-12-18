# Woodhouse Agency Turnkey Reports

Ihrie Supply dealer performance dashboard - organic social media metrics for HVAC dealers managed by Woodhouse Turnkey Social Media.

**Live:** https://woodhouseagencyturnkeyreports.vercel.app

## Overview

This dashboard shows performance metrics for 7 Ihrie Supply dealers:
- Airtech - Mechanical Services
- Scott Plumbing & Heating Co Inc
- Kennedy's Heating & Air Conditioning
- Metro Maintenance
- Advanced Air Solutions Systems, Inc.
- Elite A/C Solutions
- NC Heating & Air - Your HVAC Friend

## Metrics Tracked

- **Posts** — Content published to social media
- **Impressions** — Organic reach (excludes paid/boosted)
- **Engagements** — Likes, comments, shares, clicks
- **Leads** — Messages received
- **% Change** — Before vs after Woodhouse partnership

## Tech Stack

- Static HTML + Tailwind CSS
- Vanilla JavaScript
- SQLite databases
- Deployed on Vercel

## Development

```bash
# Clone
git clone https://github.com/heygregwood/woodhouse_agency_turnkey_perfomance.git

# Edit files directly - no build step needed
# Test by opening index.html in browser

# Deploy
git add . && git commit -m "message" && git push
```

## Data Sources

Data exported from Sprout Social:
- Post Performance CSV (individual post metrics)
- Profile Performance CSV (aggregate metrics)

All impressions are **organic only** - paid/boosted posts excluded from analysis.
