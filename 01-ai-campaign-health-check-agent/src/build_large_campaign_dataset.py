"""
Build Large Campaign Health Dataset

This script simulates a realistic marketing analytics workflow:

1. Read raw ad platform exports from Google Ads, Meta Ads, and LinkedIn Ads.
2. Read GA4-style website behavior data.
3. Read CRM lead quality and revenue data.
4. Join the datasets using date + platform + campaign_id + campaign_name.
5. Save one clean processed dataset for KPI calculation and dashboarding.

Run from this folder:
    python src/build_large_campaign_dataset.py

Input:
    sample-data/raw/google_ads_sample_large.csv
    sample-data/raw/meta_ads_sample_large.csv
    sample-data/raw/linkedin_ads_sample_large.csv
    sample-data/raw/ga4_sample_large.csv
    sample-data/raw/crm_leads_sample_large.csv

Output:
    sample-data/processed/campaign_health_large_sample.csv
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "sample-data" / "raw"
PROCESSED_DIR = BASE_DIR / "sample-data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "campaign_health_large_sample.csv"

JOIN_KEYS = ["date", "platform", "campaign_id", "campaign_name"]


def read_ad_platform_data() -> pd.DataFrame:
    """Combine raw ad platform exports into one media delivery table."""
    files = [
        RAW_DIR / "google_ads_sample_large.csv",
        RAW_DIR / "meta_ads_sample_large.csv",
        RAW_DIR / "linkedin_ads_sample_large.csv",
    ]

    frames = []
    for file in files:
        if not file.exists():
            raise FileNotFoundError(f"Missing raw ad platform file: {file}")
        frames.append(pd.read_csv(file))

    media_df = pd.concat(frames, ignore_index=True)
    return media_df


def build_dataset() -> pd.DataFrame:
    """Join ad platform data with GA4 and CRM data."""
    media_df = read_ad_platform_data()
    ga4_df = pd.read_csv(RAW_DIR / "ga4_sample_large.csv")
    crm_df = pd.read_csv(RAW_DIR / "crm_leads_sample_large.csv")

    merged_df = media_df.merge(
        ga4_df,
        on=JOIN_KEYS,
        how="left",
        validate="one_to_one",
    )

    merged_df = merged_df.merge(
        crm_df,
        on=JOIN_KEYS,
        how="left",
        validate="one_to_one",
    )

    numeric_columns = [
        "sessions",
        "engaged_sessions",
        "form_starts",
        "form_submits",
        "leads",
        "qualified_leads",
        "meeting_booked",
        "deals_won",
        "revenue",
    ]
    for column in numeric_columns:
        merged_df[column] = merged_df[column].fillna(0)

    merged_df["landing_page"] = merged_df["landing_page"].fillna("unknown")
    merged_df["lead_quality"] = merged_df["lead_quality"].fillna("Unknown")

    # Keep a clean reporting column order.
    ordered_columns = [
        "date",
        "platform",
        "campaign_id",
        "campaign_name",
        "ad_group_or_ad_set",
        "ad_name",
        "landing_page",
        "spend",
        "impressions",
        "clicks",
        "sessions",
        "engaged_sessions",
        "form_starts",
        "form_submits",
        "leads",
        "qualified_leads",
        "meeting_booked",
        "deals_won",
        "revenue",
        "lead_quality",
    ]

    return merged_df[ordered_columns].sort_values(["date", "platform", "campaign_name"])


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    final_df = build_dataset()
    final_df.to_csv(OUTPUT_FILE, index=False)

    print("Large campaign health dataset built successfully.")
    print(f"Output: {OUTPUT_FILE}")
    print(f"Rows: {len(final_df)}")
    print("\nPreview:")
    print(final_df[["date", "platform", "campaign_name", "spend", "clicks", "leads", "qualified_leads", "revenue", "lead_quality"]].head(10))


if __name__ == "__main__":
    main()
