# Testing and Quality

## Automated tests

Run:

```bash
pytest -q
```

The current tests verify:

- Exactly one summary row is produced per work order.
- Work-order identifiers remain unique in the summary.
- Revenue and costs are non-negative.
- Risk bands stay within the expected values.
- Higher labor-rate scenarios increase total scenario cost.

## Syntax validation

```bash
python -m compileall app.py src scripts tests
```

## Data-quality checks in the application

The Data Quality page reports:

- Potential duplicate work-unit lines
- Activity records with missing parent work orders
- Zero-hour lifecycle events
- Negative-hour records
- Work orders without work-unit revenue

## SQL validation

Run `sql/quality_checks.sql` in Snowflake after loading or mapping data.

## Recommended additional tests

- Effective-date labor-rate selection
- Duplicate invoice handling
- Billing-status-specific revenue logic
- Zero-revenue work orders
- Missing-rate behavior
- Currency conversion
- Extremely large values and outliers
- Time-zone and date-boundary behavior
- Row-level access rules
