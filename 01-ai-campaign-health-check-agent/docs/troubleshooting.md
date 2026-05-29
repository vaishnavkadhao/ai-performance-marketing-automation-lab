# Troubleshooting

This file documents common issues that can occur in campaign tracking, reporting, and automation workflows.

## GA4 and Ad Platform Numbers Do Not Match

Common causes:

- Different attribution windows
- Different time zones
- Clicks vs sessions mismatch
- Consent mode or ad blockers
- Delayed conversions
- Missing or inconsistent UTMs

Recommended checks:

- Use ad platforms for media delivery metrics.
- Use GA4 for website behavior.
- Use CRM for lead quality and sales status.
- Compare trends instead of expecting exact one-to-one matching.

## GTM Tag Not Firing

Common causes:

- Wrong trigger condition
- Button class or ID changed
- Form reloads before tag fires
- Consent settings block the tag
- Wrong GTM container installed

Recommended checks:

- Use GTM Preview mode.
- Check variables and triggers.
- Check GA4 DebugView.
- Test on mobile and desktop.

## Duplicate Conversions

Common causes:

- Same action tracked from button click and thank-you page
- Form submit event fires multiple times
- User refreshes thank-you page
- Browser pixel and server-side event are not deduplicated

Recommended checks:

- Define one primary conversion event.
- Avoid duplicate triggers.
- Use event IDs for deduplication where required.

## AI or Rule Recommendations Look Incorrect

Common causes:

- Incomplete data
- Missing target CPL or benchmark
- Small sample size
- Wrong campaign objective
- No CRM quality feedback

Recommended checks:

- Review source data quality.
- Confirm thresholds.
- Add business context before taking action.
- Require human approval before campaign changes.

## UTM Data Is Broken

Common causes:

- Missing UTM parameters
- Inconsistent naming
- Spaces and special characters
- Wrong source or medium

Recommended checks:

- Use a UTM builder template.
- Standardize naming rules.
- Use lowercase names.
- Review URLs before campaign launch.

## Lead Quality Is Poor Despite Low CPL

Common causes:

- Audience too broad
- Offer attracts low-intent users
- Form has no qualification fields
- Ad copy overpromises

Recommended checks:

- Add qualifying form fields.
- Connect CRM status to reporting.
- Optimize for qualified leads, not only lead volume.
