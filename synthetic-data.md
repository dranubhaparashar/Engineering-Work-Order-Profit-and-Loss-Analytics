# Developer Guide

## Application flow

1. `app.py` calls `load_data`.
2. `src/data_loader.py` reads required CSVs and parses dates.
3. `build_work_order_summary` aggregates revenue, labor, billing, and other costs.
4. The dashboard filters the summary and renders charts and tables.
5. `recalculate_with_rates` performs non-destructive scenario analysis.

## Add a new source field

1. Add the field to the relevant synthetic generator output.
2. Regenerate `data/`.
3. Update `DATA_DICTIONARY.md`.
4. Update `sql/snowflake_schema.sql` if the field belongs in the warehouse model.
5. Add calculations or display logic.
6. Add or update tests.

## Add a new metric

Implement reusable calculations in `src/metrics.py`, not directly in chart code. Add a test that checks the calculation’s grain, null handling, and expected direction.

## Add a dashboard page

Create a new Streamlit tab in `app.py`. Reuse the existing filtered work-order summary whenever possible. For event-level analysis, filter the relevant fact table using the selected work-order set.

## Coding conventions

- Use type hints.
- Keep source data immutable inside calculations by calling `.copy()`.
- Avoid hard-coded customer or organization identifiers.
- Handle missing numeric values explicitly.
- Preserve one row per work order in the summary.
- Keep confidential configuration outside version control.

## Test locally

```bash
pytest -q
python -m compileall app.py src scripts tests
```

## Dependency updates

The project intentionally uses version ranges in `requirements.txt`. Test the full application and CI before widening major-version ranges.
