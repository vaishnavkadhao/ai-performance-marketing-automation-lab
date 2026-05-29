# Setup and Run

## Requirements

- Python 3.10+
- pip
- Git
- VS Code or any code editor

## Setup

From the project folder:

```bash
cd 01-ai-campaign-health-check-agent
python -m pip install -r requirements.txt
```

## Run the Workflow

Run the scripts in this order:

```bash
python src/calculate_kpis.py
python src/rule_engine.py
python src/generate_visuals.py
```

## Generated Outputs

```text
outputs/campaign_kpis.csv
outputs/campaign_recommendations.csv
outputs/sample-campaign-health-report.md
outputs/visuals/spend_by_platform.png
outputs/visuals/leads_by_platform.png
outputs/visuals/recommendations_by_issue.png
outputs/visuals/cpl_by_campaign.png
```

## Commit Outputs

From the main repository folder:

```bash
git add 01-ai-campaign-health-check-agent/outputs/
git commit -m "Add campaign health outputs"
git push origin main
```

## Notes

This module uses sample data for demonstration. Live ad platform integrations are planned as future enhancements.
