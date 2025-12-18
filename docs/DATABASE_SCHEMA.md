# Database Schema

## Overview

This project uses SQLite databases to store dealer performance metrics. All data is derived from Sprout Social exports and filtered to include **organic metrics only** (excludes paid/boosted posts).

## Databases

### ihrie_organic.db

Primary database for Ihrie Supply dealer metrics using organic impressions from the Post Performance CSV.

### ihrie_dealers.db

Legacy database (may contain total impressions including paid).

---

## Schema: ihrie_organic.db

### Table: monthly_metrics

Stores monthly aggregated metrics for each dealer.

```sql
CREATE TABLE monthly_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dealer_name TEXT NOT NULL,
    month TEXT NOT NULL,              -- Format: YYYY-MM
    posts INTEGER DEFAULT 0,
    organic_impressions INTEGER DEFAULT 0,
    engagements INTEGER DEFAULT 0,
    organic_video_views INTEGER DEFAULT 0,
    messages INTEGER DEFAULT 0,
    UNIQUE(dealer_name, month)
);

CREATE INDEX idx_monthly_dealer ON monthly_metrics(dealer_name);
CREATE INDEX idx_monthly_month ON monthly_metrics(month);
```

### Table: dealer_summary

Stores aggregated before/after metrics for each dealer.

```sql
CREATE TABLE dealer_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dealer_name TEXT UNIQUE NOT NULL,
    slug TEXT,                        -- URL-friendly name
    distributor TEXT,                 -- Parent distributor
    first_post_date TEXT,             -- When Woodhouse started (YYYY-MM-DD)
    
    -- Totals (all time)
    total_posts INTEGER DEFAULT 0,
    total_impressions INTEGER DEFAULT 0,
    total_engagements INTEGER DEFAULT 0,
    total_video_views INTEGER DEFAULT 0,
    total_messages INTEGER DEFAULT 0,
    
    -- Before Woodhouse (pre-first_post_date)
    before_posts INTEGER DEFAULT 0,
    before_impressions INTEGER DEFAULT 0,
    before_engagements INTEGER DEFAULT 0,
    before_video_views INTEGER DEFAULT 0,
    before_messages INTEGER DEFAULT 0,
    before_months INTEGER DEFAULT 0,  -- Months of activity before Woodhouse
    
    -- After Woodhouse (post-first_post_date)
    after_posts INTEGER DEFAULT 0,
    after_impressions INTEGER DEFAULT 0,
    after_engagements INTEGER DEFAULT 0,
    after_video_views INTEGER DEFAULT 0,
    after_messages INTEGER DEFAULT 0,
    after_months INTEGER DEFAULT 0,   -- Months of activity with Woodhouse
    
    -- Calculated metrics
    pct_change_posts REAL,
    pct_change_impressions REAL,
    pct_change_engagements REAL,
    pct_change_video_views REAL,
    pct_change_messages REAL,
    avg_pct_change REAL               -- Average across all 5 metrics
);

CREATE INDEX idx_summary_distributor ON dealer_summary(distributor);
CREATE INDEX idx_summary_pct ON dealer_summary(avg_pct_change DESC);
```

---

## Data Sources

### Post Performance CSV

Source: `Post_Performance_ALL_DEALERS_*.csv`

**Columns used:**
- `Profile` - Dealer name
- `Date` - Post date
- `Organic Impressions` - Reach excluding paid
- `Engagements` - Total interactions
- `Organic Video Views` - Video views excluding paid

### Profile Performance CSV

Source: `Profile_Performance_ALL_DEALERS_*.csv`

**Columns used:**
- `Profile` - Dealer name
- `Date` - Report date
- `Received Messages (Total)` - Lead count (messages)

---

## % Change Calculation

```
pct_change = ((after - before) / before) * 100

If before = 0:
    pct_change = 100 if after > 0 else 0
```

Average % change is the mean of all 5 metric changes:
```
avg_pct_change = (pct_posts + pct_impressions + pct_engagements + pct_video + pct_messages) / 5
```

---

## Filtering Criteria

For meaningful comparisons, dealers should have:
- **Minimum 6 months** of activity before Woodhouse partnership
- **Minimum 20 posts** before Woodhouse partnership

This ensures sufficient baseline data for accurate before/after comparison.

---

## Ihrie Supply Dealers

| Dealer | Slug | First Post |
|--------|------|------------|
| Airtech - Mechanical Services | airtech | 2023-04-01 |
| Scott Plumbing & Heating Co Inc | scott-plumbing | 2023-05-25 |
| Kennedy's Heating & Air Conditioning | kennedys | 2023-06-01 |
| Metro Maintenance | metro | 2023-08-12 |
| Advanced Air Solutions Systems, Inc. | advanced-air | 2024-02-18 |
| Elite A/C Solutions | elite-ac | 2024-01-15 |
| NC Heating & Air - Your HVAC Friend | nc-heating | 2023-09-01 |

---

## Notes

- Elite A/C has abnormally high pre-Woodhouse engagement due to memorial posts for "Big John"
- All impressions exclude paid/boosted posts
- Data current through December 15, 2025
