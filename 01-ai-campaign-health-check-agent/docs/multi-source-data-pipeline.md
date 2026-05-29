# Multi-Source Campaign Data Pipeline

## Overview

This module simulates how paid media, web analytics, and CRM data can be combined into one campaign health dataset for KPI reporting and optimization analysis.

## Source Data

| Source File | Represents | Main Fields |
|---|---|---|
| `sample-data/raw/google_ads_sample_large.csv` | Google Ads export | spend, impressions, clicks, campaign data |
| `sample-data/raw/meta_ads_sample_large.csv` | Meta Ads export | spend, impressions, clicks, campaign data |
| `sample-data/raw/linkedin_ads_sample_large.csv` | LinkedIn Ads export | spend, impressions, clicks, B2B campaign data |
| `sample-data/raw/ga4_sample_large.csv` | GA4-style analytics export | sessions, engaged sessions, form starts, form submits, landing page |
| `sample-data/raw/crm_leads_sample_large.csv` | CRM or sales feedback export | leads, qualified leads, meetings, deals won, revenue, lead quality |

## Processing Flow

```text
Raw ad platform data
+ GA4-style behavior data
+ CRM lead quality data
↓
Join by date + platform + campaign_id + campaign_name
↓
Processed campaign health dataset
↓
KPI calculation
↓
Recommendation engine
↓
Charts and Streamlit dashboard
```

## Processed Output

```text
sample-data/processed/campaign_health_large_sample.csv
```

## Why Raw Data Is Kept Separate

Raw files are kept separate to preserve the original source structure and avoid mixing data before validation. The processed dataset is created only after campaign identifiers and dates are aligned.

## Join Keys

The sample pipeline uses:

```text
date
platform
campaign_id
campaign_name
```

In real projects, campaign IDs and UTM naming rules are important because inconsistent names can break reporting and attribution.

## Dashboard Output

The Streamlit dashboard reads the generated KPI and recommendation outputs and presents campaign performance, issue summaries, high-priority recommendations, and report previews.
