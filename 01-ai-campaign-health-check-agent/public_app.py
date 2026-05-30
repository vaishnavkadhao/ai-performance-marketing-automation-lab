"""
Public portfolio version of the Campaign Health Intelligence app.

Use this file for Streamlit deployment and public portfolio links.
It intentionally excludes resume/interview-only preparation content.

Run:
    python -m streamlit run public_app.py
"""

import streamlit as st
import pro_app as app


def main():
    kpi, rec = app.load_data()
    app.render_hero(kpi, rec)

    platforms, priorities, qualities = app.render_filters(kpi, rec)
    kpi_f = kpi[
        kpi["platform"].isin(platforms)
        & kpi["lead_quality"].isin(qualities)
    ]
    rec_f = rec[
        rec["platform"].isin(platforms)
        & rec["priority"].isin(priorities)
    ]

    dashboard_tab, pipeline_tab, report_tab = st.tabs([
        "📊 Dashboard",
        "🔄 Data Pipeline",
        "📄 Report",
    ])

    with dashboard_tab:
        app.render_key_insights(kpi_f, rec_f)
        app.render_charts(kpi_f, rec_f)
        app.render_insights(kpi_f, rec_f)
        st.subheader("Campaign KPI Data")
        st.dataframe(kpi_f, use_container_width=True)

    with pipeline_tab:
        app.render_pipeline(kpi)

    with report_tab:
        app.render_report(kpi, rec)


if __name__ == "__main__":
    main()
