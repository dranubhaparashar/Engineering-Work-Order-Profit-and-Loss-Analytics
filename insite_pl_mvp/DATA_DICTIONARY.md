# Synthetic Data Dictionary

## `dim_work_order.csv`

- `work_order_number`: Synthetic WO identifier and primary join key
- `customer`: Synthetic customer grouping
- `account`: Operating account
- `budgeted_program`: Budget/program grouping
- `job_category`: Aerial, buried, mixed-plant, or permit-only work
- `bid_region`: Synthetic state/region code
- `intake_date`, `planned_close_date`, `actual_close_date`: Lifecycle dates
- `status`: Closed, In Progress, Billing Pending, On Hold
- `target_margin_pct`: Target margin for the WO
- `medium_risk_threshold_pct`, `high_risk_threshold_pct`: Risk configuration

## `fact_work_unit_revenue.csv`

One row per Sales Order work-unit line. `total_rate = work_unit_qty × item_rate`.

## `fact_dwr_labor.csv`

One row per synthetic DWR event. Includes milestone, dummy unit, subsidiary, hours, and scope text. Zero-hour revenue-true-up events are intentional and should be retained as lifecycle events.

## `fact_billing.csv`

One row per invoice, draft, or progress-billing event.

## `fact_other_cost.csv`

Synthetic mileage/travel, permit, and subcontractor costs.

## `dim_labor_rate.csv`

Configurable synthetic burdened rates for PSG and US Fielding.

## `dim_milestone.csv`

Standardized milestone and dummy-unit mapping for lifecycle sequencing.
