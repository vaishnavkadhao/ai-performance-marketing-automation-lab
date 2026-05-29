"""
Campaign KPI Calculator

This script reads campaign performance data and calculates core performance
marketing KPIs used by campaign analysts.

Run from this folder:
    python src/calculate_kpis.py

Input priority:
    1. sample-data/processed/campaign_health_large_sample.csv
    2. sample-data/campaign_performance_sample.csv

Output:
    outputs/campaign_kpis.csv
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_INPUT_FILE = BASE_DIR / "sample-data" / "processed" / "campaign_health_large_sample.csv"
FALLBACK_INPUT_FILE = BASE_DIR / "sample-data" / "campaign_performance_sample.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "campaign_kpis.csv"


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Avoid divide-by-zero errors while calculating marketing KPIs."""
    return numerator.div(denominator.replace({0: pd.NA})).fillna(0)


def get_input_file() -> Path:
    """Use the large processed dataset when available; otherwise use the small demo dataset."""
    if PROCESSED_INPUT_FILE.exists():
        return PROCESSED_INPUT_FILE
    return FALLBACK_INPUT_FILE


def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate campaign-level KPIs from campaign data."""
    df = df.copy()

    df["ctr"] = safe_divide(df["clicks"], df["impressions"])
    df["cpc"] = safe_divide(df["spend"], df["clicks"])
    df["cpm"] = safe_divide(df["spend"], df["impressions"]) * 1000
    df["cpl"] = safe_divide(df["spend"], df["leads"])
    df["conversion_rate"] = safe_divide(df["leads"], df["clicks"])
    df["engagement_rate"] = safe_divide(df["engaged_sessions"], df["sessions"])
    df["form_completion_rate"] = safe_divide(df["form_submits"], df["form_starts"])

    if "qualified_leads" in df.columns:
        df["cost_per_qualified_lead"] = safe_divide(df["spend"], df["qualified_leads"])
        df["lead_to_qualified_rate"] = safe_divide(df["qualified_leads"], df["leads"])
    else:
        df["qualified_leads"] = 0
        df["cost_per_qualified_lead"] = 0
        df["lead_to_qualified_rate"] = 0

    if "revenue" in df.columns:
        df["roas"] = safe_divide(df["revenue"], df["spend"])
    else:
        df["revenue"] = 0
        df["roas"] = 0

    percentage_columns = [
        "ctr",
        "conversion_rate",
        "engagement_rate",
        "form_completion_rate",
        "lead_to_qualified_rate",
    ]
    currency_columns = ["cpc", "cpm", "cpl", "cost_per_qualified_lead"]

    for column in percentage_columns:
        df[column] = (df[column] * 100).round(2)

    for column in currency_columns:
        df[column] = df[column].round(2)

    df["roas"] = df["roas"].round(2)

    return df


def main() -> None:
    input_file = get_input_file()
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_df = pd.read_csv(input_file)
    kpi_df = calculate_kpis(raw_df)
    kpi_df.to_csv(OUTPUT_FILE, index=False)

    print("Campaign KPIs calculated successfully.")
    print(f"Input: {input_file}")
    print(f"Output: {OUTPUT_FILE}")
    print("\nPreview:")
    preview_columns = [
        "platform",
        "campaign_name",
        "spend",
        "clicks",
        "leads",
        "qualified_leads",
        "ctr",
        "cpl",
        "cost_per_qualified_lead",
        "roas",
    ]
    print(kpi_df[preview_columns].head())


if __name__ == "__main__":
    main()
