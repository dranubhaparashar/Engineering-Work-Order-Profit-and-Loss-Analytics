# Project Structure

```text
engineering-workorder-profit-loss-analytics/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── workflows/ci.yml
│   └── pull_request_template.md
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── data/
│   ├── dim_labor_rate.csv
│   ├── dim_milestone.csv
│   ├── dim_work_order.csv
│   ├── fact_billing.csv
│   ├── fact_activity_labor.csv
│   ├── fact_other_cost.csv
│   └── fact_work_unit_revenue.csv
├── docs/
│   ├── configuration.md
│   ├── data-model.md
│   ├── deployment.md
│   ├── developer-guide.md
│   ├── faq.md
│   ├── financial-calculations.md
│   ├── installation.md
│   ├── security-privacy.md
│   ├── snowflake-integration.md
│   ├── synthetic-data.md
│   ├── testing.md
│   ├── troubleshooting.md
│   ├── user-guide.md
│   └── wiki-publishing.md
├── scripts/
│   ├── generate_synthetic_data.py
│   ├── publish_wiki.ps1
│   └── publish_wiki.sh
├── sql/
│   ├── profit_loss_views.sql
│   ├── quality_checks.sql
│   └── snowflake_schema.sql
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   └── metrics.py
├── tests/
│   ├── test_data_quality.py
│   └── test_metrics.py
├── wiki/
│   ├── Home.md
│   ├── Getting-Started.md
│   ├── Architecture.md
│   ├── Data-Model.md
│   ├── Dashboard-Guide.md
│   ├── Synthetic-Data.md
│   ├── Financial-Calculations.md
│   ├── Snowflake-Integration.md
│   ├── Deployment.md
│   ├── Testing-and-Quality.md
│   ├── Troubleshooting.md
│   ├── Security-and-Privacy.md
│   ├── FAQ.md
│   ├── Roadmap.md
│   ├── _Sidebar.md
│   └── _Footer.md
├── app.py
├── requirements.txt
├── setup_and_run.bat
├── setup_and_run.ps1
├── setup_and_run.sh
├── README.md
├── ARCHITECTURE.md
├── DATA_DICTIONARY.md
├── GITHUB_REPOSITORY_SETUP.md
├── A-Z_FILE_GUIDE.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── ROADMAP.md
└── SECURITY.md
```

## Directory responsibilities

| Directory | Purpose |
|---|---|
| `.github/` | Continuous integration, issue forms, and pull-request guidance |
| `.streamlit/` | Application theme and safe secrets template |
| `data/` | Public synthetic demonstration datasets |
| `docs/` | Repository documentation intended for contributors and operators |
| `scripts/` | Repeatable maintenance and publishing utilities |
| `sql/` | Snowflake-oriented schema, views, and validation SQL |
| `src/` | Reusable Python data and metric logic |
| `tests/` | Automated regression tests |
| `wiki/` | Markdown files ready for a GitHub Wiki repository |

## Extension points

- Add authentication before exposing real data.
- Replace CSV loading in `src/data_loader.py` with a governed warehouse adapter.
- Add effective-date labor-rate joins.
- Add predictive risk models under a new `models/` directory.
- Add Docker, Terraform, or cloud deployment assets under `deploy/` when a target platform is selected.
