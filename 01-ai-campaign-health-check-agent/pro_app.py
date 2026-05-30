from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE = Path(__file__).resolve().parent
OUTPUTS = BASE / "outputs"
KPI_FILE = OUTPUTS / "campaign_kpis.csv"
REC_FILE = OUTPUTS / "campaign_recommendations.csv"
REPORT_FILE = OUTPUTS / "sample-campaign-health-report.md"
PIPELINE_DOC = BASE / "docs" / "multi-source-data-pipeline.md"

st.set_page_config(page_title="AI Campaign Health Intelligence", page_icon="📈", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1320px;}
.hero-card {background: linear-gradient(135deg, #101827 0%, #172036 60%, #0b1220 100%); border: 1px solid #263247; border-radius: 24px; padding: 32px; margin-bottom: 24px; box-shadow: 0 18px 45px rgba(0,0,0,.28);}
.hero-title {font-size: 42px; font-weight: 800; letter-spacing: -0.04em; margin-bottom: 8px;}
.hero-subtitle {font-size: 17px; color: #b8c2d6; max-width: 900px; line-height: 1.65;}
.badge {display: inline-block; padding: 7px 12px; margin: 6px 6px 0 0; border-radius: 999px; background: #1f2a44; border: 1px solid #34415f; color: #dfe7ff; font-size: 13px;}
.card {background: #111827; border: 1px solid #263247; border-radius: 18px; padding: 20px; height: 100%;}
.section-title {font-size: 26px; font-weight: 750; margin: 26px 0 14px 0;}
.small-muted {color: #a9b4c7; font-size: 14px; line-height: 1.55;}
.insight {background: #0f172a; border-left: 4px solid #38bdf8; border-radius: 14px; padding: 16px 18px; margin: 10px 0;}
.warning {background: #201a10; border-left: 4px solid #f59e0b; border-radius: 14px; padding: 16px 18px; margin: 10px 0;}
.success {background: #102018; border-left: 4px solid #22c55e; border-radius: 14px; padding: 16px 18px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    if not KPI_FILE.exists() or not REC_FILE.exists():
        st.error("Generated outputs are missing. Run the pipeline scripts first.")
        st.code("python src/build_large_campaign_dataset.py\npython src/calculate_kpis.py\npython src/rule_engine.py\npython src/generate_visuals.py")
        st.stop()
    return pd.read_csv(KPI_FILE), pd.read_csv(REC_FILE)

def money(x):
    return f"₹{x:,.0f}"

def plot_style(fig):
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20, r=20, t=45, b=25), font=dict(size=13), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig

def render_hero(kpi, rec):
    spend = kpi["spend"].sum(); impressions = kpi["impressions"].sum(); clicks = kpi["clicks"].sum(); leads = kpi["leads"].sum()
    qualified = kpi["qualified_leads"].sum() if "qualified_leads" in kpi.columns else 0
    ctr = clicks / impressions * 100 if impressions else 0; cpl = spend / leads if leads else 0
    health_score = max(0, min(100, int(100 - (len(rec[rec["priority"] == "High"]) / max(len(rec), 1) * 55) - (cpl / 100))))
    st.markdown(f"""
    <div class='hero-card'>
      <div class='hero-title'>📈 AI Campaign Health Intelligence</div>
      <div class='hero-subtitle'>A professional portfolio web app that simulates how performance marketing teams combine ad-platform exports, GA4-style behavior data, and CRM lead-quality data to monitor campaign health and prioritize optimization actions.</div>
      <div style='margin-top:14px'>
        <span class='badge'>Google Ads</span><span class='badge'>Meta Ads</span><span class='badge'>LinkedIn Ads</span><span class='badge'>GA4-style events</span><span class='badge'>CRM lead quality</span><span class='badge'>Python + Streamlit</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Health Score", f"{health_score}/100")
    c2.metric("Spend", money(spend))
    c3.metric("Clicks", f"{clicks:,.0f}")
    c4.metric("Leads", f"{leads:,.0f}")
    c5.metric("Qualified Leads", f"{qualified:,.0f}")
    c6.metric("Avg CPL", money(cpl))
    st.metric("Average CTR", f"{ctr:.2f}%")

def render_filters(kpi, rec):
    with st.sidebar:
        st.header("Control Panel")
        platforms = st.multiselect("Platforms", sorted(kpi["platform"].unique()), default=sorted(kpi["platform"].unique()))
        priorities = st.multiselect("Priorities", sorted(rec["priority"].unique()), default=sorted(rec["priority"].unique()))
        qualities = st.multiselect("Lead Quality", sorted(kpi["lead_quality"].unique()), default=sorted(kpi["lead_quality"].unique()))
        st.divider()
        st.caption("Use filters to simulate how a campaign analyst reviews platform, lead quality, and recommendation priority.")
    return platforms, priorities, qualities

def render_charts(kpi_f, rec_f):
    st.markdown("<div class='section-title'>Executive Visual Analytics</div>", unsafe_allow_html=True)
    left, right = st.columns(2)
    platform_spend = kpi_f.groupby("platform", as_index=False)["spend"].sum()
    platform_leads = kpi_f.groupby("platform", as_index=False)["leads"].sum()
    fig_spend = px.pie(platform_spend, names="platform", values="spend", hole=.55, title="Spend Share by Platform")
    fig_leads = px.pie(platform_leads, names="platform", values="leads", hole=.55, title="Lead Share by Platform")
    left.plotly_chart(plot_style(fig_spend), use_container_width=True)
    right.plotly_chart(plot_style(fig_leads), use_container_width=True)

    funnel_values = [kpi_f["impressions"].sum(), kpi_f["clicks"].sum(), kpi_f["leads"].sum(), kpi_f["qualified_leads"].sum() if "qualified_leads" in kpi_f.columns else 0]
    fig_funnel = go.Figure(go.Funnel(y=["Impressions", "Clicks", "Leads", "Qualified Leads"], x=funnel_values, textinfo="value+percent previous"))
    fig_funnel.update_layout(title="Full Funnel: Impression to Qualified Lead")
    st.plotly_chart(plot_style(fig_funnel), use_container_width=True)

    c1, c2 = st.columns(2)
    daily = kpi_f.groupby("date", as_index=False).agg({"spend":"sum", "leads":"sum"}) if "date" in kpi_f.columns else pd.DataFrame()
    if not daily.empty:
        fig_trend = px.line(daily, x="date", y=["spend", "leads"], markers=True, title="Daily Spend and Lead Trend")
        c1.plotly_chart(plot_style(fig_trend), use_container_width=True)
    issue_summary = rec_f.groupby(["issue", "priority"], as_index=False).size()
    fig_issue = px.bar(issue_summary, x="size", y="issue", color="priority", orientation="h", title="Issues by Type and Priority")
    c2.plotly_chart(plot_style(fig_issue), use_container_width=True)

    ranked = kpi_f.groupby(["platform", "campaign_name"], as_index=False).agg({"leads":"sum", "spend":"sum"})
    ranked["cpl"] = ranked["spend"] / ranked["leads"].replace(0, pd.NA)
    ranked = ranked.fillna(0).sort_values("leads", ascending=False).head(10)
    fig_rank = px.bar(ranked, x="leads", y="campaign_name", color="platform", orientation="h", title="Top Campaigns by Lead Volume")
    st.plotly_chart(plot_style(fig_rank), use_container_width=True)

def render_insights(kpi_f, rec_f):
    st.markdown("<div class='section-title'>Optimization Command Center</div>", unsafe_allow_html=True)
    high = rec_f[rec_f["priority"] == "High"]
    medium = rec_f[rec_f["priority"] == "Medium"]
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='warning'><b>High Priority Issues</b><br><span style='font-size:32px'>{len(high)}</span><br><span class='small-muted'>Needs marketer review before scaling.</span></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='insight'><b>Medium Priority Issues</b><br><span style='font-size:32px'>{len(medium)}</span><br><span class='small-muted'>Monitor and test improvements.</span></div>", unsafe_allow_html=True)
    scale = rec_f[rec_f["issue"].str.contains("Scale", case=False, na=False)]
    c3.markdown(f"<div class='success'><b>Scale Candidates</b><br><span style='font-size:32px'>{len(scale)}</span><br><span class='small-muted'>Potential campaigns to increase budget gradually.</span></div>", unsafe_allow_html=True)
    st.subheader("Priority Recommendation Cards")
    for _, row in high.head(8).iterrows():
        st.markdown(f"""
        <div class='card'>
          <b>{row['platform']} · {row['campaign_name']}</b><br>
          <span class='badge'>{row['issue']}</span><span class='badge'>{row['priority']}</span><br><br>
          <b>Reason:</b> {row['reason']}<br>
          <b>Recommended action:</b> {row['recommended_action']}<br>
          <b>Human approval:</b> {row['human_approval_required']}
        </div><br>
        """, unsafe_allow_html=True)

def render_pipeline(kpi):
    st.markdown("<div class='section-title'>Data Pipeline Story</div>", unsafe_allow_html=True)
    st.code("Ad exports + GA4-style behavior + CRM quality -> clean processed dataset -> KPI engine -> recommendation engine -> dashboard", language="text")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown("<div class='card'><b>1. Ad Platforms</b><br><span class='small-muted'>Spend, impressions, clicks, campaign/ad data.</span></div>", unsafe_allow_html=True)
    c2.markdown("<div class='card'><b>2. GA4 Events</b><br><span class='small-muted'>Sessions, engaged sessions, form starts, submits.</span></div>", unsafe_allow_html=True)
    c3.markdown("<div class='card'><b>3. CRM Feedback</b><br><span class='small-muted'>Qualified leads, meetings, deals, revenue, quality.</span></div>", unsafe_allow_html=True)
    c4.markdown("<div class='card'><b>4. Dashboard</b><br><span class='small-muted'>KPIs, risks, recommendations, next actions.</span></div>", unsafe_allow_html=True)
    if PIPELINE_DOC.exists():
        with st.expander("Read technical pipeline documentation"):
            st.markdown(PIPELINE_DOC.read_text(encoding="utf-8"))
    st.subheader("Available Dataset Fields")
    st.dataframe(pd.DataFrame({"columns": kpi.columns}), use_container_width=True)

def render_report():
    st.markdown("<div class='section-title'>Generated Report</div>", unsafe_allow_html=True)
    if REPORT_FILE.exists():
        st.markdown(REPORT_FILE.read_text(encoding="utf-8"))
    else:
        st.info("Report not found. Run rule_engine.py first.")

def render_resume():
    st.markdown("<div class='section-title'>Resume / Interview View</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><b>Project positioning:</b> Multi-source performance marketing analytics and campaign optimization dashboard.<br><br><b>Tools:</b> Python, Pandas, Plotly, Streamlit, Matplotlib, CSV data pipeline, rule-based recommendations.<br><br><b>Data simulated:</b> Google Ads, Meta Ads, LinkedIn Ads, GA4-style events, CRM lead quality and revenue.</div>", unsafe_allow_html=True)
    st.subheader("Resume Bullet")
    st.code("Built a Python and Streamlit-based campaign health intelligence web app combining simulated Google Ads, Meta Ads, LinkedIn Ads, GA4-style behavior data, and CRM lead-quality data to calculate KPIs, visualize funnel performance, and generate human-approved optimization recommendations.")

def main():
    kpi, rec = load_data()
    render_hero(kpi, rec)
    platforms, priorities, qualities = render_filters(kpi, rec)
    kpi_f = kpi[kpi["platform"].isin(platforms) & kpi["lead_quality"].isin(qualities)]
    rec_f = rec[rec["platform"].isin(platforms) & rec["priority"].isin(priorities)]
    t1, t2, t3, t4 = st.tabs(["📊 Dashboard", "🔄 Data Pipeline", "📄 Report", "💼 Resume View"])
    with t1:
        render_charts(kpi_f, rec_f)
        render_insights(kpi_f, rec_f)
        st.subheader("Campaign KPI Data")
        st.dataframe(kpi_f, use_container_width=True)
    with t2:
        render_pipeline(kpi)
    with t3:
        render_report()
    with t4:
        render_resume()

if __name__ == "__main__":
    main()
