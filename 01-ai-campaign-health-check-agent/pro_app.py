from pathlib import Path
import html
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
.block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1380px;}
.hero-card {background: radial-gradient(circle at top left, rgba(56,189,248,.20), transparent 30%), linear-gradient(135deg, #101827 0%, #172036 58%, #0b1220 100%); border: 1px solid #263247; border-radius: 26px; padding: 34px; margin-bottom: 22px; box-shadow: 0 18px 45px rgba(0,0,0,.30);}
.hero-title {font-size: 44px; font-weight: 850; letter-spacing: -0.04em; margin-bottom: 10px;}
.hero-subtitle {font-size: 17px; color: #c3cee5; max-width: 960px; line-height: 1.65;}
.badge {display: inline-block; padding: 7px 12px; margin: 6px 6px 0 0; border-radius: 999px; background: #1f2a44; border: 1px solid #34415f; color: #dfe7ff; font-size: 13px;}
.card {background: #111827; border: 1px solid #263247; border-radius: 18px; padding: 20px; height: 100%; box-shadow: inset 0 1px 0 rgba(255,255,255,.03);}
.card-title {font-size: 14px; color: #a9b4c7; margin-bottom: 8px;}
.card-value {font-size: 30px; font-weight: 800; color: #ffffff; margin-bottom: 6px;}
.card-note {font-size: 13px; color: #a9b4c7; line-height: 1.5;}
.section-title {font-size: 27px; font-weight: 800; margin: 28px 0 14px 0; letter-spacing: -.02em;}
.small-muted {color: #a9b4c7; font-size: 14px; line-height: 1.55;}
.insight {background: #0f172a; border-left: 4px solid #38bdf8; border-radius: 14px; padding: 16px 18px; margin: 10px 0;}
.warning {background: #201a10; border-left: 4px solid #f59e0b; border-radius: 14px; padding: 16px 18px; margin: 10px 0;}
.success {background: #102018; border-left: 4px solid #22c55e; border-radius: 14px; padding: 16px 18px; margin: 10px 0;}
.danger {background: #231316; border-left: 4px solid #ef4444; border-radius: 14px; padding: 16px 18px; margin: 10px 0;}
.priority-high {background:#3f1d22; color:#fecaca; border:1px solid #7f1d1d; padding:5px 10px; border-radius:999px; font-size:12px;}
.priority-medium {background:#33280f; color:#fde68a; border:1px solid #92400e; padding:5px 10px; border-radius:999px; font-size:12px;}
.rec-card {background:#111827; border:1px solid #263247; border-radius:18px; padding:18px 20px; margin:12px 0;}
.rec-title {font-size:16px; font-weight:800; margin-bottom:8px;}
.rec-meta {color:#a9b4c7; font-size:13px; margin-bottom:12px;}
hr {border-color:#263247;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    if not KPI_FILE.exists() or not REC_FILE.exists():
        st.error("Generated outputs are missing. Run the pipeline scripts first.")
        st.code("python src/build_large_campaign_dataset.py\npython src/calculate_kpis.py\npython src/rule_engine.py\npython src/generate_visuals.py")
        st.stop()
    kpi = pd.read_csv(KPI_FILE)
    rec = pd.read_csv(REC_FILE)
    if "date" in kpi.columns:
        kpi["date"] = pd.to_datetime(kpi["date"], errors="coerce")
    return kpi, rec

def money(x):
    return f"₹{x:,.0f}"

def pct(x):
    return f"{x:.2f}%"

def safe_html(value):
    return html.escape(str(value))

def plot_style(fig, height=None):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=24, r=24, t=52, b=32),
        font=dict(size=13),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    if height:
        fig.update_layout(height=height)
    return fig

def metric_card(title, value, note="", kind="card"):
    st.markdown(
        f"<div class='{kind}'><div class='card-title'>{safe_html(title)}</div><div class='card-value'>{safe_html(value)}</div><div class='card-note'>{safe_html(note)}</div></div>",
        unsafe_allow_html=True,
    )

def get_summary(kpi, rec):
    spend = kpi["spend"].sum()
    impressions = kpi["impressions"].sum()
    clicks = kpi["clicks"].sum()
    leads = kpi["leads"].sum()
    qualified = kpi["qualified_leads"].sum() if "qualified_leads" in kpi.columns else 0
    ctr = clicks / impressions * 100 if impressions else 0
    cpl = spend / leads if leads else 0
    high_share = len(rec[rec["priority"] == "High"]) / max(len(rec), 1)
    health_score = max(0, min(100, int(100 - (high_share * 55) - (cpl / 100))))
    return spend, impressions, clicks, leads, qualified, ctr, cpl, health_score

def render_hero(kpi, rec):
    spend, impressions, clicks, leads, qualified, ctr, cpl, health_score = get_summary(kpi, rec)
    st.markdown(f"""
    <div class='hero-card'>
      <div class='hero-title'>📈 AI Campaign Health Intelligence</div>
      <div class='hero-subtitle'>A professional portfolio web app that simulates how performance marketing teams combine ad-platform exports, GA4-style behavior data, and CRM lead-quality data to monitor campaign health and prioritize optimization actions.</div>
      <div style='margin-top:14px'>
        <span class='badge'>Google Ads</span><span class='badge'>Meta Ads</span><span class='badge'>LinkedIn Ads</span><span class='badge'>GA4-style events</span><span class='badge'>CRM lead quality</span><span class='badge'>Python + Streamlit</span><span class='badge'>Plotly dashboard</span>
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
    st.metric("Average CTR", pct(ctr))

def render_filters(kpi, rec):
    with st.sidebar:
        st.header("Control Panel")
        platforms = st.multiselect("Platforms", sorted(kpi["platform"].unique()), default=sorted(kpi["platform"].unique()))
        priorities = st.multiselect("Priorities", sorted(rec["priority"].unique()), default=sorted(rec["priority"].unique()))
        qualities = st.multiselect("Lead Quality", sorted(kpi["lead_quality"].unique()), default=sorted(kpi["lead_quality"].unique()))
        st.divider()
        st.caption("Use filters to simulate how a campaign analyst reviews platform, lead quality, and recommendation priority.")
    return platforms, priorities, qualities

def render_key_insights(kpi_f, rec_f):
    st.markdown("<div class='section-title'>Executive Insights</div>", unsafe_allow_html=True)
    platform_leads = kpi_f.groupby("platform")["leads"].sum().sort_values(ascending=False)
    platform_spend = kpi_f.groupby("platform")["spend"].sum().sort_values(ascending=False)
    campaign = kpi_f.groupby(["platform", "campaign_name"], as_index=False).agg({"spend":"sum", "leads":"sum", "qualified_leads":"sum"})
    campaign["cpl"] = campaign["spend"] / campaign["leads"].replace(0, pd.NA)
    campaign = campaign.fillna(0)
    worst_cpl = campaign[campaign["leads"] > 0].sort_values("cpl", ascending=False).head(1)
    scale_count = len(rec_f[rec_f["issue"].str.contains("Scale", case=False, na=False)])
    high_count = len(rec_f[rec_f["priority"] == "High"])

    best_platform = platform_leads.index[0] if not platform_leads.empty else "N/A"
    best_platform_value = int(platform_leads.iloc[0]) if not platform_leads.empty else 0
    top_spend_platform = platform_spend.index[0] if not platform_spend.empty else "N/A"
    top_spend_value = platform_spend.iloc[0] if not platform_spend.empty else 0
    worst_name = worst_cpl.iloc[0]["campaign_name"] if not worst_cpl.empty else "N/A"
    worst_value = worst_cpl.iloc[0]["cpl"] if not worst_cpl.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Top Lead Platform", best_platform, f"{best_platform_value:,} leads generated", "success")
    with c2:
        metric_card("Highest Spend Platform", top_spend_platform, f"{money(top_spend_value)} media spend", "insight")
    with c3:
        metric_card("Highest CPL Campaign", worst_name[:38] + ("..." if len(worst_name) > 38 else ""), f"Approx. {money(worst_value)} per lead", "warning")
    with c4:
        metric_card("Priority Workload", f"{high_count} high issues", f"{scale_count} scale candidates found", "danger" if high_count else "success")

def render_charts(kpi_f, rec_f):
    st.markdown("<div class='section-title'>Executive Visual Analytics</div>", unsafe_allow_html=True)
    left, right = st.columns(2)
    platform_spend = kpi_f.groupby("platform", as_index=False)["spend"].sum()
    platform_leads = kpi_f.groupby("platform", as_index=False)["leads"].sum()
    fig_spend = px.pie(platform_spend, names="platform", values="spend", hole=.58, title="Spend Share by Platform")
    fig_leads = px.pie(platform_leads, names="platform", values="leads", hole=.58, title="Lead Share by Platform")
    left.plotly_chart(plot_style(fig_spend, 430), use_container_width=True)
    right.plotly_chart(plot_style(fig_leads, 430), use_container_width=True)

    funnel_values = [
        int(kpi_f["impressions"].sum()),
        int(kpi_f["clicks"].sum()),
        int(kpi_f["leads"].sum()),
        int(kpi_f["qualified_leads"].sum()) if "qualified_leads" in kpi_f.columns else 0,
    ]
    fig_funnel = go.Figure(go.Funnel(y=["Impressions", "Clicks", "Leads", "Qualified Leads"], x=funnel_values, textinfo="value+percent previous"))
    fig_funnel.update_layout(title="Full Funnel: Impression to Qualified Lead")
    st.plotly_chart(plot_style(fig_funnel, 430), use_container_width=True)

    c1, c2 = st.columns(2)
    if "date" in kpi_f.columns:
        daily = kpi_f.groupby("date", as_index=False).agg({"spend":"sum", "leads":"sum"}).sort_values("date")
    else:
        daily = pd.DataFrame()
    if not daily.empty:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(x=daily["date"], y=daily["spend"], name="Spend", marker_color="#38bdf8", opacity=.75))
        fig_trend.add_trace(go.Scatter(x=daily["date"], y=daily["leads"], name="Leads", mode="lines+markers", marker_color="#f97316", yaxis="y2"))
        fig_trend.update_layout(
            title="Daily Spend vs Lead Trend",
            yaxis=dict(title="Spend"),
            yaxis2=dict(title="Leads", overlaying="y", side="right", showgrid=False),
            bargap=.42,
        )
        c1.plotly_chart(plot_style(fig_trend, 430), use_container_width=True)

    issue_summary = rec_f.groupby(["issue", "priority"], as_index=False).size().sort_values("size", ascending=True)
    fig_issue = px.bar(issue_summary, x="size", y="issue", color="priority", orientation="h", title="Issues by Type and Priority", text="size")
    fig_issue.update_traces(textposition="outside")
    c2.plotly_chart(plot_style(fig_issue, 430), use_container_width=True)

    ranked = kpi_f.groupby(["platform", "campaign_name"], as_index=False).agg({"leads":"sum", "spend":"sum", "qualified_leads":"sum"})
    ranked["cpl"] = ranked["spend"] / ranked["leads"].replace(0, pd.NA)
    ranked = ranked.fillna(0).sort_values("leads", ascending=True).tail(10)
    fig_rank = px.bar(ranked, x="leads", y="campaign_name", color="platform", orientation="h", title="Top Campaigns by Lead Volume", hover_data=["spend", "qualified_leads", "cpl"])
    st.plotly_chart(plot_style(fig_rank, 520), use_container_width=True)

def render_insights(kpi_f, rec_f):
    st.markdown("<div class='section-title'>Optimization Command Center</div>", unsafe_allow_html=True)
    high = rec_f[rec_f["priority"] == "High"]
    medium = rec_f[rec_f["priority"] == "Medium"]
    scale = rec_f[rec_f["issue"].str.contains("Scale", case=False, na=False)]
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("High Priority Issues", str(len(high)), "Needs review before scaling.", "warning")
    with c2:
        metric_card("Medium Priority Issues", str(len(medium)), "Monitor and test improvements.", "insight")
    with c3:
        metric_card("Scale Candidates", str(len(scale)), "Increase budget gradually after quality check.", "success")

    st.subheader("Priority Recommendation Cards")
    issue_icons = {
        "Landing Page Issue": "🧭",
        "Lead Quality Issue": "🎯",
        "Creative Issue": "🎨",
        "Traffic Quality Issue": "🚦",
        "Form Friction": "📝",
        "Scale Candidate": "📈",
    }
    if high.empty:
        st.success("No high-priority recommendations found for the selected filters.")
        return

    for _, row in high.head(6).iterrows():
        icon = issue_icons.get(row["issue"], "⚠️")
        priority_class = "priority-high" if row["priority"] == "High" else "priority-medium"
        st.markdown(f"""
        <div class='rec-card'>
          <div class='rec-title'>{icon} {safe_html(row['platform'])} · {safe_html(row['campaign_name'])}</div>
          <div class='rec-meta'>{safe_html(row.get('ad_group_or_ad_set', ''))} · {safe_html(row.get('ad_name', ''))}</div>
          <span class='badge'>{safe_html(row['issue'])}</span> <span class='{priority_class}'>{safe_html(row['priority'])}</span><br><br>
          <b>Reason:</b> {safe_html(row['reason'])}<br>
          <b>Recommended action:</b> {safe_html(row['recommended_action'])}<br>
          <b>Human approval:</b> {safe_html(row['human_approval_required'])}
        </div>
        """, unsafe_allow_html=True)

    remaining = high.iloc[6:]
    if not remaining.empty:
        with st.expander(f"View {len(remaining)} more high-priority recommendations"):
            st.dataframe(remaining, use_container_width=True)

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

def render_report(kpi, rec):
    st.markdown("<div class='section-title'>Generated Report</div>", unsafe_allow_html=True)
    spend, impressions, clicks, leads, qualified, ctr, cpl, health_score = get_summary(kpi, rec)
    high = rec[rec["priority"] == "High"]
    scale = rec[rec["issue"].str.contains("Scale", case=False, na=False)]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Report Score", f"{health_score}/100", "Overall campaign health estimate", "insight")
    with c2:
        metric_card("Total Recommendations", str(len(rec)), "All flagged optimization items", "card")
    with c3:
        metric_card("High Priority", str(len(high)), "Needs human review first", "warning")
    with c4:
        metric_card("Scale Candidates", str(len(scale)), "Potential controlled growth", "success")

    st.subheader("Top Issue Summary")
    issue_summary = rec.groupby(["issue", "priority"], as_index=False).size().sort_values("size", ascending=False)
    st.dataframe(issue_summary.rename(columns={"size": "count"}), use_container_width=True)

    st.subheader("Executive Notes")
    st.markdown("""
    <div class='card'>
      This report is generated using rule-based campaign logic. In a real commercial workflow, recommendations should be reviewed with campaign objective, sales feedback, CRM lead status, audience size, attribution window, and historical benchmark context before changes are applied.
      <br><br><b>Safe automation principle:</b> the system recommends actions, but does not directly change live campaigns without human approval.
    </div>
    """, unsafe_allow_html=True)

    if REPORT_FILE.exists():
        with st.expander("View full technical markdown report"):
            st.markdown(REPORT_FILE.read_text(encoding="utf-8"))
    else:
        st.info("Report not found. Run rule_engine.py first.")

def render_resume():
    st.markdown("<div class='section-title'>Resume / Interview View</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><b>Project positioning:</b> Multi-source performance marketing analytics and campaign optimization dashboard.<br><br><b>Tools:</b> Python, Pandas, Plotly, Streamlit, Matplotlib, CSV data pipeline, rule-based recommendations.<br><br><b>Data simulated:</b> Google Ads, Meta Ads, LinkedIn Ads, GA4-style events, CRM lead quality and revenue.</div>", unsafe_allow_html=True)
    st.subheader("Resume Bullet")
    st.code("Built a Python and Streamlit-based campaign health intelligence web app combining simulated Google Ads, Meta Ads, LinkedIn Ads, GA4-style behavior data, and CRM lead-quality data to calculate KPIs, visualize funnel performance, and generate human-approved optimization recommendations.")
    st.subheader("Interview Pitch")
    st.info("This project simulates a real performance marketing operations workflow: ad platform data shows delivery, GA4-style data shows post-click behavior, CRM data shows lead quality, and the dashboard converts that combined data into optimization priorities for a marketer or manager.")

def main():
    kpi, rec = load_data()
    render_hero(kpi, rec)
    platforms, priorities, qualities = render_filters(kpi, rec)
    kpi_f = kpi[kpi["platform"].isin(platforms) & kpi["lead_quality"].isin(qualities)]
    rec_f = rec[rec["platform"].isin(platforms) & rec["priority"].isin(priorities)]
    t1, t2, t3, t4 = st.tabs(["📊 Dashboard", "🔄 Data Pipeline", "📄 Report", "💼 Resume View"])
    with t1:
        render_key_insights(kpi_f, rec_f)
        render_charts(kpi_f, rec_f)
        render_insights(kpi_f, rec_f)
        st.subheader("Campaign KPI Data")
        st.dataframe(kpi_f, use_container_width=True)
    with t2:
        render_pipeline(kpi)
    with t3:
        render_report(kpi, rec)
    with t4:
        render_resume()

if __name__ == "__main__":
    main()
