# Visual Assets Guide

This guide explains how to make the GitHub repository visually attractive using images, GIFs, screenshots, diagrams, and badges.

## Why Visuals Matter

Recruiters and hiring managers may not read every file. A strong README should quickly show:

- What the project does
- What tools are used
- What the workflow looks like
- What the output/dashboard looks like
- Why the project is commercially useful

## Recommended Assets Folder

Use this folder:

```text
assets/
```

Recommended file names:

```text
assets/dashboard-preview.svg
assets/workflow-demo.gif
assets/looker-dashboard-screenshot.png
assets/gtm-debug-screenshot.png
assets/ga4-debugview-screenshot.png
assets/campaign-health-report-screenshot.png
assets/architecture-diagram.png
```

## What to Upload

### 1. Dashboard screenshot

Use a screenshot of Looker Studio, Streamlit, Power BI, or a mock dashboard.

Recommended name:

```text
assets/looker-dashboard-screenshot.png
```

### 2. Workflow GIF

A GIF can show the flow of:

```text
CSV upload → KPI calculation → issue detection → recommendation output
```

Recommended name:

```text
assets/workflow-demo.gif
```

How to create a GIF:

- Use ScreenToGif on Windows, or any screen recorder that exports GIF.
- Keep the GIF short, ideally 5–15 seconds.
- Avoid recording private data.
- Keep file size below 10 MB when possible.

### 3. GTM/GA4 screenshots

Upload screenshots only from demo/test properties.

Do not show:

- Client names
- Account IDs
- Email addresses
- Tokens
- Private business data

### 4. Architecture diagram

You can create this using:

- Miro
- Lucidchart
- Excalidraw
- Canva
- Mermaid diagram inside Markdown

## How to Add an Image in README

Use Markdown:

```markdown
![Dashboard Preview](assets/dashboard-preview.svg)
```

For GIF:

```markdown
![Workflow Demo](assets/workflow-demo.gif)
```

For clickable image:

```markdown
[![Dashboard Preview](assets/dashboard-preview.svg)](01-ai-campaign-health-check-agent/README.md)
```

## Manual Upload Steps on GitHub

1. Open your GitHub repository.
2. Click **Add file**.
3. Click **Upload files**.
4. Drag and drop the image or GIF into the `assets/` folder.
5. Add a commit message like:

```text
Add dashboard screenshot
```

6. Click **Commit changes**.

## Safety Checklist Before Uploading Visuals

- No client data visible
- No access tokens visible
- No account IDs visible
- No private emails visible
- No payment or billing information visible
- No confidential campaign names unless they are fake/demo

## Recommended Visual Order in README

1. Hero image or dashboard preview
2. Workflow diagram
3. Project modules table
4. Sample output table
5. Screenshots/GIFs
6. Roadmap
7. Skills demonstrated

## Current Assets

- `assets/dashboard-preview.svg` — portfolio-style dashboard preview image

More screenshots and GIFs can be added as the project becomes functional.
