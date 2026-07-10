# A–Z File Guide

This guide lists every intentional file in the repository, sorted alphabetically by path. Generated caches and local virtual environments are excluded.

| File | Purpose | Editing guidance |
|---|---|---|
| [`.github/ISSUE_TEMPLATE/bug_report.md`](.github/ISSUE_TEMPLATE/bug_report.md) | Public-safe bug-report template. | Yes |
| [`.github/ISSUE_TEMPLATE/feature_request.md`](.github/ISSUE_TEMPLATE/feature_request.md) | Public-safe feature-request template. | Yes |
| [`.github/pull_request_template.md`](.github/pull_request_template.md) | Checklist automatically shown for new pull requests. | Yes |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions matrix that compiles code and runs tests. | Edit with tests/review |
| [`.gitignore`](.gitignore) | Files and local artifacts Git must not commit. | Yes |
| [`.streamlit/config.toml`](.streamlit/config.toml) | Streamlit theme and local server configuration. | Yes |
| [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example) | Non-secret template for private Snowflake configuration. | Copy; never add real secrets here |
| [`A-Z_FILE_GUIDE.md`](A-Z_FILE_GUIDE.md) | Alphabetical reference describing every repository file. | Yes |
| [`app.py`](app.py) | Main Streamlit dashboard and user-interface orchestration. | Edit with tests/review |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Complete system, component, data-flow, security, and deployment architecture. | Yes |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history and notable changes. | Yes |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | Expected standards for contributor behavior. | Yes |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Development and pull-request contribution process. | Yes |
| [`data/dim_labor_rate.csv`](data/dim_labor_rate.csv) | Synthetic dimension CSV used by the application and tests. | Regenerate rather than hand-edit |
| [`data/dim_milestone.csv`](data/dim_milestone.csv) | Synthetic dimension CSV used by the application and tests. | Regenerate rather than hand-edit |
| [`data/dim_work_order.csv`](data/dim_work_order.csv) | Synthetic dimension CSV used by the application and tests. | Regenerate rather than hand-edit |
| [`data/fact_activity_labor.csv`](data/fact_activity_labor.csv) | Synthetic fact CSV used by the application and tests. | Regenerate rather than hand-edit |
| [`data/fact_billing.csv`](data/fact_billing.csv) | Synthetic fact CSV used by the application and tests. | Regenerate rather than hand-edit |
| [`data/fact_other_cost.csv`](data/fact_other_cost.csv) | Synthetic fact CSV used by the application and tests. | Regenerate rather than hand-edit |
| [`data/fact_work_unit_revenue.csv`](data/fact_work_unit_revenue.csv) | Synthetic fact CSV used by the application and tests. | Regenerate rather than hand-edit |
| [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) | Field-level definitions, table grains, joins, and derived metrics. | Yes |
| [`docs/configuration.md`](docs/configuration.md) | Detailed configuration documentation for users, developers, or operators. | Yes |
| [`docs/data-model.md`](docs/data-model.md) | Detailed data model documentation for users, developers, or operators. | Yes |
| [`docs/deployment.md`](docs/deployment.md) | Detailed deployment documentation for users, developers, or operators. | Yes |
| [`docs/developer-guide.md`](docs/developer-guide.md) | Detailed developer guide documentation for users, developers, or operators. | Yes |
| [`docs/faq.md`](docs/faq.md) | Detailed faq documentation for users, developers, or operators. | Yes |
| [`docs/financial-calculations.md`](docs/financial-calculations.md) | Detailed financial calculations documentation for users, developers, or operators. | Yes |
| [`docs/installation.md`](docs/installation.md) | Detailed installation documentation for users, developers, or operators. | Yes |
| [`docs/security-privacy.md`](docs/security-privacy.md) | Detailed security privacy documentation for users, developers, or operators. | Yes |
| [`docs/snowflake-integration.md`](docs/snowflake-integration.md) | Detailed snowflake integration documentation for users, developers, or operators. | Yes |
| [`docs/synthetic-data.md`](docs/synthetic-data.md) | Detailed synthetic data documentation for users, developers, or operators. | Yes |
| [`docs/testing.md`](docs/testing.md) | Detailed testing documentation for users, developers, or operators. | Yes |
| [`docs/troubleshooting.md`](docs/troubleshooting.md) | Detailed troubleshooting documentation for users, developers, or operators. | Yes |
| [`docs/user-guide.md`](docs/user-guide.md) | Detailed user guide documentation for users, developers, or operators. | Yes |
| [`docs/wiki-publishing.md`](docs/wiki-publishing.md) | Detailed wiki publishing documentation for users, developers, or operators. | Yes |
| [`GITHUB_REPOSITORY_SETUP.md`](GITHUB_REPOSITORY_SETUP.md) | Repository name, description, topics, push commands, Wiki publishing, and public-release checklist. | Yes |
| [`LICENSE`](LICENSE) | MIT license for source code and documentation. | Change only intentionally |
| [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) | Visual directory tree and responsibility of each folder. | Yes |
| [`README.md`](README.md) | Primary GitHub landing page, setup guide, features, and project overview. | Yes |
| [`requirements.txt`](requirements.txt) | Python runtime and test dependencies. | Yes |
| [`ROADMAP.md`](ROADMAP.md) | Planned features and future production milestones. | Yes |
| [`scripts/generate_synthetic_data.py`](scripts/generate_synthetic_data.py) | Creates the reproducible synthetic dataset. | Yes |
| [`scripts/publish_wiki.ps1`](scripts/publish_wiki.ps1) | Publishes `wiki/` pages to GitHub Wiki from PowerShell. | Yes |
| [`scripts/publish_wiki.sh`](scripts/publish_wiki.sh) | Publishes `wiki/` pages to GitHub Wiki from Bash. | Yes |
| [`SECURITY.md`](SECURITY.md) | Security reporting and data-exposure response policy. | Yes |
| [`setup_and_run.bat`](setup_and_run.bat) | Windows Command Prompt one-click setup and launch script. | Yes |
| [`setup_and_run.ps1`](setup_and_run.ps1) | Windows PowerShell one-click setup and launch script. | Yes |
| [`setup_and_run.sh`](setup_and_run.sh) | macOS/Linux one-click setup and launch script. | Yes |
| [`sql/profit_loss_views.sql`](sql/profit_loss_views.sql) | Creates Snowflake revenue, labor, and profit-and-loss analytical views. | Edit with tests/review |
| [`sql/quality_checks.sql`](sql/quality_checks.sql) | Runs warehouse-level duplicate, orphan, rate, arithmetic, and validity checks. | Edit with tests/review |
| [`sql/snowflake_schema.sql`](sql/snowflake_schema.sql) | Creates the Snowflake logical tables. | Edit with tests/review |
| [`src/__init__.py`](src/__init__.py) | Marks `src` as a Python package. | Edit with tests/review |
| [`src/data_loader.py`](src/data_loader.py) | Loads required CSV files and parses date columns. | Edit with tests/review |
| [`src/metrics.py`](src/metrics.py) | Calculates work-order revenue, cost, margin, lifecycle, scenario, and risk metrics. | Edit with tests/review |
| [`tests/test_data_quality.py`](tests/test_data_quality.py) | Tests relationships, non-negative values, work-unit arithmetic, and public-data safety. | Yes |
| [`tests/test_metrics.py`](tests/test_metrics.py) | Tests work-order summary grain and labor-rate scenario behavior. | Yes |
| [`wiki/_Footer.md`](wiki/_Footer.md) | Disclaimer footer displayed on GitHub Wiki pages. | Yes |
| [`wiki/_Sidebar.md`](wiki/_Sidebar.md) | Navigation menu displayed on every GitHub Wiki page. | Yes |
| [`wiki/Architecture.md`](wiki/Architecture.md) | GitHub Wiki page covering architecture. | Yes |
| [`wiki/Dashboard-Guide.md`](wiki/Dashboard-Guide.md) | GitHub Wiki page covering dashboard guide. | Yes |
| [`wiki/Data-Model.md`](wiki/Data-Model.md) | GitHub Wiki page covering data model. | Yes |
| [`wiki/Deployment.md`](wiki/Deployment.md) | GitHub Wiki page covering deployment. | Yes |
| [`wiki/FAQ.md`](wiki/FAQ.md) | GitHub Wiki page covering faq. | Yes |
| [`wiki/Financial-Calculations.md`](wiki/Financial-Calculations.md) | GitHub Wiki page covering financial calculations. | Yes |
| [`wiki/Getting-Started.md`](wiki/Getting-Started.md) | GitHub Wiki page covering getting started. | Yes |
| [`wiki/Home.md`](wiki/Home.md) | GitHub Wiki page covering home. | Yes |
| [`wiki/Roadmap.md`](wiki/Roadmap.md) | GitHub Wiki page covering roadmap. | Yes |
| [`wiki/Security-and-Privacy.md`](wiki/Security-and-Privacy.md) | GitHub Wiki page covering security and privacy. | Yes |
| [`wiki/Snowflake-Integration.md`](wiki/Snowflake-Integration.md) | GitHub Wiki page covering snowflake integration. | Yes |
| [`wiki/Synthetic-Data.md`](wiki/Synthetic-Data.md) | GitHub Wiki page covering synthetic data. | Yes |
| [`wiki/Testing-and-Quality.md`](wiki/Testing-and-Quality.md) | GitHub Wiki page covering testing and quality. | Yes |
| [`wiki/Troubleshooting.md`](wiki/Troubleshooting.md) | GitHub Wiki page covering troubleshooting. | Yes |

## Files that should never be committed

- `.venv/` and other local environments
- `.streamlit/secrets.toml`
- `.env` files containing credentials
- Python caches and test caches
- Real company, customer, employee, billing, rate-card, or production data
- Internal screenshots, system names, or connection details

## Where to start

1. Read `README.md` to run the application.
2. Read `ARCHITECTURE.md` to understand the design.
3. Read `DATA_DICTIONARY.md` before changing schemas.
4. Read `GITHUB_REPOSITORY_SETUP.md` before publishing.
5. Read `CONTRIBUTING.md` before modifying code.
6. Use the `wiki/` folder when publishing the GitHub Wiki.
