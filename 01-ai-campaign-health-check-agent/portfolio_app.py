from pathlib import Path
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent
OUTPUTS = BASE / "outputs"
VISUALS = OUTPUTS / "visuals"
KPI_FILE = OUTPUTS / "campaign_kpis.csv"
REC_FILE = OUTPUTS / "campaign_recommendations.csv"
REPORT_FILE = OUTPUTS / "sample-campaign-health-report.md"
PIPELINE_DOC = BASE / "docs" / "multi-source-data-pipeline.md"

st.set_page_config(page_title="Campaign Health Check Agent", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv(KPI_FILE), pd.read_csv(REC_FILE)

def money(x):
    return f"₹{x:,.0f}"

def main():
    kpi, rec = load_data()
    spend = kpi["spend"].sum()
    impressions = kpi["impressions"].sum()
    clicks = kpi["clicks"].sum()
    leads = kpi["leads"].sum()
    ctr = clicks / impressions * 100 if impressions else 0
    cpl = spend / leads if leads else 0

    st.title("📊 Campaign Health Check Agent")
    st.write("A portfolio web app for multi-source performance marketing analysis, KPI monitoring, and campaign health recommendations.")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Spend", money(spend))
    c2.metric("Impressions", f"{impressions:,.0f}")
    c3.metric("Clicks", f"{clicks:,.0f}")
    c4.metric("Leads", f"{leads:,.0f}")
    c5.metric("Avg CPL", money(cpl))
    st.metric("Average CTR", f"{ctr:.2f}%")

    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Data Pipeline", "Report", "Resume View"])

    with tab1:
        platform = st.multiselect("Platform", sorted(kpi["platform"].unique()), default=sorted(kpi["platform"].unique()))
        priority = st.multiselect("Priority", sorted(rec["priority"].unique()), default=sorted(rec["priority"].unique()))
        kpi_f = kpi[kpi["platform"].isin(platform)]
        rec_f = rec[rec["platform"].isin(platform) & rec["priority"].isin(priority)]

        st.subheader("Visual Summary")
        charts = ["spend_by_platform.png", "leads_by_platform.png", "recommendations_by_issue.png", "cpl_by_campaign.png"]
        col_a, col_b = st.columns(2)
        for i, chart in enumerate(charts):
            with (col_a if i % 2 == 0 else col_b):
                path = VISUALS / chart
                if path.exists():
                    st.image(str(path), width="stretch")

        st.subheader("Recommendation Summary")
        st.dataframe(rec_f.groupby(["issue", "priority"]).size().reset_index(name="count"), width="stretch")
        st.subheader("Campaign KPI Table")
        st.dataframe(kpi_f, width="stretch")

    with tab2:
        st.subheader("Multi-Source Data Pipeline")
        st.code("Ad platform exports + GA4-style behavior + CRM quality data -> processed dataset -> KPI engine -> recommendations -> dashboard", language="text")
        if PIPELINE_DOC.exists():
            st.markdown(PIPELINE_DOC.read_text(encoding="utf-8"))

    with tab3:
        st.subheader("Generated Report")
        if REPORT_FILE.exists():
            st.markdown(REPORT_FILE.read_text(encoding="utf-8"))

    with tab4:
        st.subheader("Resume / Interview View")
        st.info("Built a Python and Streamlit-based campaign health dashboard combining simulated Google Ads, Meta Ads, LinkedIn Ads, GA4-style behavior data, and CRM lead-quality data to calculate KPIs and generate campaign recommendations.")

if __name__ == "__main__":
    main()
