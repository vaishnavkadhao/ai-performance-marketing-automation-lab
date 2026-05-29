# Optimization Rules for Campaign Health Check Agent

This file defines the rule logic used to classify campaign issues and recommendations.

These rules are designed for learning and portfolio demonstration. In real campaigns, thresholds should be adjusted based on industry, budget, funnel type, objective, seasonality, and historical benchmarks.

---

## Rule 1: Wasted Spend

### Logic

```text
If spend is high and leads are zero, flag as Wasted Spend.
```

### Why it matters

A campaign spending money without leads may have targeting, keyword, creative, offer, landing page, or tracking issues.

### Recommended action

- Check conversion tracking first.
- Review landing page and form.
- Check search terms, audience, placement, or targeting.
- Do not increase budget until the issue is diagnosed.

---

## Rule 2: Creative Issue

### Logic

```text
If impressions are high and CTR is low, flag as Creative Issue.
```

### Why it matters

The ad is being shown, but users are not clicking. This can mean the hook, creative, headline, offer, or audience match is weak.

### Recommended action

- Test new hooks.
- Test new visuals.
- Improve offer clarity.
- Rewrite headline and CTA.
- Check whether the audience is relevant.

---

## Rule 3: Landing Page Issue

### Logic

```text
If clicks are high but leads are low, flag as Landing Page Issue.
```

### Why it matters

Users are interested enough to click, but something after the click is stopping them from converting.

### Possible causes

- Weak above-the-fold message
- Slow page speed
- Poor mobile experience
- Weak CTA
- Trust issue
- Form not visible
- Offer mismatch
- Broken form or tracking

### Recommended action

- Check page speed.
- Review mobile layout.
- Check CTA visibility.
- Test shorter form.
- Match ad message with landing page headline.

---

## Rule 4: Form Friction

### Logic

```text
If form starts are high but form submits are low, flag as Form Friction.
```

### Why it matters

Users are interested, but the form experience is stopping completion.

### Recommended action

- Reduce form fields.
- Check mobile usability.
- Add trust indicators near form.
- Improve submit button copy.
- Check technical errors.

---

## Rule 5: Scale Candidate

### Logic

```text
If CPL is below target and lead quality is good, flag as Scale Candidate.
```

### Why it matters

This campaign is generating useful leads at an efficient cost.

### Recommended action

- Increase budget gradually.
- Duplicate winning creative into new tests.
- Expand audience or keyword set carefully.
- Monitor CPL and quality after scaling.

---

## Rule 6: Lead Quality Issue

### Logic

```text
If lead volume is good but lead quality is poor, flag as Lead Quality Issue.
```

### Why it matters

Cheap leads are not useful if sales cannot convert them.

### Recommended action

- Add qualifying questions to forms.
- Narrow targeting.
- Improve ad copy to set expectations.
- Exclude irrelevant audiences/keywords.
- Connect CRM status back into reports.

---

## Rule 7: Tracking Review

### Logic

```text
If clicks are high but sessions are unusually low, flag as Tracking Review.
```

### Why it matters

This can indicate tracking gaps, page load issues, redirect issues, consent blocking, or analytics configuration problems.

### Recommended action

- Test with GTM Preview.
- Check GA4 DebugView.
- Check UTM parameters.
- Check landing page load and redirects.
- Compare ad platform clicks with GA4 sessions carefully.

---

## Rule 8: Traffic Quality Issue

### Logic

```text
If sessions are high but engaged sessions are low, flag as Traffic Quality Issue.
```

### Why it matters

Users are arriving but not engaging. The campaign may be attracting low-quality traffic.

### Recommended action

- Review audience/placement/search terms.
- Check landing page relevance.
- Exclude poor placements.
- Improve keyword intent.
- Adjust creative promise to match landing page.

---

## Rule 9: Budget Pacing Issue

### Logic

```text
If actual spend is much higher than expected spend for the period, flag as Overspending Risk.
If actual spend is much lower than expected spend, flag as Underdelivery Risk.
```

### Why it matters

Budget pacing helps ensure that monthly spend is controlled and aligned with goals.

### Recommended action

- Review daily budget settings.
- Check campaign delivery status.
- Shift budget from weak campaigns to stronger campaigns.
- Avoid aggressive daily budget changes without enough data.

---

## Professional Safety Rule

The agent should not automatically change live campaign settings in the first version.

Correct workflow:

```text
Detect issue → Explain reason → Recommend action → Human approval → Manual/API execution → Monitor result
```

This is safer and closer to how real marketing teams work.
