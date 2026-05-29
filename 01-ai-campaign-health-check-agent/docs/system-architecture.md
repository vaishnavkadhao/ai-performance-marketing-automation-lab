# System Architecture

## Objective

The Campaign Health Check Agent analyzes paid media campaign data, calculates core performance KPIs, flags optimization opportunities, and generates structured reporting outputs.

## Input Data

The current version uses a sample CSV dataset with campaign-level fields:

- Platform
- Campaign name
- Ad group or ad set
- Ad name
- Spend
- Impressions
- Clicks
- Leads
- Sessions
- Engaged sessions
- Form starts
- Form submits
- Lead quality
- Landing page

## Processing Flow

```text
Sample campaign CSV
↓
KPI calculator
↓
Campaign KPI output
↓
Rule engine
↓
Recommendations output
↓
Markdown report + visual charts
```

## KPI Layer

The system calculates:

- CTR
- CPC
- CPM
- CPL
- Conversion rate
- Engagement rate
- Form completion rate

## Recommendation Layer

The rule engine flags:

- Creative issues
- Landing page issues
- Form friction
- Lead quality issues
- Traffic quality issues
- Scale candidates
- Wasted spend risks

## Outputs

Generated outputs are stored in:

```text
outputs/campaign_kpis.csv
outputs/campaign_recommendations.csv
outputs/sample-campaign-health-report.md
outputs/visuals/
```

## Future Enhancements

- GA4 Data API integration
- Google Ads API read-only reporting
- Meta Ads reporting integration
- CRM lead quality feedback
- Streamlit dashboard
- Scheduled GitHub Actions workflow
- Human-approved optimization workflow
