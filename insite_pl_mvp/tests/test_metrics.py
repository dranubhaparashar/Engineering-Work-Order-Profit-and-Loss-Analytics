from pathlib import Path
import pandas as pd

from src.data_loader import load_data
from src.metrics import build_work_order_summary, recalculate_with_rates


def test_summary_has_one_row_per_work_order():
    root = Path(__file__).parents[1]
    frames = load_data(root / "data")
    summary = build_work_order_summary(
        frames["dim_work_order.csv"], frames["fact_work_unit_revenue.csv"],
        frames["fact_dwr_labor.csv"], frames["fact_billing.csv"],
        frames["fact_other_cost.csv"], frames["dim_labor_rate.csv"]
    )
    assert len(summary) == frames["dim_work_order.csv"]["work_order_number"].nunique()
    assert summary["work_order_number"].is_unique
    assert (summary["forecast_revenue"] >= 0).all()
    assert (summary["actual_cost"] >= 0).all()
    assert set(summary["risk_band"].unique()).issubset({"Low", "Medium", "High"})


def test_scenario_rate_change_changes_cost():
    root = Path(__file__).parents[1]
    frames = load_data(root / "data")
    summary = build_work_order_summary(
        frames["dim_work_order.csv"], frames["fact_work_unit_revenue.csv"],
        frames["fact_dwr_labor.csv"], frames["fact_billing.csv"],
        frames["fact_other_cost.csv"], frames["dim_labor_rate.csv"]
    )
    base = recalculate_with_rates(summary, 18.5, 52.0, 0.22)
    high = recalculate_with_rates(summary, 25.0, 70.0, 0.22)
    assert high["scenario_actual_cost"].sum() > base["scenario_actual_cost"].sum()
