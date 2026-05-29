# 🚀 AI Performance Marketing Automation Lab

<p align="center">
  <img src="assets/dashboard-preview.svg" alt="AI Performance Marketing Automation Lab dashboard preview" width="100%">
</p>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-active-blue">
  <img alt="Focus" src="https://img.shields.io/badge/focus-performance%20marketing-orange">
  <img alt="Tracking" src="https://img.shields.io/badge/tracking-GTM%20%7C%20GA4-green">
  <img alt="Automation" src="https://img.shields.io/badge/automation-python%20%7C%20AI-purple">
  <img alt="Repo" src="https://img.shields.io/badge/portfolio-case%20study-black">
</p>

## 🎯 Project Overview

A performance marketing automation case study focused on campaign health checks, KPI analysis, measurement planning, dashboard reporting, UTM governance, and human-approved optimization workflows.

The project demonstrates how paid media data can be converted into structured insights for budget control, campaign prioritization, reporting, and optimization decisions.

> **Core idea:** Campaign optimization should be driven by clean tracking, meaningful KPIs, lead quality signals, and explainable recommendations.

---

## 🖥️ Interactive Dashboard Preview

<p align="center">
  <img src="assets/streamlit-dashboard-preview.png" alt="Streamlit campaign health dashboard preview" width="100%">
</p>

<p align="center">
  <img src="assets/streamlit-recommendation-summary.png" alt="Streamlit recommendation summary preview" width="48%">
  <img src="assets/streamlit-generated-report-overview.png" alt="Streamlit generated report preview" width="48%">
</p>

---

## 🧠 Workflow

```mermaid
flowchart LR
    A[Ad Platforms] --> B[Campaign Data]
    B --> C[KPI Calculator]
    C --> D[Rule-Based Health Check]
    D --> E[Recommendation Output]
    E --> F[Human Review]
    F --> G[Manual/API Optimization]
    G --> H[Dashboard + Report]
```

---

## 📦 Repository Modules

| Module | Purpose | Key Skills Demonstrated |
|---|---|---|
| [`01-ai-campaign-health-check-agent`](01-ai-campaign-health-check-agent/) | Analyze campaign data and generate optimization recommendations | KPI analysis, rule-based logic, reporting, visual dashboard, wasted-spend detection |
| `02-gtm-ga4-measurement-dashboard-system` | Design campaign measurement and dashboard structure | GTM, GA4 events, UTM strategy, conversion QA, dashboard planning |
| `03-bulk-campaign-planner-utm-builder` | Prepare scalable campaign launch templates | Campaign naming, UTM builder, bulk planning, pre-launch QA |
| [`docs`](docs/) | Shared documentation and SOPs | Process design, troubleshooting, documentation |
| [`assets`](assets/) | Screenshots, diagrams, and dashboard visuals | Portfolio presentation support |

---

## 🛠️ Tools & Skills Covered

| Category | Tools / Skills |
|---|---|
| Performance Marketing | Google Ads, Meta Ads, LinkedIn Campaigns, Remarketing, A/B Testing, Campaign QA |
| Tracking & Analytics | GTM, GA4, UTM Tracking, Enhanced Conversions concepts, Looker Studio |
| Automation | Python, Pandas, Matplotlib, Streamlit, Google Sheets, GitHub Actions concepts |
| AI-Assisted Workflow | Campaign analysis, rule explanation, reporting summaries, recommendation logic |
| Data & Reporting | Excel, dashboard planning, KPI definitions, sample datasets, campaign reports |
| Marketing Operations | Lead quality, budget pacing, funnel diagnosis, landing page issue detection |

---

## 📊 Campaign Health Logic

| Signal | Possible Issue | Recommended Action |
|---|---|---|
| High spend + zero leads | Wasted spend | Check tracking, landing page, audience, and keywords before scaling |
| High impressions + low CTR | Creative or offer issue | Test new hooks, visuals, headlines, and CTAs |
| High clicks + low leads | Landing page issue | Review page speed, CTA clarity, form visibility, and offer match |
| High form starts + low submits | Form friction | Reduce fields, improve mobile form UX, check form errors |
| Low CPL + good lead quality | Scale candidate | Increase budget gradually and monitor quality |
| Good lead volume + poor quality | Lead quality issue | Improve targeting, add qualifying questions, connect CRM feedback |

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A[Google Ads / Meta Ads / LinkedIn Ads] --> B[Landing Page]
    B --> C[GTM Events]
    C --> D[GA4 + Ad Platform Conversion Data]
    D --> E[Campaign Dataset]
    E --> F[KPI Calculator]
    F --> G[Optimization Rule Engine]
    G --> H[Report + Visuals]
    H --> I[Streamlit Dashboard]
    I --> J[Human Review]
    J --> K[Campaign Optimization]
```

---

## 📁 Project Status

| Area | Status |
|---|---|
| Repository setup | ✅ Done |
| Dashboard preview visual | ✅ Done |
| Campaign health check module | ✅ Done |
| Sample campaign data | ✅ Done |
| KPI calculator | ✅ Done |
| Rule engine | ✅ Done |
| Sample report output | ✅ Done |
| Campaign charts | ✅ Done |
| Streamlit dashboard | ✅ Done |
| GTM/GA4 measurement module | ⏳ Upcoming |
| UTM builder module | ⏳ Upcoming |

---

## 🖼️ Current Outputs

Project 1 generates:

- [`campaign_kpis.csv`](01-ai-campaign-health-check-agent/outputs/campaign_kpis.csv)
- [`campaign_recommendations.csv`](01-ai-campaign-health-check-agent/outputs/campaign_recommendations.csv)
- [`sample-campaign-health-report.md`](01-ai-campaign-health-check-agent/outputs/sample-campaign-health-report.md)
- Campaign visual charts in [`outputs/visuals`](01-ai-campaign-health-check-agent/outputs/visuals/)
- Interactive dashboard through [`app.py`](01-ai-campaign-health-check-agent/app.py)

---

## ▶️ Run Project 1 Locally

```bash
cd 01-ai-campaign-health-check-agent
python -m pip install -r requirements.txt
python src/calculate_kpis.py
python src/rule_engine.py
python src/generate_visuals.py
python -m streamlit run app.py
```

---

## 👨‍💼 Professional Use Case

This project is relevant for roles such as:

- Performance Marketing Executive
- Digital Marketing Executive
- Campaign Analyst
- Marketing Automation Executive
- Growth Marketing Associate
- Marketing Operations Associate
- Ads Operations Specialist
- B2B Lead Generation Specialist

---

## 🔐 Security Note

This repository uses sample/demo data only.

Do not commit:

- API keys
- Google Ads tokens
- Meta access tokens
- GA4 credentials
- `.env` files
- Service account JSON files
- Real client campaign data

---

## 🧭 Roadmap

```mermaid
flowchart LR
    A[Campaign Health Check] --> B[Visual Reports]
    B --> C[Streamlit Dashboard]
    C --> D[GTM/GA4 Measurement Module]
    D --> E[Bulk Campaign Planner]
    E --> F[API-Based Reporting]
```

---

## 📌 Portfolio Positioning

> **AI-assisted performance marketing automation using campaign analytics, conversion tracking logic, visual reporting, dashboarding, and safe optimization workflows.**
