# Financial Calculations

## Estimated revenue

For each work-unit line:

```text
Line Revenue = Work Unit Quantity × Item Rate
```

At work-order level:

```text
Estimated Revenue = Sum of all Line Revenue
```

## Labor cost

Each activity record is mapped to a rate by `delivery_organization`:

```text
Activity Labor Cost = On-Site Hours × Hourly Rate
Labor Cost = Sum of Activity Labor Cost
```

Zero-hour events therefore contribute no labor cost.

## Actual cost

```text
Actual Cost = Labor Cost + Other Cost
```

The synthetic model includes travel, permit, and occasional subcontractor expenses. It does not include every possible accounting cost.

## Billed revenue

```text
Billed Revenue = Sum of Billing Events
```

Billing status is not currently weighted; Draft, Issued, Paid, and Progress Billing records all contribute to the displayed total. A production model may separate these statuses.

## Forecast revenue

```text
Forecast Revenue = MAX(Estimated Revenue, Billed Revenue)
```

This is a demonstration assumption that avoids showing forecast revenue below billing already recorded. It must be validated for a real use case.

## Forecast margin

```text
Forecast Margin = Forecast Revenue − Actual Cost
Forecast Margin % = Forecast Margin ÷ Forecast Revenue
```

If forecast revenue is zero, margin percentage is undefined.

## Risk classification

High risk is triggered by any of:

- Forecast margin percentage below `high_risk_threshold_pct`
- Rework hours at least 6
- Travel hours at least 8

Medium risk is triggered by any of:

- Forecast margin percentage below `medium_risk_threshold_pct`
- Rework hours at least 3
- Travel hours at least 5

Low risk applies otherwise.

## Example

Suppose a work order has:

- Estimated revenue: $2,000
- Billed revenue: $1,500
- Delivery Center labor cost: $450
- Field Operations labor cost: $520
- Other cost: $130

Then:

```text
Forecast Revenue = MAX(2,000, 1,500) = 2,000
Actual Cost = 450 + 520 + 130 = 1,100
Forecast Margin = 2,000 − 1,100 = 900
Forecast Margin % = 900 ÷ 2,000 = 45%
```

## Accounting disclaimer

The formulas are analytical assumptions, not Generally Accepted Accounting Principles, International Financial Reporting Standards, or audited accounting guidance.
