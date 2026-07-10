# User Guide

## Start the application

Run `streamlit run app.py` and open the local URL displayed in the terminal.

## Sidebar filters

Use the sidebar to filter by account, program, job category, region, status, risk band, and intake-date range. Filters apply across all dashboard pages.

## Portfolio Overview

Use this page to answer:

- How many work orders are in the selected portfolio?
- What are forecast revenue, billed revenue, actual cost, and forecast margin?
- How many high-risk work orders exist?
- Which regions or programs have weak margins?

The table can be downloaded as CSV.

## Work Order Detail

Select a work order to view:

- Forecast revenue
- Actual cost
- Forecast margin percentage
- Total labor hours
- Risk band and reason
- Work-unit and sales-order lines
- Billing history
- Other cost history
- Activity timeline and scope notes

## Lifecycle & Labor

This page groups activity hours by milestone and delivery organization. Use it to locate stages with high effort and detailed activities that consume the most hours.

## Rate Scenario

Enter alternative burdened rates for the Global Delivery Center and Field Operations. Set an at-risk margin threshold. The page recalculates scenario costs and margins without changing the underlying data.

## Data Quality

Review the quality indicators before interpreting financial outputs:

- Potential duplicate work-unit rows
- Orphan activity records
- Zero-hour lifecycle events
- Negative-hour records
- Work orders without work units

Potential duplicates are not removed automatically because two lines can be legitimate when they have distinct sales-order-line identifiers.

## Interpretation caution

This application is an analytical demonstration. Confirm revenue-recognition rules, labor-rate definitions, overhead, taxes, currency, billing status, and cost allocation with authorized finance stakeholders before using a similar model operationally.
