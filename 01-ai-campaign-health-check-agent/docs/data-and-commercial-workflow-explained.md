# Data and Commercial Workflow Explained

This document explains the logic behind the Campaign Health Check Agent from a marketing, analytics, and operations perspective.

---

## 1. What Kind of Data Is This?

The sample dataset represents paid marketing campaign data.

In real companies, similar data comes from:

- Google Ads
- Meta Ads
- LinkedIn Ads
- Google Analytics 4
- CRM systems such as HubSpot, Zoho, or Salesforce
- Landing page forms
- Call tracking tools
- Google Sheets or Excel exports

The current project uses a CSV file to simulate this because CSV files are free, easy to understand, and commonly used in real reporting workflows.

---

## 2. Main Data Categories

### Ad Platform Data

This tells us how the ad performed before the user reached the website.

Examples:

- Platform
- Campaign name
- Ad group or ad set
- Ad name
- Spend
- Impressions
- Clicks

This data answers:

> Did the ad reach people, and did they click?

### Website Analytics Data

This tells us what happened after the user clicked the ad.

Examples:

- Sessions
- Engaged sessions
- Landing page
- Form starts
- Form submits

This data answers:

> Did users engage after landing on the website?

### Lead Quality Data

This tells us whether the lead was useful for sales.

Examples:

- Good
- Average
- Poor
- Qualified
- Unqualified
- Meeting booked
- Deal won
- Deal lost

This data answers:

> Did the campaign generate business value, not just form submissions?

---

## 3. Why Raw Data Is Not Enough

Raw data only shows numbers.

Example:

```text
Spend = 2500
Clicks = 280
Leads = 5
```

But marketing decisions need calculated KPIs:

```text
CPL = Spend / Leads
CPL = 2500 / 5 = 500
```

Now we know each lead cost 500.

This is why the first script calculates KPIs.

---

## 4. Project Data Flow

```text
Raw campaign CSV
↓
KPI calculator
↓
Campaign KPI output
↓
Rule engine
↓
Recommendation output
↓
Markdown report
↓
Charts and dashboard
↓
Human review and action
```

---

## 5. Marketing Logic Behind the Rules

### Low CTR

If impressions are high but CTR is low, users are seeing the ad but not clicking.

Possible reasons:

- Weak creative
- Poor headline
- Weak offer
- Wrong audience
- Poor keyword intent

### High Clicks but Low Leads

If users click but do not convert, the issue may be after the click.

Possible reasons:

- Landing page is weak
- Form is too long
- CTA is unclear
- Page is slow
- Ad promise does not match page content

### Low CPL and Good Quality

If a campaign generates leads at low cost and the lead quality is good, it may be a scale candidate.

Action:

- Increase budget slowly
- Test similar audiences
- Expand keywords
- Monitor quality after scaling

### Good Lead Volume but Poor Quality

This is common in lead generation.

Possible reasons:

- Targeting is too broad
- Offer attracts low-intent users
- Form has no qualification questions
- Ad copy overpromises

Action:

- Add lead qualification questions
- Improve targeting
- Send lead status back from CRM

---

## 6. Marketing + Operations Perspective

This system improves efficiency because it reduces manual checking.

Without automation:

```text
Marketer downloads data manually
↓
Calculates KPIs manually
↓
Checks each campaign manually
↓
Writes recommendations manually
↓
Creates report manually
```

With automation:

```text
Data is loaded
↓
KPIs are calculated automatically
↓
Issues are flagged automatically
↓
Recommendations are generated automatically
↓
Marketer reviews and approves actions
```

This saves time and reduces human error.

---

## 7. Where Real Data Will Come From Later

### Google Ads

Google Ads provides delivery and cost data such as spend, impressions, clicks, CPC, conversions, and campaign structure.

Possible connection methods:

- Manual CSV export
- Google Sheets connector
- Looker Studio connector
- Google Ads API
- Google Ads Scripts

### Meta Ads

Meta Ads provides campaign, ad set, ad, creative, spend, impressions, clicks, CTR, CPC, CPM, and conversion data.

Possible connection methods:

- Manual CSV export
- Meta Ads Manager reports
- Third-party connectors
- Meta Marketing API

### GA4

GA4 provides website behavior data such as sessions, engagement, events, conversions, and landing page performance.

Possible connection methods:

- GA4 interface export
- Looker Studio connector
- GA4 Data API
- BigQuery export

### CRM

CRM systems provide lead quality data.

Examples:

- Qualified lead
- Unqualified lead
- Meeting booked
- Proposal sent
- Deal won
- Deal lost

Possible connection methods:

- CSV export
- Google Sheets sync
- HubSpot/Zoho/Salesforce API
- Zapier/Make/n8n workflow

---

## 8. How the Tools Connect in a Real Setup

```text
Google Ads / Meta Ads / LinkedIn Ads
↓
Landing Page
↓
GTM
↓
GA4 + Ad Platform Conversion Tags
↓
Looker Studio / BigQuery / CSV Export
↓
Python Campaign Health Check Agent
↓
Report + Dashboard + Recommendations
↓
Human Approval
↓
Campaign Optimization
```

---

## 9. Where the Output Will Show

Depending on the stage, the output can show in:

- CSV files
- Markdown reports
- GitHub repo
- Looker Studio dashboard
- Streamlit dashboard
- Google Sheets
- Email report
- Slack/Teams alert
- CRM notes

For this project, the first output is stored in:

```text
outputs/campaign_kpis.csv
outputs/campaign_recommendations.csv
outputs/sample-campaign-health-report.md
outputs/visuals/
```

---

## 10. How to Scale This for Large Data

For small data:

```text
CSV + Python + pandas
```

For medium data:

```text
Google Sheets + Python + Looker Studio
```

For large data:

```text
GA4 BigQuery Export + Google Ads API + Meta API + Python/SQL + Dashboard
```

Large-data workflow:

```text
Collect data daily
↓
Store in database or BigQuery
↓
Clean and standardize campaign names
↓
Join ad data with GA4 and CRM data
↓
Calculate KPIs
↓
Apply rules and AI summaries
↓
Send alerts/reports
```

---

## 11. Professional Reminder

The most valuable marketing automation does not only show clicks and leads. It connects:

```text
Spend → Traffic → Engagement → Lead → Qualified Lead → Revenue
```

That is how marketing becomes connected to business operations.
