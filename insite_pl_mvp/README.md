# Engineering Work Order P&L — Synthetic MVP

A complete local prototype for estimating revenue and monitoring expenses/margin through an Engineering Work Order lifecycle.

## What is included

- 600 synthetic work orders
- Work Order dimensions: account, program, category, region, dates, status, margin targets
- Sales Orders and work-unit revenue
- DWR labor events with PSG/US classification, milestones, dummy units, travel, rework, and zero-hour lifecycle events
- Billing/invoice events
- Labor rates and other costs
- Streamlit dashboard with portfolio, work-order detail, lifecycle, rate-scenario, and data-quality views
- Snowflake DDL and analytical views
- Automated tests

All records are synthetic. Names and identifiers do not represent production employees, customers, invoices, or work orders.

## Run on Windows PowerShell

```powershell
cd path\to\insite_pl_mvp
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`.

## Regenerate synthetic data

```powershell
python scripts\generate_synthetic_data.py --output data --work-orders 600
```

Use a different number after `--work-orders` to generate a smaller or larger dataset.

## Run tests

```powershell
pytest -q
```

## Data model

| File | Grain |
|---|---|
| `dim_work_order.csv` | One row per Work Order |
| `fact_work_unit_revenue.csv` | One row per Sales Order work-unit line |
| `fact_dwr_labor.csv` | One row per DWR labor/lifecycle event |
| `fact_billing.csv` | One row per invoice/progress-billing event |
| `fact_other_cost.csv` | One row per non-labor cost |
| `dim_labor_rate.csv` | One row per subsidiary/effective rate |
| `dim_milestone.csv` | Milestone and dummy-unit mapping |

## Main calculations

```text
Estimated Revenue = SUM(Work Unit Quantity × Item Rate)
Labor Cost = PSG Hours × PSG Rate + US Hours × US Rate
Actual Cost = Labor Cost + Other Cost
Forecast Revenue = MAX(Estimated Revenue, Billed Revenue)
Forecast Margin = Forecast Revenue - Actual Cost
Forecast Margin % = Forecast Margin / Forecast Revenue
```

## Replace synthetic CSVs with Snowflake data

1. Create the tables in `sql/snowflake_schema.sql`.
2. Map actual Insite/Snowflake columns to the same logical fields.
3. Create the views in `sql/mvp_views.sql`.
4. Replace `src/data_loader.py` with `snowflake.snowpark` reads or export the view results to the expected CSV names.

## Assumptions to validate with the business

- Whether work-unit totals are estimated, approved, earned, or final billed revenue
- PSG and US burdened labor rates
- Treatment of travel hours and mileage
- Inclusion of permit, subcontractor, and overhead expenses
- Margin targets by account/program/category/region
- Risk thresholds
- Final billing and revenue-recognition rules
- One-to-many relationship between Work Orders and Sales Orders
