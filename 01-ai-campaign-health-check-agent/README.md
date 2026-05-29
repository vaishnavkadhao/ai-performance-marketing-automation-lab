# Project 1: AI Campaign Health Check Agent

## Goal

Build a practical campaign analysis system that reads paid media data, calculates key performance marketing KPIs, detects campaign issues, and creates optimization recommendations.

This project simulates how a performance marketing analyst or marketing automation executive reviews campaign performance inside an agency, SaaS company, or growth team.

## Business Problem

Marketing teams often run campaigns across Google Ads, Meta Ads, LinkedIn, and other platforms. The challenge is not only launching campaigns, but understanding:

- Which campaign is wasting budget?
- Which ad or creative has weak engagement?
- Which campaign has high clicks but low leads?
- Which landing page has form friction?
- Which campaign can be scaled?
- Which campaign needs tracking or lead quality review?

## Solution

This project creates a campaign health check workflow:

1. Import campaign performance data.
2. Calculate KPIs such as CTR, CPC, CPM, CPL, CVR, engagement rate, and form completion rate.
3. Apply rule-based checks to identify issues.
4. Generate structured optimization recommendations.
5. Convert the findings into a client-friendly report.
6. Later, add an AI summary layer for easier reporting.

## Files in This Module

| File/Folder | Purpose |
|---|---|
| `sample-data/campaign_performance_sample.csv` | Practice dataset for Google Ads, Meta Ads, and LinkedIn-style campaigns |
| `docs/kpi-definitions.md` | Explains all KPIs used in this project |
| `docs/optimization-rules.md` | Explains rule logic used to detect campaign issues |
| `docs/errors-and-fixes.md` | Common real-world issues and troubleshooting notes |
| `src/` | Python scripts will be added here later |
| `outputs/` | Sample generated reports will be stored here later |

## KPIs Covered

- Impressions
- Clicks
- Spend
- CTR
- CPC
- CPM
- Leads
- Cost per Lead
- Conversion Rate
- Sessions
- Engaged Sessions
- Engagement Rate
- Form Starts
- Form Submits
- Form Completion Rate
- Lead Quality

## Optimization Categories

The project classifies issues into categories:

| Category | Meaning |
|---|---|
| Wasted Spend | Campaign is spending but not generating leads |
| Creative Issue | Impressions are high but CTR is weak |
| Landing Page Issue | Clicks are coming but users are not taking action |
| Form Friction | Users start the form but do not submit it |
| Scale Candidate | Campaign has strong CPL and good lead quality |
| Lead Quality Issue | Campaign generates leads but quality is poor |
| Tracking Review | Numbers suggest tracking may be broken or incomplete |

## Professional Learning Outcome

After completing this project, you should be able to explain campaign performance like this:

> The campaign is receiving enough traffic, but the conversion rate is weak. Since clicks are high and form submissions are low, the issue may be with landing page clarity, form friction, CTA placement, or offer relevance. I would first check tracking, then review the landing page and run a new CTA/form test before increasing budget.

## Current Status

- [x] Project folder created
- [x] Sample data added
- [x] KPI definitions added
- [x] Optimization rules added
- [ ] Python KPI calculator
- [ ] Rule engine script
- [ ] Sample output report
- [ ] AI summary prompt
