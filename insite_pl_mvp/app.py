from __future__ import annotations

from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_data
from src.metrics import build_work_order_summary, recalculate_with_rates

st.set_page_config(page_title="Engineering WO P&L MVP", page_icon="📊", layout="wide")
DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def get_frames() -> dict[str, pd.DataFrame]:
    return load_data(DATA_DIR)


@st.cache_data
def get_summary(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return build_work_order_summary(
        frames["dim_work_order.csv"],
        frames["fact_work_unit_revenue.csv"],
        frames["fact_dwr_labor.csv"],
        frames["fact_billing.csv"],
        frames["fact_other_cost.csv"],
        frames["dim_labor_rate.csv"],
    )


frames = get_frames()
summary = get_summary(frames)

st.title("Engineering Work Order P&L — Synthetic MVP")
st.caption("Prototype using synthetic data patterned after WO, DWR, Sales Order, billing, work-unit, milestone, and labor-rate fields.")

with st.sidebar:
    st.header("Filters")
    accounts = st.multiselect("Account", sorted(summary["account"].unique()), default=[])
    programs = st.multiselect("Budgeted program", sorted(summary["budgeted_program"].unique()), default=[])
    categories = st.multiselect("Job category", sorted(summary["job_category"].unique()), default=[])
    regions = st.multiselect("Bid region", sorted(summary["bid_region"].unique()), default=[])
    statuses = st.multiselect("Status", sorted(summary["status"].unique()), default=[])
    risks = st.multiselect("Risk band", ["High", "Medium", "Low"], default=[])
    date_min = pd.to_datetime(summary["intake_date"]).min().date()
    date_max = pd.to_datetime(summary["intake_date"]).max().date()
    intake_range = st.date_input("Intake date", value=(date_min, date_max), min_value=date_min, max_value=date_max)

filtered = summary.copy()
for col, values in [
    ("account", accounts), ("budgeted_program", programs), ("job_category", categories),
    ("bid_region", regions), ("status", statuses), ("risk_band", risks)
]:
    if values:
        filtered = filtered[filtered[col].isin(values)]
if isinstance(intake_range, tuple) and len(intake_range) == 2:
    start, end = pd.Timestamp(intake_range[0]), pd.Timestamp(intake_range[1])
    filtered = filtered[pd.to_datetime(filtered["intake_date"]).between(start, end)]

portfolio_tab, wo_tab, lifecycle_tab, scenario_tab, quality_tab = st.tabs([
    "Portfolio Overview", "Work Order Detail", "Lifecycle & Labor", "Rate Scenario", "Data Quality"
])

with portfolio_tab:
    total_revenue = filtered["forecast_revenue"].sum()
    billed = filtered["billed_revenue"].sum()
    cost = filtered["actual_cost"].sum()
    margin = total_revenue - cost
    margin_pct = margin / total_revenue if total_revenue else 0
    high_risk = int(filtered["risk_band"].eq("High").sum())

    cols = st.columns(6)
    cols[0].metric("Work Orders", f"{len(filtered):,}")
    cols[1].metric("Forecast Revenue", f"${total_revenue:,.0f}")
    cols[2].metric("Billed Revenue", f"${billed:,.0f}")
    cols[3].metric("Actual Cost", f"${cost:,.0f}")
    cols[4].metric("Forecast Margin", f"{margin_pct:.1%}")
    cols[5].metric("High-Risk WOs", f"{high_risk:,}")

    c1, c2 = st.columns(2)
    with c1:
        risk_counts = filtered["risk_band"].value_counts().rename_axis("risk_band").reset_index(name="work_orders")
        fig = px.bar(risk_counts, x="risk_band", y="work_orders", title="Work Orders by Risk Band",
                     category_orders={"risk_band": ["High", "Medium", "Low"]})
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        region = filtered.groupby("bid_region", as_index=False).agg(
            forecast_revenue=("forecast_revenue", "sum"), actual_cost=("actual_cost", "sum")
        )
        region["margin"] = region["forecast_revenue"] - region["actual_cost"]
        fig = px.bar(region, x="bid_region", y=["forecast_revenue", "actual_cost", "margin"],
                     barmode="group", title="Revenue, Cost and Margin by Region")
        st.plotly_chart(fig, use_container_width=True)

    margin_by_program = filtered.groupby("budgeted_program", as_index=False).agg(
        forecast_revenue=("forecast_revenue", "sum"), actual_cost=("actual_cost", "sum")
    )
    margin_by_program["margin_pct"] = (margin_by_program["forecast_revenue"] - margin_by_program["actual_cost"]) / margin_by_program["forecast_revenue"]
    fig = px.bar(margin_by_program, x="budgeted_program", y="margin_pct", title="Forecast Margin % by Program")
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    display_cols = [
        "work_order_number", "account", "budgeted_program", "job_category", "bid_region", "status",
        "forecast_revenue", "billed_revenue", "actual_cost", "forecast_margin_pct",
        "psg_hours", "us_hours", "travel_hours", "rework_hours", "risk_band", "risk_reason"
    ]
    st.subheader("Work Order Financial Summary")
    st.dataframe(
        filtered[display_cols].sort_values(["risk_band", "forecast_margin_pct"]),
        use_container_width=True,
        hide_index=True,
        column_config={
            "forecast_revenue": st.column_config.NumberColumn(format="dollar"),
            "billed_revenue": st.column_config.NumberColumn(format="dollar"),
            "actual_cost": st.column_config.NumberColumn(format="dollar"),
            "forecast_margin_pct": st.column_config.NumberColumn(format="percent"),
        },
    )
    st.download_button(
        "Download filtered summary CSV",
        filtered[display_cols].to_csv(index=False).encode("utf-8"),
        file_name="filtered_work_order_summary.csv",
        mime="text/csv",
    )

with wo_tab:
    if filtered.empty:
        st.info("No work orders match the current filters.")
    else:
        selected_wo = st.selectbox("Select work order", filtered["work_order_number"].tolist())
        row = summary.loc[summary["work_order_number"].eq(selected_wo)].iloc[0]
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Forecast Revenue", f"${row['forecast_revenue']:,.2f}")
        k2.metric("Actual Cost", f"${row['actual_cost']:,.2f}")
        k3.metric("Forecast Margin", f"{row['forecast_margin_pct']:.1%}")
        k4.metric("Total Hours", f"{row['total_hours']:.2f}")
        k5.metric("Risk", row["risk_band"])
        st.write(f"**Reason:** {row['risk_reason']}")

        w_units = frames["fact_work_unit_revenue.csv"].query("work_order_number == @selected_wo").copy()
        dwr = frames["fact_dwr_labor.csv"].query("work_order_number == @selected_wo").copy()
        billing = frames["fact_billing.csv"].query("work_order_number == @selected_wo").copy()
        other = frames["fact_other_cost.csv"].query("work_order_number == @selected_wo").copy()

        a, b = st.columns(2)
        with a:
            st.subheader("Work Units / Sales Orders")
            st.dataframe(w_units, use_container_width=True, hide_index=True)
        with b:
            st.subheader("Billing")
            st.dataframe(billing, use_container_width=True, hide_index=True)
            st.subheader("Other Costs")
            st.dataframe(other, use_container_width=True, hide_index=True)

        st.subheader("DWR Timeline")
        dwr = dwr.sort_values("job_stop_date")
        fig = px.scatter(dwr, x="job_stop_date", y="milestone", size=dwr["on_site_hours"].clip(lower=0.15),
                         hover_data=["dwr_name", "technician", "tech_subsidiary", "dummy_unit", "on_site_hours", "scope_of_work_performed"],
                         title=f"Lifecycle Events — {selected_wo}")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(dwr, use_container_width=True, hide_index=True)

with lifecycle_tab:
    selected_wos = set(filtered["work_order_number"])
    dwr_filtered = frames["fact_dwr_labor.csv"][frames["fact_dwr_labor.csv"]["work_order_number"].isin(selected_wos)].copy()
    if dwr_filtered.empty:
        st.info("No labor records match the current filters.")
    else:
        hours = dwr_filtered.groupby(["milestone", "tech_subsidiary"], as_index=False)["on_site_hours"].sum()
        fig = px.bar(hours, x="milestone", y="on_site_hours", color="tech_subsidiary", barmode="group",
                     title="Labor Hours by Milestone and Subsidiary")
        st.plotly_chart(fig, use_container_width=True)
        dummy = dwr_filtered.groupby("dummy_unit", as_index=False)["on_site_hours"].sum().sort_values("on_site_hours", ascending=False)
        st.dataframe(dummy, use_container_width=True, hide_index=True)

with scenario_tab:
    rate_defaults = frames["dim_labor_rate.csv"].set_index("tech_subsidiary")["hourly_rate"].to_dict()
    c1, c2, c3 = st.columns(3)
    psg_rate = c1.number_input("PSG burdened hourly rate", min_value=0.0, value=float(rate_defaults["Pearce Services Global"]), step=0.5)
    us_rate = c2.number_input("US Fielding burdened hourly rate", min_value=0.0, value=float(rate_defaults["Pearce Services"]), step=1.0)
    threshold = c3.slider("At-risk margin threshold", min_value=-0.20, max_value=0.60, value=0.22, step=0.01, format="%.0f%%")
    scenario = recalculate_with_rates(filtered, psg_rate, us_rate, threshold)
    sc_revenue = scenario["forecast_revenue"].sum()
    sc_cost = scenario["scenario_actual_cost"].sum()
    sc_margin_pct = (sc_revenue - sc_cost) / sc_revenue if sc_revenue else 0
    s1, s2, s3 = st.columns(3)
    s1.metric("Scenario Cost", f"${sc_cost:,.0f}")
    s2.metric("Scenario Margin", f"{sc_margin_pct:.1%}")
    s3.metric("WOs Below Threshold", f"{scenario['scenario_at_risk'].sum():,}")
    chart_data = scenario[["work_order_number", "forecast_margin_pct", "scenario_margin_pct"]].melt(
        id_vars="work_order_number", var_name="calculation", value_name="margin_pct"
    )
    fig = px.box(chart_data, x="calculation", y="margin_pct", points="outliers", title="Baseline vs Scenario Margin Distribution")
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(
        scenario[["work_order_number", "forecast_revenue", "scenario_actual_cost", "scenario_margin_pct", "scenario_at_risk"]]
        .sort_values("scenario_margin_pct"),
        use_container_width=True,
        hide_index=True,
    )

with quality_tab:
    duplicate_wu = frames["fact_work_unit_revenue.csv"].duplicated(
        ["work_order_number", "sales_order_number", "work_unit_name", "work_unit_qty", "item_rate"], keep=False
    ).sum()
    missing_wo_dwr = (~frames["fact_dwr_labor.csv"]["work_order_number"].isin(frames["dim_work_order.csv"]["work_order_number"])).sum()
    zero_hour = frames["fact_dwr_labor.csv"]["on_site_hours"].eq(0).sum()
    negative_hours = frames["fact_dwr_labor.csv"]["on_site_hours"].lt(0).sum()
    no_work_units = (~frames["dim_work_order.csv"]["work_order_number"].isin(frames["fact_work_unit_revenue.csv"]["work_order_number"])).sum()
    q1, q2, q3, q4, q5 = st.columns(5)
    q1.metric("Potential duplicate WU rows", f"{duplicate_wu:,}")
    q2.metric("Orphan DWR rows", f"{missing_wo_dwr:,}")
    q3.metric("Zero-hour lifecycle events", f"{zero_hour:,}")
    q4.metric("Negative-hour rows", f"{negative_hours:,}")
    q5.metric("WOs without work units", f"{no_work_units:,}")
    st.markdown("""
    **Interpretation**
    - Zero-hour DWR records are intentionally retained as lifecycle/revenue-true-up events.
    - Potential duplicate work-unit rows should be validated by Sales Order line, not removed automatically.
    - Orphan records, negative hours, and work orders without work units should normally be zero.
    """)
