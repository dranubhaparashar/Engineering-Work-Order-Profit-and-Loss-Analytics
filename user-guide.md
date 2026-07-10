# Configuration

## Data directory

The application reads CSV files from the repository’s `data/` directory:

```python
DATA_DIR = Path(__file__).parent / "data"
```

To use another directory, update `DATA_DIR` or introduce an environment variable before deployment.

## Required files

All seven files listed in `src/data_loader.py` are required. Missing files raise a clear `FileNotFoundError`.

## Labor rates

Default rates are stored in `data/dim_labor_rate.csv`. They are synthetic and can be changed through the dashboard’s Rate Scenario page without modifying the source files.

A production implementation should:

- Store rate history with effective start and end dates.
- Define whether rates are base, loaded, burdened, or fully allocated.
- Control who may view or modify rates.

## Risk thresholds

Each work order stores:

- `target_margin_pct`
- `medium_risk_threshold_pct`
- `high_risk_threshold_pct`

The current rules also use fixed travel and rework triggers in `src/metrics.py`.

## Streamlit theme

`.streamlit/config.toml` controls basic appearance and server settings. Do not place passwords or tokens there.

## Secrets

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` only for local private configuration. The real secrets file is ignored by Git.

Never commit:

- Passwords
- Private keys
- OAuth secrets
- Warehouse credentials
- Customer identifiers
- Production connection strings
