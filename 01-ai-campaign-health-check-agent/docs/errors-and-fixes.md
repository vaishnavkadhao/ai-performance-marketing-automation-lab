# Real-World Errors and Fixes

This file documents common issues faced in campaign tracking, reporting, and automation workflows.

## 1. GA4 and Ad Platform Numbers Do Not Match

### Why it happens

- Different attribution windows
- Different time zones
- Clicks vs sessions are different metrics
- Consent mode or ad blockers
- Delayed conversions
- Duplicate or missing UTMs
- Cross-device user journeys

### Fix

- Use Google Ads or Meta Ads for media delivery metrics.
- Use GA4 for website behavior.
- Use CRM for lead quality and sales status.
- Compare trends instead of expecting exact one-to-one matching.

## 2. GTM Tag Not Firing

### Possible reasons

- Wrong trigger condition
- Button class or ID changed
- Form reloads before tag fires
- Trigger is too broad or too narrow
- Consent settings block the tag
- Wrong GTM container installed

### Fix

- Use GTM Preview mode.
- Check variables and triggers.
- Check GA4 DebugView.
- Test on mobile and desktop.
- Use thank-you page tracking when possible.

## 3. Duplicate Conversions

### Possible reasons

- Same action tracked through button click and thank-you page
- Form submit event fires multiple times
- User refreshes thank-you page
- Browser pixel and server-side event are not deduplicated

### Fix

- Define one primary conversion event.
- Use event IDs for deduplication where required.
- Avoid firing the same event from multiple triggers.
- Test with debug tools before publishing.

## 4. AI Gives Wrong Recommendations

### Possible reasons

- Data is incomplete
- Prompt is too broad
- AI is asked to guess
- No target CPL or benchmark is provided
- Rule results are not clearly structured

### Fix

- Use rule-based logic first.
- Ask AI only to explain findings.
- Add instruction: do not invent data.
- Provide benchmarks and business context.
- Force structured output in tables.

## 5. Automation Quota or Rate Limit Errors

### Possible reasons

- Too many API requests
- Free plan limits reached
- Apps Script execution time exceeded
- AI API rate limit reached
- Workflow scheduled too frequently

### Fix

- Run daily or hourly first, not every minute.
- Add retry logic.
- Add error logs.
- Use sample data for GitHub demos.
- Use local or free-tier tools only for practice.

## 6. Campaign Changes Become Too Aggressive

### Problem

Changing budgets, creatives, or bidding too often can disturb learning and performance stability.

### Fix

- Monitor frequently but optimize in controlled windows.
- Add human approval before changes.
- Keep a change log.
- Avoid major changes without enough data.

## 7. UTM Data Is Broken

### Possible reasons

- Missing UTM parameters
- Inconsistent naming
- Spaces and special characters
- Wrong source or medium
- Manual typing errors

### Fix

- Use a UTM builder template.
- Standardize naming rules.
- Use lowercase names.
- Avoid spaces.
- Review URLs before launch.

## 8. Lead Quality Is Poor Even When CPL Is Low

### Possible reasons

- Audience too broad
- Offer attracts low-intent users
- Form is too easy
- Ad copy overpromises
- Sales qualification criteria are not connected back to marketing

### Fix

- Add qualifying form fields.
- Connect CRM status to campaign report.
- Optimize for qualified leads, not only total leads.
- Review audience and search intent.

## Professional Reminder

In commercial marketing teams, fixing data and tracking issues is often more important than launching more campaigns. Clean data improves optimization quality.
