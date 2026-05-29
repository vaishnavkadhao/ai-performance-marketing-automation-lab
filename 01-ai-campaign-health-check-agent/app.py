"""
Streamlit Dashboard: Campaign Health Check Agent

Run from this folder:
    streamlit run app.py

This dashboard reads generated output files from the Campaign Health Check Agent
and presents campaign KPIs, recommendations, and visual summaries.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
VISUAL_DIR = OUTPUT_DIR / "visuals"
KPI_FILE = OUTPUT_DIR / "campaign_kpis.csv"
RECOMMENDATIONS_FILE = OUTPUT_DIR / "campaign_recommendations.csv"
REPORT_FILE = OUTPUT_DIR / "sample-campaign-health-report.md"

st.set_page_config(
    page_title="Campaign Health Check Agent",
    page_icon="📊",
    layout="wide",
)


def load_data():
    """Load generated KPI and recommendation outputs."""
    if not KPI_FILE.exists() or not RECOMMENDATIONS_FILE.exists():
        st.error("Output files not found. Run calculate_kpis.py and rule_engine.py first.")
        st.stop()

    kpi_df = pd.read_csv(KPI_FILE)
    recommendations_df = pd.read_csv(RECOMMENDATIONS_FILE)
    return kpi_df, recommendations_df


def format_currency(value):
    return f"₹{value:,.0f}"


def main():
    st.title("📊 Campaign Health Check Agent")
    st.caption("Performance marketing KPI analysis, issue detection, and recommendation dashboard")

    kpi_df, recommendations_df = load_data()

    with st.sidebar:
        st.header("Filters")
        selected_platforms = st.multiselect(
            "Platform",
            options=sorted(kpi_df["platform"].unique()),
            default=sorted(kpi_df["platform"].unique()),
        )

        selected_priorities = st.multiselect(
            "Recommendation Priority",
            options=sorted(recommendations_df["priority"].unique()),
            default=sorted(recommendations_df["priority"].unique()),
        )

    filtered_kpi = kpi_df[kpi_df["platform"].isin(selected_platforms)]
    filtered_recommendations = recommendations_df[
        recommendations_df["platform"].isin(selected_platforms)
        & recommendations_df["priority"].isin(selected_priorities)
    ]

    total_spend = filtered_kpi["spend"].sum()
    total_impressions = filtered_kpi["impressions"].sum()
    total_clicks = filtered_kpi["clicks"].sum()
    total_leads = filtered_kpi["leads"].sum()
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions else 0
    avg_cpl = (total_spend / total_leads) if total_leads else 0

    st.subheader("Executive Summary")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Spend", format_currency(total_spend))
    col2.metric("Impressions", f"{total_impressions:,.0f}")
    col3.metric("Clicks", f"{total_clicks:,.0f}")
    col4.metric("Leads", f"{total_leads:,.0f}")
    col5.metric("Avg CPL", format_currency(avg_cpl))

    st.metric("Average CTR", f"{avg_ctr:.2f}%")

    st.divider()

    st.subheader("Visual Summary")
    chart_files = [
        ("Spend by Platform", VISUAL_DIR / "spend_by_platform.png"),
        ("Leads by Platform", VISUAL_DIR / "leads_by_platform.png"),
        ("Recommendations by Issue", VISUAL_DIR / "recommendations_by_issue.png"),
        ("CPL by Campaign", VISUAL_DIR / "cpl_by_campaign.png"),
    ]

    chart_col1, chart_col2 = st.columns(2)
    for index, (title, path) in enumerate(chart_files):
        target_col = chart_col1 if index % 2 == 0 else chart_col2
        with target_col:
            st.markdown(f"**{title}**")
            if path.exists():
                st.image(str(path), use_container_width=True)
            else:
                st.info(f"Chart not found: {path.name}. Run generate_visuals.py first.")

    st.divider()

    st.subheader("Recommendation Summary")
    if filtered_recommendations.empty:
        st.info("No recommendations match the selected filters.")
    else:
        summary = (
            filtered_recommendations.groupby(["issue", "priority"])
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
        )
        st.dataframe(summary, use_container_width=True)

    st.subheader("High Priority Issues")
    high_priority = filtered_recommendations[filtered_recommendations["priority"] == "High"]
    if high_priority.empty:
        st.success("No high-priority issues found for the selected filters.")
    else:
        for _, row in high_priority.head(10).iterrows():
            with st.expander(f"{row['platform']} — {row['campaign_name']} — {row['issue']}"):
                st.write(f"**Ad Group / Ad Set:** {row['ad_group_or_ad_set']}")
                st.write(f"**Ad Name:** {row['ad_name']}")
                st.write(f"**Reason:** {row['reason']}")
                st.write(f"**Recommended Action:** {row['recommended_action']}")
                st.write(f"**Human Approval Required:** {row['human_approval_required']}")

    st.divider()

    st.subheader("Campaign KPI Table")
    display_columns = [
        "platform",
        "campaign_name",
        "spend",
        "impressions",
        "clicks",
        "leads",
        "ctr",
        "cpc",
        "cpl",
        "conversion_rate",
        "engagement_rate",
        "form_completion_rate",
        "lead_quality",
    ]
    st.dataframe(filtered_kpi[display_columns], use_container_width=True)

    st.subheader("Generated Report")
    if REPORT_FILE.exists():
        with st.expander("View Markdown Report"):
            st.markdown(REPORT_FILE.read_text(encoding="utf-8"))
    else:
        st.info("Markdown report not found. Run rule_engine.py first.")


if __name__ == "__main__":
    main()
