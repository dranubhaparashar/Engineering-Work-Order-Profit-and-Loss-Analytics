# Data Dictionary

All bundled records are synthetic. Field names define the project’s logical analytical model and are not presented as the schema of any particular company or source system.

## Relationships

`work_order_number` is the main join key across all fact tables and `dim_work_order.csv`.

A work order can have:

- Multiple sales orders
- Multiple work-unit lines
- Multiple activity/labor reports
- Multiple invoices
- Multiple non-labor cost records

## `data/dim_work_order.csv`

**Grain:** one row per work order.

| Field | Type | Description |
|---|---|---|
| `work_order_number` | string | Synthetic primary key, for example `EWO-202500000` |
| `customer` | string | Synthetic customer grouping |
| `account` | string | Operating account or organizational portfolio |
| `budgeted_program` | string | Program or funding grouping |
| `job_category` | string | Type of engineering work |
| `bid_region` | string | Synthetic operating region |
| `intake_date` | date | Date the work order entered the lifecycle |
| `planned_close_date` | date | Planned completion date |
| `actual_close_date` | date/null | Actual close date for completed work orders |
| `status` | string | Closed, In Progress, Billing Pending, or On Hold |
| `target_margin_pct` | decimal | Desired work-order margin percentage |
| `medium_risk_threshold_pct` | decimal | Margin below which medium risk may apply |
| `high_risk_threshold_pct` | decimal | Margin below which high risk may apply |

## `data/fact_work_unit_revenue.csv`

**Grain:** one row per sales-order work-unit line.

| Field | Type | Description |
|---|---|---|
| `work_order_number` | string | Foreign key to the work order |
| `sales_order_number` | string | Synthetic sales-order identifier |
| `sales_order_line` | string | Unique synthetic sales-order line identifier |
| `work_unit_name` | string | Generic unit code |
| `work_unit_description` | string | Human-readable unit description |
| `unit_type` | string | Billing unit such as Each, Foot, or Structure |
| `work_unit_qty` | decimal | Quantity of the work unit |
| `item_rate` | decimal | Rate per unit in USD |
| `total_rate` | decimal | Stored line total; expected to equal quantity multiplied by rate |

## `data/fact_activity_labor.csv`

**Grain:** one row per activity, labor, or lifecycle event.

| Field | Type | Description |
|---|---|---|
| `work_order_number` | string | Foreign key to the work order |
| `activity_report_id` | string | Unique synthetic activity-report identifier |
| `technician` | string | Synthetic person or role label |
| `delivery_organization` | string | Delivery organization used for labor-rate mapping |
| `activity_date` | date | Date the activity occurred |
| `milestone` | string | High-level lifecycle stage |
| `activity_type` | string | Detailed activity category |
| `labor_hours` | decimal | Labor hours; zero is allowed for lifecycle-only events |
| `activity_description` | string | Synthetic description of the activity |

### Zero-hour events

Zero-hour records are intentional for events such as revenue reconciliation. They are excluded from labor cost because the hour value is zero, but retained in the lifecycle history.

## `data/fact_billing.csv`

**Grain:** one row per invoice, draft, or progress-billing event.

| Field | Type | Description |
|---|---|---|
| `invoice_id` | string | Unique synthetic billing identifier |
| `work_order_number` | string | Foreign key to the work order |
| `invoice_date` | date | Billing event date |
| `billing_status` | string | Paid, Issued, Draft, or Progress Billing |
| `billed_amount` | decimal | Amount associated with the billing event |

## `data/fact_other_cost.csv`

**Grain:** one row per non-labor expense.

| Field | Type | Description |
|---|---|---|
| `cost_id` | string | Unique synthetic cost identifier |
| `work_order_number` | string | Foreign key to the work order |
| `cost_date` | date | Date of the expense |
| `cost_type` | string | Mileage/Travel, Permit Fee, or Subcontractor |
| `amount` | decimal | Expense amount in USD |
| `description` | string | Synthetic expense description |

## `data/dim_labor_rate.csv`

**Grain:** one row per delivery organization and effective rate.

| Field | Type | Description |
|---|---|---|
| `delivery_organization` | string | Delivery organization matching activity records |
| `effective_date` | date | Rate effective date |
| `hourly_rate` | decimal | Synthetic burdened hourly rate |
| `currency` | string | Currency code; USD in the sample |
| `rate_type` | string | Description of the rate |

The current Python prototype maps one rate per organization. A production implementation should apply effective-date range logic when rates change over time.

## `data/dim_milestone.csv`

**Grain:** one row per standardized milestone and detailed activity.

| Field | Type | Description |
|---|---|---|
| `milestone_order` | integer | Display and lifecycle sequence |
| `milestone` | string | High-level lifecycle stage |
| `activity_type` | string | Detailed activity classification |

## Derived work-order summary fields

These fields are calculated by `src/metrics.py` and are not stored in the raw CSV files.

| Field | Definition |
|---|---|
| `estimated_revenue` | Sum of quantity multiplied by item rate |
| `total_hours` | Sum of all activity hours |
| `delivery_center_hours` | Hours recorded by the Global Delivery Center |
| `field_operations_hours` | Hours recorded by Field Operations |
| `travel_hours` | Hours whose detailed activity contains “travel” |
| `rework_hours` | Hours whose detailed activity contains “rework” or “correction” |
| `labor_cost` | Hours multiplied by mapped hourly rates |
| `billed_revenue` | Sum of billing events |
| `other_cost` | Sum of non-labor expenses |
| `actual_cost` | Labor cost plus other cost |
| `forecast_revenue` | Greater of estimated and billed revenue |
| `forecast_margin` | Forecast revenue minus actual cost |
| `forecast_margin_pct` | Forecast margin divided by forecast revenue |
| `revenue_per_hour` | Forecast revenue divided by total hours |
| `duration_days` | Days between first and last activity |
| `margin_variance_pct` | Forecast margin percentage minus target margin percentage |
| `risk_band` | High, Medium, or Low based on configured rules |
| `risk_reason` | Human-readable explanation of triggered rules |
