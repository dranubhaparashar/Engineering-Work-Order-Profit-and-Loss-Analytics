from __future__ import annotations

from pathlib import Path
import pandas as pd

DATE_COLUMNS = {
    "dim_work_order.csv": ["intake_date", "planned_close_date", "actual_close_date"],
    "fact_dwr_labor.csv": ["job_stop_date"],
    "fact_billing.csv": ["invoice_date"],
    "dim_labor_rate.csv": ["effective_date"],
}


def load_data(data_dir: str | Path) -> dict[str, pd.DataFrame]:
    data_dir = Path(data_dir)
    files = [
        "dim_work_order.csv",
        "fact_work_unit_revenue.csv",
        "fact_dwr_labor.csv",
        "fact_billing.csv",
        "fact_other_cost.csv",
        "dim_labor_rate.csv",
        "dim_milestone.csv",
    ]
    frames: dict[str, pd.DataFrame] = {}
    for name in files:
        path = data_dir / name
        if not path.exists():
            raise FileNotFoundError(f"Missing required data file: {path}")
        frames[name] = pd.read_csv(path, parse_dates=DATE_COLUMNS.get(name))
    return frames
