"""
Campaign KPI Calculator

This script reads sample campaign performance data and calculates core
performance marketing KPIs used by campaign analysts.

Run from this folder:
    python src/calculate_kpis.py

Input:
    sample-data/campaign_performance_sample.csv

Output:
    outputs/campaign_kpis.csv
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "sample-data" / "campaign_performance_sample.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "campaign_kpis.csv"


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Avoid divide-by-zero errors while calculating marketing KPIs."""
    return numerator.div(denominator.replace({0: pd.NA})).fillna(0)


def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate campaign-level KPIs from raw campaign data."""
    df = df.copy()

    df["ctr"] = safe_divide(df["clicks"], df["impressions"])
    df["cpc"] = safe_divide(df["spend"], df["clicks"])
    df["cpm"] = safe_divide(df["spend"], df["impressions"]) * 1000
    df["cpl"] = safe_divide(df["spend"], df["leads"])
    df["conversion_rate"] = safe_divide(df["leads"], df["clicks"])
    df["engagement_rate"] = safe_divide(df["engaged_sessions"], df["sessions"])
    df["form_completion_rate"] = safe_divide(df["form_submits"], df["form_starts"])

    percentage_columns = [
        "ctr",
        "conversion_rate",
        "engagement_rate",
        "form_completion_rate",
    ]
    currency_columns = ["cpc", "cpm", "cpl"]

    for column in percentage_columns:
        df[column] = (df[column] * 100).round(2)

    for column in currency_columns:
        df[column] = df[column].round(2)

    return df


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_df = pd.read_csv(INPUT_FILE)
    kpi_df = calculate_kpis(raw_df)
    kpi_df.to_csv(OUTPUT_FILE, index=False)

    print("Campaign KPIs calculated successfully.")
    print(f"Input: {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print("\nPreview:")
    print(kpi_df[["platform", "campaign_name", "spend", "clicks", "leads", "ctr", "cpc", "cpl", "conversion_rate"]].head())


if __name__ == "__main__":
    main()
