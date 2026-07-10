# Troubleshooting

## `py` is not recognized

Install Python from the official Python distribution or use `python`/`python3` instead of `py`.

## PowerShell blocks script execution

Run for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then run `setup_and_run.ps1` again.

## `streamlit` is not recognized

Activate the virtual environment and reinstall dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```

On macOS/Linux:

```bash
source .venv/bin/activate
python -m streamlit run app.py
```

## Missing required data file

Regenerate the data:

```bash
python scripts/generate_synthetic_data.py --output data --work-orders 600
```

## Empty dashboard after filtering

Clear one or more sidebar filters or expand the intake-date range.

## Port 8501 is already in use

```bash
streamlit run app.py --server.port 8502
```

## Tests cannot import `src`

Run tests from the repository root, not from inside `tests/`.

## Charts are slow

Reduce the generated work-order count or push aggregations to a database.

## Incorrect rates or margins

Confirm the values in `data/dim_labor_rate.csv`, the delivery-organization labels in activity data, and the assumptions documented in `docs/financial-calculations.md`.
