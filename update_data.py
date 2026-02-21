#!/usr/bin/env python3
"""
Update Ihrie Supply dealer performance dashboard from Sprout Social CSV exports.

Usage:
    python3 update_data.py \\
        --post-csv "/path/to/Post Performance.csv" \\
        --profile-csv "/path/to/Profile Performance.csv"

Optional:
    --data-through "February 20, 2026"   Override the display date (auto-detected otherwise)
    --dry-run                            Preview changes without writing files

What it does:
    1. Reads Post Performance CSV for organic impressions, engagements, video views per dealer per month
    2. Reads Profile Performance CSV for messages (leads) and audience (followers) per dealer
    3. Updates dealer JSON files in dealers/ (adds new monthly data, updates after-period totals)
    4. Updates index.html (patches the hardcoded dealer array and "Data through" date)
    5. Creates .bak backups of every file before modifying
"""

import argparse
import csv
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
DEALERS_DIR = os.path.join(REPO_ROOT, "dealers")
INDEX_HTML = os.path.join(REPO_ROOT, "index.html")

# Sprout Social profile name -> JSON file slug
PROFILE_MAP = {
    "Airtech - Mechanical Services": "airtech",
    "Scott Plumbing & Heating Co Inc": "scott-plumbing",
    "Kennedy's Heating & Air Conditioning": "kennedys",
    "Metro Maintenance": "metro",
    "Advanced Air Solutions Systems, Inc.": "advanced-air",
    "NC Heating & Air - Your HVAC Friend": "nc-heating",
    "Elite A/C Solutions": "elite-ac",
}

