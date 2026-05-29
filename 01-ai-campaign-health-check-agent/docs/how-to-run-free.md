# How to Run This Project for Free

This guide explains how to run the AI Campaign Health Check Agent without paid tools.

## Option 1: Run Locally on Your Laptop - Recommended

### Why use this option?

This is the best option for learning because you understand what is happening step by step.

### Free tools needed

- Python
- VS Code
- GitHub repository
- Terminal or Command Prompt

### Steps

1. Download or clone the GitHub repository.
2. Open the repository in VS Code.
3. Open terminal.
4. Move into the project folder:

```bash
cd 01-ai-campaign-health-check-agent
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run KPI calculator:

```bash
python src/calculate_kpis.py
```

7. Run rule engine:

```bash
python src/rule_engine.py
```

8. Check generated files:

```text
outputs/campaign_kpis.csv
outputs/campaign_recommendations.csv
outputs/sample-campaign-health-report.md
```

## Option 2: Run in Google Colab - Free Browser Option

### Why use this option?

Use this if Python is not installed on your laptop.

### Steps

1. Open Google Colab.
2. Create a new notebook.
3. Upload `campaign_performance_sample.csv`.
4. Copy the logic from `calculate_kpis.py` and `rule_engine.py` into notebook cells.
5. Run the cells.
6. Download the output CSV/report files.

### Limitation

Colab is easy for practice, but GitHub project structure is cleaner when code is kept in the repository.

## Option 3: Use GitHub Codespaces - May Have Free Monthly Limits

### Why use this option?

It runs VS Code in the browser and is useful if your laptop setup has issues.

### Caution

Free usage may have monthly limits. Use it carefully and stop the Codespace when not using it.

## What This Project Does

```text
Raw campaign CSV
↓
KPI calculator
↓
Campaign KPI CSV
↓
Rule engine
↓
Recommendation CSV + Markdown report
```

## Why This Step Is Important

Before adding AI, dashboards, or APIs, the basic campaign logic must work.

In real companies, AI should not blindly decide campaign actions. A professional workflow uses:

```text
Data → KPI logic → rule checks → AI explanation → human approval
```

## Common Errors

### Error: pandas not found

Fix:

```bash
pip install -r requirements.txt
```

### Error: input file not found

Fix:

Make sure you are running commands from inside:

```text
01-ai-campaign-health-check-agent
```

### Error: tabulate missing

Fix:

```bash
pip install tabulate
```

### Error: Permission denied

Fix:

Close the CSV/report file if it is already open in Excel, then run the script again.

## Next Upgrade

After this works, the next upgrades are:

1. Add AI summary prompt.
2. Add Streamlit dashboard.
3. Add GitHub Actions scheduled automation.
4. Add GA4/Google Ads API read-only integrations later.
