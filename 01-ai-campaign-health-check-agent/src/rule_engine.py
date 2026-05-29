"""
Campaign Optimization Rule Engine

This script reads calculated campaign KPIs and applies practical optimization
rules used by performance marketing teams.

Run from this folder:
    python src/calculate_kpis.py
    python src/rule_engine.py

Input:
    outputs/campaign_kpis.csv

Outputs:
    outputs/campaign_recommendations.csv
    outputs/sample-campaign-health-report.md
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "outputs" / "campaign_kpis.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
RECOMMENDATIONS_FILE = OUTPUT_DIR / "campaign_recommendations.csv"
REPORT_FILE = OUTPUT_DIR / "sample-campaign-health-report.md"

# Beginner-friendly thresholds. In real campaigns, adjust these by industry,
# funnel stage, budget, country, objective, and historical performance.
THRESHOLDS = {
    "high_spend": 2500,
    "low_ctr": 1.0,
    "high_impressions": 15000,
    "high_clicks": 250,
    "low_conversion_rate": 2.0,
    "low_form_completion_rate": 40.0,
    "good_cpl": 300,
    "low_engagement_rate": 45.0,
}


def add_recommendation(recommendations: list, row: pd.Series, issue: str, reason: str, action: str, priority: str) -> None:
    """Append one recommendation row."""
    recommendations.append(
        {
            "date": row["date"],
            "platform": row["platform"],
            "campaign_name": row["campaign_name"],
            "ad_group_or_ad_set": row["ad_group_or_ad_set"],
            "ad_name": row["ad_name"],
            "issue": issue,
            "reason": reason,
            "recommended_action": action,
            "priority": priority,
            "human_approval_required": "Yes",
        }
    )


def apply_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Apply performance marketing rules to campaign KPI data."""
    recommendations = []

    for _, row in df.iterrows():
        if row["spend"] >= THRESHOLDS["high_spend"] and row["leads"] == 0:
            add_recommendation(
                recommendations,
                row,
                "Wasted Spend",
                "Campaign has high spend but no leads.",
                "Check conversion tracking, landing page, targeting, and campaign objective before spending more.",
                "High",
            )

        if row["impressions"] >= THRESHOLDS["high_impressions"] and row["ctr"] < THRESHOLDS["low_ctr"]:
            add_recommendation(
                recommendations,
                row,
                "Creative Issue",
                "Campaign has high impressions but low CTR.",
                "Test new hooks, visuals, headlines, CTAs, and audience-message alignment.",
                "High",
            )

        if row["clicks"] >= THRESHOLDS["high_clicks"] and row["conversion_rate"] < THRESHOLDS["low_conversion_rate"]:
            add_recommendation(
                recommendations,
                row,
                "Landing Page Issue",
                "Campaign is generating clicks but conversion rate is weak.",
                "Review landing page speed, CTA placement, form visibility, trust signals, and offer match.",
                "High",
            )

        if row["form_starts"] > 0 and row["form_completion_rate"] < THRESHOLDS["low_form_completion_rate"]:
            add_recommendation(
                recommendations,
                row,
                "Form Friction",
                "Users are starting the form but not completing it.",
                "Reduce form fields, improve mobile UX, check technical errors, and add trust elements near the form.",
                "Medium",
            )

        if row["leads"] > 0 and row["cpl"] <= THRESHOLDS["good_cpl"] and str(row["lead_quality"]).lower() == "good":
            add_recommendation(
                recommendations,
                row,
                "Scale Candidate",
                "Campaign has efficient CPL and good lead quality.",
                "Increase budget gradually, monitor CPL/lead quality, and test similar audiences or keywords.",
                "Medium",
            )

        if row["leads"] >= 4 and str(row["lead_quality"]).lower() == "poor":
            add_recommendation(
                recommendations,
                row,
                "Lead Quality Issue",
                "Campaign is generating leads but quality is poor.",
                "Improve targeting, add qualifying questions, refine offer, and connect CRM feedback to campaign reports.",
                "High",
            )

        if row["sessions"] > 0 and row["engagement_rate"] < THRESHOLDS["low_engagement_rate"]:
            add_recommendation(
                recommendations,
                row,
                "Traffic Quality Issue",
                "Sessions are coming in but engagement rate is weak.",
                "Review audience, placements, search terms, landing page relevance, and ad-message alignment.",
                "Medium",
            )

    return pd.DataFrame(recommendations)


