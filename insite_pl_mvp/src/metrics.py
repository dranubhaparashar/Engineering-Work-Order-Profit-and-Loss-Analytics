from __future__ import annotations

import numpy as np
import pandas as pd


def build_work_order_summary(
    work_orders: pd.DataFrame,
    work_units: pd.DataFrame,
    dwr: pd.DataFrame,
    billing: pd.DataFrame,
    other_costs: pd.DataFrame,
    labor_rates: pd.DataFrame,
) -> pd.DataFrame:
    """Create one financial/lifecycle row per work order."""
    wo = work_orders.copy()

    revenue = (
        work_units.assign(estimated_revenue=lambda x: x["work_unit_qty"] * x["item_rate"])
        .groupby("work_order_number", as_index=False)["estimated_revenue"]
        .sum()
    )

    rate_lookup = labor_rates.set_index("tech_subsidiary")["hourly_rate"].to_dict()
    labor = dwr.copy()
    labor["hourly_rate"] = labor["tech_subsidiary"].map(rate_lookup).fillna(0.0)
    labor["labor_cost"] = labor["on_site_hours"] * labor["hourly_rate"]
    labor["is_travel"] = labor["dummy_unit"].str.contains("travel", case=False, na=False)
    labor["is_rework"] = labor["dummy_unit"].str.contains("rework|correction", case=False, regex=True, na=False)
    labor["is_zero_hour_event"] = labor["on_site_hours"].eq(0)

    labor_agg = labor.groupby("work_order_number", as_index=False).agg(
        total_hours=("on_site_hours", "sum"),
        labor_cost=("labor_cost", "sum"),
        psg_hours=("on_site_hours", lambda s: s[labor.loc[s.index, "tech_subsidiary"].eq("Pearce Services Global")].sum()),
        us_hours=("on_site_hours", lambda s: s[labor.loc[s.index, "tech_subsidiary"].eq("Pearce Services")].sum()),
        travel_hours=("on_site_hours", lambda s: s[labor.loc[s.index, "is_travel"]].sum()),
        rework_hours=("on_site_hours", lambda s: s[labor.loc[s.index, "is_rework"]].sum()),
        zero_hour_events=("is_zero_hour_event", "sum"),
        first_activity_date=("job_stop_date", "min"),
        last_activity_date=("job_stop_date", "max"),
    )

    billed = billing.groupby("work_order_number", as_index=False).agg(
        billed_revenue=("billed_amount", "sum"),
        latest_invoice_date=("invoice_date", "max"),
    )

    other = other_costs.groupby("work_order_number", as_index=False).agg(
        other_cost=("amount", "sum")
    )

    out = (
        wo.merge(revenue, on="work_order_number", how="left")
        .merge(labor_agg, on="work_order_number", how="left")
        .merge(billed, on="work_order_number", how="left")
        .merge(other, on="work_order_number", how="left")
    )

    numeric_cols = [
        "estimated_revenue", "total_hours", "labor_cost", "psg_hours", "us_hours",
        "travel_hours", "rework_hours", "zero_hour_events", "billed_revenue", "other_cost"
    ]
    for col in numeric_cols:
        out[col] = out[col].fillna(0.0)

    out["actual_cost"] = out["labor_cost"] + out["other_cost"]
    out["recognized_revenue"] = np.where(
        out["status"].eq("Closed"),
        np.maximum(out["billed_revenue"], out["estimated_revenue"]),
        out["billed_revenue"],
    )
    out["forecast_revenue"] = np.maximum(out["estimated_revenue"], out["billed_revenue"])
    out["forecast_margin"] = out["forecast_revenue"] - out["actual_cost"]
    out["forecast_margin_pct"] = np.where(
        out["forecast_revenue"] > 0,
        out["forecast_margin"] / out["forecast_revenue"],
        np.nan,
    )
    out["revenue_per_hour"] = np.where(
        out["total_hours"] > 0,
        out["forecast_revenue"] / out["total_hours"],
        np.nan,
    )
    out["duration_days"] = (
        pd.to_datetime(out["last_activity_date"]) - pd.to_datetime(out["first_activity_date"])
    ).dt.days.fillna(0).clip(lower=0)
    out["margin_variance_pct"] = out["forecast_margin_pct"] - out["target_margin_pct"]

    conditions = [
        (out["forecast_margin_pct"] < out["high_risk_threshold_pct"]) |
        (out["rework_hours"] >= 6) |
        (out["travel_hours"] >= 8),
        (out["forecast_margin_pct"] < out["medium_risk_threshold_pct"]) |
        (out["rework_hours"] >= 3) |
        (out["travel_hours"] >= 5),
    ]
    out["risk_band"] = np.select(conditions, ["High", "Medium"], default="Low")

    out["risk_reason"] = out.apply(_risk_reason, axis=1)
    return out.sort_values(["risk_band", "forecast_margin_pct"], ascending=[True, True])


def _risk_reason(row: pd.Series) -> str:
    reasons: list[str] = []
    if row["forecast_margin_pct"] < row["high_risk_threshold_pct"]:
        reasons.append("margin below high-risk threshold")
    elif row["forecast_margin_pct"] < row["medium_risk_threshold_pct"]:
        reasons.append("margin below medium-risk threshold")
    if row["rework_hours"] >= 6:
        reasons.append("heavy rework")
    elif row["rework_hours"] >= 3:
        reasons.append("elevated rework")
    if row["travel_hours"] >= 8:
        reasons.append("heavy travel")
    elif row["travel_hours"] >= 5:
        reasons.append("elevated travel")
    return "; ".join(reasons) if reasons else "within configured thresholds"


def recalculate_with_rates(
    summary: pd.DataFrame,
    psg_rate: float,
    us_rate: float,
    margin_threshold: float,
) -> pd.DataFrame:
    """Scenario calculation without mutating source data."""
    out = summary.copy()
    out["scenario_labor_cost"] = out["psg_hours"] * psg_rate + out["us_hours"] * us_rate
    out["scenario_actual_cost"] = out["scenario_labor_cost"] + out["other_cost"]
    out["scenario_margin"] = out["forecast_revenue"] - out["scenario_actual_cost"]
    out["scenario_margin_pct"] = np.where(
        out["forecast_revenue"] > 0,
        out["scenario_margin"] / out["forecast_revenue"],
        np.nan,
    )
    out["scenario_at_risk"] = out["scenario_margin_pct"] < margin_threshold
    return out
