"""
Campaign Visual Generator

This script creates simple GitHub-friendly charts from calculated campaign KPI data.

Run from this folder:
    python src/calculate_kpis.py
    python src/rule_engine.py
    python src/generate_visuals.py

Input:
    outputs/campaign_kpis.csv
    outputs/campaign_recommendations.csv

Outputs:
    outputs/visuals/spend_by_platform.png
    outputs/visuals/leads_by_platform.png
    outputs/visuals/recommendations_by_issue.png
    outputs/visuals/cpl_by_campaign.png
"""

from pathlib import Path
import textwrap
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
VISUAL_DIR = OUTPUT_DIR / "visuals"
KPI_FILE = OUTPUT_DIR / "campaign_kpis.csv"
RECOMMENDATIONS_FILE = OUTPUT_DIR / "campaign_recommendations.csv"


def wrap_labels(labels, width=24):
    """Wrap long chart labels so they fit better."""
    return ["\n".join(textwrap.wrap(str(label), width=width)) for label in labels]


def save_bar_chart(data, x_col, y_col, title, ylabel, filename, rotate=False):
    """Create and save a basic bar chart."""
    fig, ax = plt.subplots(figsize=(10, 6))
    x_labels = wrap_labels(data[x_col].tolist())
    ax.bar(x_labels, data[y_col])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    if rotate:
        ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(VISUAL_DIR / filename, dpi=160)
    plt.close(fig)


def main() -> None:
    if not KPI_FILE.exists():
        raise FileNotFoundError(f"KPI file not found: {KPI_FILE}. Run calculate_kpis.py first.")

    VISUAL_DIR.mkdir(parents=True, exist_ok=True)
    kpi_df = pd.read_csv(KPI_FILE)

    spend_by_platform = kpi_df.groupby("platform", as_index=False)["spend"].sum().sort_values("spend", ascending=False)
    save_bar_chart(
        spend_by_platform,
        "platform",
        "spend",
        "Spend by Platform",
        "Spend",
        "spend_by_platform.png",
    )

    leads_by_platform = kpi_df.groupby("platform", as_index=False)["leads"].sum().sort_values("leads", ascending=False)
    save_bar_chart(
        leads_by_platform,
        "platform",
        "leads",
        "Leads by Platform",
        "Leads",
        "leads_by_platform.png",
    )

    cpl_by_campaign = (
        kpi_df.groupby("campaign_name", as_index=False)
        .agg({"spend": "sum", "leads": "sum"})
    )
    cpl_by_campaign = cpl_by_campaign[cpl_by_campaign["leads"] > 0]
    cpl_by_campaign["cpl"] = cpl_by_campaign["spend"] / cpl_by_campaign["leads"]
    cpl_by_campaign = cpl_by_campaign.sort_values("cpl", ascending=False)
    save_bar_chart(
        cpl_by_campaign,
        "campaign_name",
        "cpl",
        "Cost Per Lead by Campaign",
        "CPL",
        "cpl_by_campaign.png",
        rotate=True,
    )

    if RECOMMENDATIONS_FILE.exists():
        recommendations_df = pd.read_csv(RECOMMENDATIONS_FILE)
        if not recommendations_df.empty:
            rec_by_issue = (
                recommendations_df.groupby("issue", as_index=False)
                .size()
                .rename(columns={"size": "count"})
                .sort_values("count", ascending=False)
            )
            save_bar_chart(
                rec_by_issue,
                "issue",
                "count",
                "Recommendations by Issue Type",
                "Count",
                "recommendations_by_issue.png",
                rotate=True,
            )

    print("Visuals generated successfully.")
    print(f"Output folder: {VISUAL_DIR}")


if __name__ == "__main__":
    main()
