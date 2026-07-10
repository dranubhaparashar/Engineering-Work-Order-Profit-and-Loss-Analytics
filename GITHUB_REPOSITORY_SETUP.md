# GitHub Repository Setup

## Repository details

**Repository name**

```text
engineering-workorder-profit-loss-analytics
```

**Project title**

```text
Engineering Work Order Profit and Loss Analytics
```

**GitHub description**

```text
A synthetic-data analytics platform for estimating work-order revenue, tracking labor and operational costs, monitoring billing, calculating profit and loss, and identifying margin risk across the engineering lifecycle.
```

**Suggested topics**

```text
python
streamlit
plotly
snowflake
synthetic-data
financial-analytics
profit-and-loss
work-order-management
data-analytics
risk-monitoring
```

## Create the repository

1. Create a new empty GitHub repository using the repository name above.
2. Choose **Public** only after reviewing every file and confirming that the Git history contains no confidential data.
3. Do not initialize it with a separate README, license, or `.gitignore`, because this project already contains them.

## Push the project

From the project directory:

```bash
git init
git add .
git commit -m "Initial public synthetic analytics project"
git branch -M main
git remote add origin https://github.com/USERNAME/engineering-workorder-profit-loss-analytics.git
git push -u origin main
```

Replace `USERNAME` with the correct GitHub account or organization.

## Enable GitHub Wiki

1. Open the repository **Settings** page.
2. Under **Features**, enable **Wikis**.
3. Create an initial Wiki page in the browser if GitHub requires it.
4. Publish the included pages:

```powershell
.\scripts\publish_wiki.ps1 -RepositoryUrl "https://github.com/USERNAME/engineering-workorder-profit-loss-analytics.git"
```

Or on macOS/Linux:

```bash
./scripts/publish_wiki.sh https://github.com/USERNAME/engineering-workorder-profit-loss-analytics.git
```

## Recommended repository settings

- Require pull requests before merging to `main`.
- Require the Python CI workflow to pass.
- Enable secret scanning and push protection where available.
- Disable direct pushes to `main` for collaborative repositories.
- Add a repository social preview image only if it contains no company material.
- Review Dependabot and security-alert settings.

## Final public-release check

- Synthetic data only
- No credentials
- No internal screenshots
- No company/customer/employee names
- No proprietary field mappings or rate cards
- Tests pass
- README links work
- Wiki pages reviewed
- License and security policy present