# Order dealers appear in index.html
DEALER_ORDER = [
    "airtech", "scott-plumbing", "kennedys", "metro",
    "advanced-air", "nc-heating", "elite-ac",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_number(val):
    """Convert CSV value like '2,132' or '' to int."""
    if not val or not val.strip():
        return 0
    return int(val.strip().replace(",", ""))


def find_column(headers, *keywords):
    """Find a column name by searching for keywords (case-insensitive).
    Returns the matching header string, or raises ValueError."""
    for header in headers:
        h_lower = header.lower()
        if all(kw.lower() in h_lower for kw in keywords):
            return header
    raise ValueError(
        f"Could not find column matching keywords: {keywords}\n"
        f"Available columns: {headers}"
    )


def parse_post_date(date_str):
    """Parse date from Post Performance CSV, e.g. '2/17/2026 10:49 am'."""
    date_str = date_str.strip()
    for fmt in ["%m/%d/%Y %I:%M %p", "%m/%d/%Y %I:%M%p", "%m/%d/%Y"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse post date: '{date_str}'")


def parse_profile_date(date_str):
    """Parse date from Profile Performance CSV, e.g. '12-16-2025'."""
    return datetime.strptime(date_str.strip(), "%m-%d-%Y")


def format_display_date(dt):
    """Format a datetime as 'February 20, 2026'."""
    return dt.strftime("%B %d, %Y").replace(" 0", " ")

# ---------------------------------------------------------------------------
# CSV Parsing
# ---------------------------------------------------------------------------

def parse_post_csv(path):
    """Parse the Post Performance CSV.

    Returns:
        post_data: {slug: {month_str: {posts, impressions, engagements, video_views}}}
        latest_date: datetime of the most recent post
    """
    post_data = defaultdict(lambda: defaultdict(lambda: {
        "posts": 0, "impressions": 0, "engagements": 0, "video_views": 0
    }))
    latest_date = datetime(2000, 1, 1)
    skipped_profiles = set()

    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        col_profile = find_column(headers, "Profile")
        col_date = find_column(headers, "Date")
        col_impressions = find_column(headers, "Organic", "Impressions")
        col_engagements = find_column(headers, "Engagements")
        col_video = find_column(headers, "Organic", "Video", "Views")

        for row in reader:
            profile = row[col_profile].strip()
            slug = PROFILE_MAP.get(profile)
            if not slug:
                skipped_profiles.add(profile)
                continue

            dt = parse_post_date(row[col_date])
            month_str = dt.strftime("%Y-%m")
            latest_date = max(latest_date, dt)

            bucket = post_data[slug][month_str]
            bucket["posts"] += 1
            bucket["impressions"] += parse_number(row[col_impressions])
            bucket["engagements"] += parse_number(row[col_engagements])
            bucket["video_views"] += parse_number(row[col_video])

    if skipped_profiles:
        print(f"  Skipped profiles not in dealer map: {', '.join(sorted(skipped_profiles))}")

    return dict(post_data), latest_date


def parse_profile_csv(path):
    """Parse the Profile Performance CSV.

    Returns:
        profile_data: {slug: {messages_by_month: {month: count}, messages_total: int, audience_end: int}}
        latest_date: datetime of the most recent row
    """
    # Collect daily data first, then aggregate
    daily = defaultdict(lambda: defaultdict(lambda: {"messages": 0, "audience": 0}))
    latest_date = datetime(2000, 1, 1)
    skipped_profiles = set()

    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        col_profile = find_column(headers, "Profile")
        col_date = find_column(headers, "Date")
        col_messages = find_column(headers, "Received", "Messages")
        col_audience = find_column(headers, "Audience")

        for row in reader:
            profile = row[col_profile].strip()
            slug = PROFILE_MAP.get(profile)
            if not slug:
                skipped_profiles.add(profile)
                continue

            dt = parse_profile_date(row[col_date])
            date_str = dt.strftime("%Y-%m-%d")
            latest_date = max(latest_date, dt)

            day = daily[slug][date_str]
            day["messages"] += parse_number(row[col_messages])
            # Take max audience across networks for a given day
            aud = parse_number(row[col_audience])
            if aud > day["audience"]:
                day["audience"] = aud

    if skipped_profiles:
        print(f"  Skipped profiles not in dealer map: {', '.join(sorted(skipped_profiles))}")

    # Aggregate into final structure
    profile_data = {}
    for slug, days in daily.items():
        messages_by_month = defaultdict(int)
        messages_total = 0
        latest_day = None
        audience_end = 0

        for date_str in sorted(days.keys()):
            month_str = date_str[:7]
            msg = days[date_str]["messages"]
            messages_by_month[month_str] += msg
            messages_total += msg
            latest_day = date_str
            # Use latest non-zero audience (last day may be empty in Sprout Social)
            if days[date_str]["audience"] > 0:
                audience_end = days[date_str]["audience"]

        profile_data[slug] = {
            "messages_by_month": dict(messages_by_month),
            "messages_total": messages_total,
            "audience_end": audience_end,
        }

    return profile_data, latest_date

# ---------------------------------------------------------------------------
# Merge Logic
# ---------------------------------------------------------------------------

def merge_dealer_data(dealer, post_months, profile_info):
    """Merge new CSV data into an existing dealer dict (modifies in place).

    Args:
        dealer: the loaded JSON dict for this dealer
        post_months: {month_str: {posts, impressions, engagements, video_views}} from Post CSV
        profile_info: {messages_by_month, messages_total, audience_end} from Profile CSV

    Returns:
        changes dict for summary output
    """
    old_after = dict(dealer["after"])
    old_audience = dealer.get("audience_end", 0)

    # Find the last month already in the JSON
    existing_months = {m["month"] for m in dealer["monthly"]}
    last_existing = max(existing_months) if existing_months else "0000-00"

    months_updated = []
    months_added = []
    months_skipped = []

    for month_str in sorted(post_months.keys()):
        new = post_months[month_str]

        if month_str < last_existing:
            # This month is already fully accounted for -- skip
            months_skipped.append(month_str)
            continue
        elif month_str == last_existing:
            # Partial month (e.g., Dec 2025 had data through Dec 15, new CSV adds Dec 16+)
            for entry in dealer["monthly"]:
                if entry["month"] == month_str:
                    entry["posts"] += new["posts"]
                    entry["impressions"] += new["impressions"]
                    entry["engagements"] += new["engagements"]
                    months_updated.append(month_str)
                    break
        else:
            # Brand new month
            dealer["monthly"].append({
                "month": month_str,
                "posts": new["posts"],
                "impressions": new["impressions"],
                "engagements": new["engagements"],
            })
            months_added.append(month_str)

        # Add to "after" totals
        dealer["after"]["posts"] += new["posts"]
        dealer["after"]["impressions"] += new["impressions"]
        dealer["after"]["engagements"] += new["engagements"]
        dealer["after"]["video_views"] += new.get("video_views", 0)

    # Sort monthly array by month
    dealer["monthly"].sort(key=lambda m: m["month"])

    # Messages from Profile CSV
    new_messages = 0
    if profile_info and "messages_by_month" in profile_info:
        for month_str, msg_count in profile_info["messages_by_month"].items():
            if month_str >= last_existing:
                new_messages += msg_count
        dealer["after"]["messages"] += new_messages

    # Audience from Profile CSV
    if profile_info and profile_info.get("audience_end", 0) > 0:
        dealer["audience_end"] = profile_info["audience_end"]

    return {
        "old_after": old_after,
        "new_after": dict(dealer["after"]),
        "old_audience": old_audience,
        "new_audience": dealer.get("audience_end", 0),
        "months_updated": months_updated,
        "months_added": months_added,
        "months_skipped": months_skipped,
        "new_messages": new_messages,
    }

# ---------------------------------------------------------------------------
# File Writing
# ---------------------------------------------------------------------------

def backup_and_write_json(json_path, data):
    """Create a .bak backup and write updated JSON."""
    bak_path = json_path + ".bak"
    shutil.copy2(json_path, bak_path)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def update_index_html(data_through):
    """Patch index.html with updated dealer data and data-through date."""
    # Load ALL dealer JSONs (including unchanged ones like Elite)
    all_dealers = []
    for slug in DEALER_ORDER:
        json_path = os.path.join(DEALERS_DIR, f"{slug}.json")
        if not os.path.exists(json_path):
            continue
        with open(json_path, "r", encoding="utf-8") as f:
            all_dealers.append(json.load(f))

    # Build the JS array entries
    js_entries = []
    for d in all_dealers:
        entry = (
            f'      {{ "profile": {json.dumps(d["profile"])}, '
            f'"slug": "{d["slug"]}", '
            f'"first_post": "{d["first_post"]}",\n'
            f'        "before": {{"posts": {d["before"]["posts"]}, '
            f'"impressions": {d["before"]["impressions"]}, '
            f'"engagements": {d["before"]["engagements"]}, '
            f'"messages": {d["before"]["messages"]}}},\n'
            f'        "after": {{"posts": {d["after"]["posts"]}, '
            f'"impressions": {d["after"]["impressions"]}, '
            f'"engagements": {d["after"]["engagements"]}, '
            f'"messages": {d["after"]["messages"]}}} }}'
        )
        js_entries.append(entry)

    js_array = "const dealers = [\n" + ",\n".join(js_entries) + "\n    ];"

    # Read, patch, write
    bak_path = INDEX_HTML + ".bak"
    shutil.copy2(INDEX_HTML, bak_path)

    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # Replace the dealers array
    html = re.sub(
        r"const dealers = \[.*?\];",
        js_array,
        html,
        flags=re.DOTALL,
    )

    # Replace the "Data through" text
    html = re.sub(
        r"Data through [^<]+",
        f"Data through {data_through}",
        html,
    )

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def print_summary(results, unchanged_slugs, data_through, dry_run):
    """Print a human-readable summary of all changes."""
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"\n{'=' * 60}")
    print(f"{prefix}Ihrie Supply Dashboard Update")
    print(f"{'=' * 60}")
    print(f"Data through: {data_through}\n")

    for slug, changes in results.items():
        profile = changes.get("profile", slug)
        print(f"--- {profile} ---")

        if changes["months_updated"]:
            for m in changes["months_updated"]:
                print(f"  Updated: {m} (added new data to existing month)")
        if changes["months_added"]:
            for m in changes["months_added"]:
                print(f"  Added:   {m} (new month)")
        if changes["months_skipped"]:
            for m in changes["months_skipped"]:
                print(f"  Skipped: {m} (already counted)")

        old = changes["old_after"]
        new = changes["new_after"]
        print(f"  Posts:       {old['posts']:,} -> {new['posts']:,} (+{new['posts'] - old['posts']:,})")
        print(f"  Impressions: {old['impressions']:,} -> {new['impressions']:,} (+{new['impressions'] - old['impressions']:,})")
        print(f"  Engagements: {old['engagements']:,} -> {new['engagements']:,} (+{new['engagements'] - old['engagements']:,})")
        print(f"  Video Views: {old['video_views']:,} -> {new['video_views']:,} (+{new['video_views'] - old['video_views']:,})")
        print(f"  Messages:    {old['messages']:,} -> {new['messages']:,} (+{changes['new_messages']})")
        print(f"  Audience:    {changes['old_audience']:,} -> {changes['new_audience']:,}")
        print()

    if unchanged_slugs:
        for slug in unchanged_slugs:
            json_path = os.path.join(DEALERS_DIR, f"{slug}.json")
            if os.path.exists(json_path):
                with open(json_path) as f:
                    d = json.load(f)
                print(f"--- {d['profile']} ---")
            else:
                print(f"--- {slug} ---")
            print(f"  (not in CSV exports -- unchanged)")
            print()

    if not dry_run:
        print(f"Files updated (backups created with .bak extension)")
        print(f"\nReady to deploy:")
        print(f'  git add -A && git commit -m "Update data through {data_through}" && git push')
    else:
        print("No files were modified (dry run).")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Update Ihrie Supply dashboard from Sprout Social CSV exports."
    )
    parser.add_argument(
        "--post-csv", required=True,
        help="Path to Post Performance CSV from Sprout Social"
    )
    parser.add_argument(
        "--profile-csv", required=True,
        help="Path to Profile Performance CSV from Sprout Social"
    )
    parser.add_argument(
        "--data-through", default=None,
        help='Display date, e.g. "February 20, 2026" (auto-detected if omitted)'
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without writing files"
    )
    args = parser.parse_args()

    # Validate files exist
    for path, label in [(args.post_csv, "Post CSV"), (args.profile_csv, "Profile CSV")]:
        if not os.path.exists(path):
            print(f"ERROR: {label} not found: {path}")
            sys.exit(1)

    # Parse CSVs
    print("Reading Post Performance CSV...")
    post_data, latest_post_date = parse_post_csv(args.post_csv)
    print(f"  Found {sum(sum(m['posts'] for m in months.values()) for months in post_data.values())} posts across {len(post_data)} dealers")

    print("Reading Profile Performance CSV...")
    profile_data, latest_profile_date = parse_profile_csv(args.profile_csv)
    print(f"  Found data for {len(profile_data)} dealers")

    # Determine data-through date
    if args.data_through:
        data_through = args.data_through
    else:
        latest = max(latest_post_date, latest_profile_date)
        data_through = format_display_date(latest)
    print(f"  Data through: {data_through}")

    # Merge data into each dealer
    results = {}
    all_slugs_with_data = set(list(post_data.keys()) + list(profile_data.keys()))

    for slug in sorted(all_slugs_with_data):
        json_path = os.path.join(DEALERS_DIR, f"{slug}.json")
        if not os.path.exists(json_path):
            print(f"  WARNING: No JSON file for '{slug}', skipping")
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            dealer = json.load(f)

        changes = merge_dealer_data(
            dealer,
            post_data.get(slug, {}),
            profile_data.get(slug, {}),
        )
        changes["profile"] = dealer["profile"]

        if not args.dry_run:
            backup_and_write_json(json_path, dealer)

        results[slug] = changes

    # Update index.html
    if not args.dry_run:
        update_index_html(data_through)

    # Report on dealers not in the CSV
    unchanged_slugs = [s for s in DEALER_ORDER if s not in all_slugs_with_data]

    # Print summary
    print_summary(results, unchanged_slugs, data_through, args.dry_run)


if __name__ == "__main__":
    main()