def create_markdown_report(df: pd.DataFrame, recommendations_df: pd.DataFrame) -> str:
    """Create a portfolio-friendly Markdown report using readable sections instead of one wide table."""
    total_spend = df["spend"].sum()
    total_impressions = df["impressions"].sum()
    total_clicks = df["clicks"].sum()
    total_leads = df["leads"].sum()
    avg_cpl = total_spend / total_leads if total_leads else 0
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions else 0

    report = [
        "# Sample Campaign Health Report",
        "",
        "## Executive Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Total Spend | ₹{total_spend:,.2f} |",
        f"| Total Impressions | {total_impressions:,.0f} |",
        f"| Total Clicks | {total_clicks:,.0f} |",
        f"| Total Leads | {total_leads:,.0f} |",
        f"| Average CTR | {avg_ctr:.2f}% |",
        f"| Average CPL | ₹{avg_cpl:,.2f} |",
        f"| Recommendations Flagged | {len(recommendations_df)} |",
        "",
        "## Visual Outputs",
        "",
        "After running `python src/generate_visuals.py`, the following charts are created in `outputs/visuals/`:",
        "",
        "- `spend_by_platform.png`",
        "- `leads_by_platform.png`",
        "- `recommendations_by_issue.png`",
        "- `cpl_by_campaign.png`",
        "",
        "## Recommendation Summary",
        "",
    ]

    if recommendations_df.empty:
        report.append("No major issues were detected based on the current rule thresholds.")
    else:
        summary = recommendations_df.groupby(["issue", "priority"]).size().reset_index(name="count")
        report.append(summary.to_markdown(index=False))

        high_priority = recommendations_df[recommendations_df["priority"] == "High"]
        report.extend(["", "## High Priority Issues", ""])
        if high_priority.empty:
            report.append("No high-priority issues were detected.")
        else:
            for _, rec in high_priority.head(10).iterrows():
                report.extend(
                    [
                        f"### {rec['campaign_name']}",
                        "",
                        f"- **Platform:** {rec['platform']}",
                        f"- **Issue:** {rec['issue']}",
                        f"- **Reason:** {rec['reason']}",
                        f"- **Recommended Action:** {rec['recommended_action']}",
                        f"- **Human Approval Required:** {rec['human_approval_required']}",
                        "",
                    ]
                )

        report.extend(["", "## Campaign Recommendation Cards", ""])
        for _, rec in recommendations_df.head(15).iterrows():
            report.extend(
                [
                    f"### {rec['platform']} — {rec['campaign_name']}",
                    "",
                    f"**Issue:** {rec['issue']}  ",
                    f"**Priority:** {rec['priority']}  ",
                    f"**Reason:** {rec['reason']}  ",
                    f"**Recommended Action:** {rec['recommended_action']}  ",
                    "",
                    "---",
                    "",
                ]
            )

    report.extend(
        [
            "",
            "## Analyst Notes",
            "",
            "This report is generated using rule-based logic. In a real commercial workflow, these recommendations should be reviewed with additional context such as campaign objective, sales feedback, CRM lead status, attribution window, audience size, and historical benchmarks.",
            "",
            "The recommended actions are not automatic campaign changes. They are decision-support outputs for a marketer, analyst, or manager.",
            "",
            "## Safe Automation Reminder",
            "",
            "The system recommends actions but does not directly change live campaigns. Human approval is required before budget, bidding, targeting, or creative changes are applied.",
        ]
    )

    return "\n".join(report)


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}. Run calculate_kpis.py first."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    kpi_df = pd.read_csv(INPUT_FILE)
    recommendations_df = apply_rules(kpi_df)
    recommendations_df.to_csv(RECOMMENDATIONS_FILE, index=False)

    report = create_markdown_report(kpi_df, recommendations_df)
    REPORT_FILE.write_text(report, encoding="utf-8")

    print("Campaign recommendations generated successfully.")
    print(f"Recommendations: {RECOMMENDATIONS_FILE}")
    print(f"Report: {REPORT_FILE}")

    if recommendations_df.empty:
        print("No major issues detected.")
    else:
        print("\nRecommendation preview:")
        print(recommendations_df[["platform", "campaign_name", "issue", "priority"]].head())


if __name__ == "__main__":
    main()
