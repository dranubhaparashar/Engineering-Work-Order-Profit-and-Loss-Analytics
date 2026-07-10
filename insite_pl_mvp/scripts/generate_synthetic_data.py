from __future__ import annotations

import argparse
from pathlib import Path
from datetime import timedelta
import numpy as np
import pandas as pd

RNG = np.random.default_rng(20260609)

CUSTOMERS = ["Telecom Alpha", "Telecom Beta", "FiberLink", "MetroNet Demo"]
ACCOUNTS = ["Southeast Engineering", "Gulf Engineering", "Central Engineering"]
PROGRAMS = ["BAU Engineering", "ASE Expansion", "Fiber Modernization"]
JOB_CATEGORIES = ["Aerial Design", "Buried Design", "Mixed Plant", "Permit Only"]
REGIONS = ["AL", "FL", "GA", "LA", "MS", "TX"]
STATUSES = ["Closed", "Closed", "Closed", "In Progress", "Billing Pending", "On Hold"]

WORK_UNIT_CATALOG = [
    ("ESU00A-ESE22", "Engineering setup", "Each", 306.72, (1, 2)),
    ("ICP00A-ESE22", "Intake and close package", "Each", 359.10, (1, 1)),
    ("ACA00A-ESE22", "Aerial cable design footage", "Foot", 0.36, (150, 1600)),
    ("ACA02A-ESE22", "Buried cable design footage", "Foot", 0.27, (100, 1400)),
    ("POL00A-ESE22", "Pole loading analysis", "Pole", 22.50, (1, 18)),
    ("PRM00A-ESE22", "Permit package", "Each", 145.00, (0, 3)),
    ("FQC00A-ESE22", "Field quality control", "Each", 65.00, (0, 2)),
]

MILESTONES = [
    (1, "Intake", "Intake"),
    (2, "Pre-field", "Pre-field"),
    (3, "Fielding", "Field Travel"),
    (3, "Fielding", "Site Visit"),
    (3, "Fielding", "Fielding"),
    (3, "Fielding", "Field QC"),
    (4, "OCALC", "Pole loading"),
    (5, "Design", "Design"),
    (5, "Design", "Design QC"),
    (5, "Design", "Rework - Design"),
    (6, "Permitting", "Permit Admin"),
    (6, "Permitting", "Unscaled Permit"),
    (6, "Permitting", "Quality Control - Permit"),
    (7, "Final Delivery", "Final Delivery"),
    (7, "Final Delivery", "Rework - Final Delivery"),
    (8, "Billing", "Revenue true-up"),
]

PSG_TECHS = [f"PSG Technician {i:02d}" for i in range(1, 41)]
US_TECHS = [f"US Field Technician {i:02d}" for i in range(1, 21)]


def random_date(start: pd.Timestamp, end: pd.Timestamp) -> pd.Timestamp:
    days = (end - start).days
    return start + pd.Timedelta(days=int(RNG.integers(0, max(days, 1))))


def add_dwr(rows: list[dict], wo: str, dwr_id: int, technician: str, subsidiary: str,
            date: pd.Timestamp, milestone: str, dummy: str, hours: float, text: str) -> int:
    rows.append({
        "work_order_number": wo,
        "dwr_name": f"DWR-{dwr_id}",
        "technician": technician,
        "tech_subsidiary": subsidiary,
        "job_stop_date": date.date().isoformat(),
        "milestone": milestone,
        "dummy_unit": dummy,
        "on_site_hours": round(float(hours), 2),
        "scope_of_work_performed": text,
    })
    return dwr_id + 1


def generate(output_dir: Path, n_work_orders: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    wo_rows, wu_rows, dwr_rows, bill_rows, cost_rows = [], [], [], [], []
    dwr_id, sol_id, invoice_id, cost_id = 11000000, 1500000, 780000, 400000

    start_date = pd.Timestamp("2025-01-01")
    end_date = pd.Timestamp("2026-06-01")

    for idx in range(n_work_orders):
        wo_num = f"WO-{35000000 + idx:08d}"
        intake = random_date(start_date, end_date)
        status = str(RNG.choice(STATUSES))
        category = str(RNG.choice(JOB_CATEGORIES, p=[0.34, 0.26, 0.30, 0.10]))
        region = str(RNG.choice(REGIONS))
        duration = int(np.clip(RNG.normal(24, 12), 5, 75))
        planned_close = intake + pd.Timedelta(days=duration)
        actual_close = planned_close + pd.Timedelta(days=int(np.clip(RNG.normal(3, 8), -8, 30))) if status == "Closed" else pd.NaT
        target_margin = float(RNG.choice([0.28, 0.30, 0.32, 0.35]))
        wo_rows.append({
            "work_order_number": wo_num,
            "customer": str(RNG.choice(CUSTOMERS)),
            "account": str(RNG.choice(ACCOUNTS)),
            "budgeted_program": str(RNG.choice(PROGRAMS)),
            "job_category": category,
            "bid_region": region,
            "intake_date": intake.date().isoformat(),
            "planned_close_date": planned_close.date().isoformat(),
            "actual_close_date": actual_close.date().isoformat() if pd.notna(actual_close) else "",
            "status": status,
            "target_margin_pct": target_margin,
            "medium_risk_threshold_pct": 0.22,
            "high_risk_threshold_pct": 0.12,
        })

        sales_orders = [f"SO-{900000 + idx}"]
        if RNG.random() < 0.08:
            sales_orders.append(f"SO-{990000 + idx}")

        selected_units = [WORK_UNIT_CATALOG[0], WORK_UNIT_CATALOG[1]]
        if category in ["Aerial Design", "Mixed Plant"]:
            selected_units.append(WORK_UNIT_CATALOG[2])
        if category in ["Buried Design", "Mixed Plant"]:
            selected_units.append(WORK_UNIT_CATALOG[3])
        if category in ["Aerial Design", "Mixed Plant"] and RNG.random() < 0.75:
            selected_units.append(WORK_UNIT_CATALOG[4])
        if category == "Permit Only" or RNG.random() < 0.55:
            selected_units.append(WORK_UNIT_CATALOG[5])
        if RNG.random() < 0.35:
            selected_units.append(WORK_UNIT_CATALOG[6])

        total_est_revenue = 0.0
        for u_idx, (code, desc, unit_type, rate, qty_range) in enumerate(selected_units):
            low, high = qty_range
            qty = int(RNG.integers(low, high + 1)) if high > low else low
            if qty == 0:
                continue
            so = sales_orders[min(u_idx, len(sales_orders) - 1)]
            total = qty * rate
            total_est_revenue += total
            wu_rows.append({
                "work_order_number": wo_num,
                "sales_order_number": so,
                "sales_order_line": f"SOL-{sol_id}",
                "work_unit_name": code,
                "work_unit_description": desc,
                "unit_type": unit_type,
                "work_unit_qty": qty,
                "item_rate": rate,
                "total_rate": round(total, 2),
            })
            sol_id += 1

        current = intake
        # Intake and pre-field (PSG)
        dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                         "Intake", "Intake", RNG.uniform(0.25, 0.75), "Synthetic WO and project folder created.")
        current += pd.Timedelta(days=int(RNG.integers(0, 3)))
        dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                         "Pre-field", "Pre-field", RNG.uniform(0.5, 3.5), "Synthetic scoping and site-map preparation completed.")

        # US fielding and travel
        current += pd.Timedelta(days=int(RNG.integers(1, 8)))
        travel_hours = max(0.25, RNG.gamma(1.8, 1.2))
        field_hours = max(0.5, RNG.gamma(2.2, 1.0))
        us_tech = str(RNG.choice(US_TECHS))
        dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, us_tech, "Pearce Services", current,
                         "Fielding", "Field Travel", travel_hours, "Synthetic travel to and from the work site.")
        dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, us_tech, "Pearce Services", current,
                         "Fielding", "Site Visit", RNG.uniform(0.75, 2.5), "Synthetic site visit and local-contact coordination.")
        dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, us_tech, "Pearce Services", current,
                         "Fielding", "Fielding", field_hours, "Synthetic aerial/buried field measurements captured.")

        # PSG QC/design
        current += pd.Timedelta(days=int(RNG.integers(1, 5)))
        dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                         "Fielding", "Field QC", RNG.uniform(0.2, 0.8), "Synthetic field package reviewed.")
        if category in ["Aerial Design", "Mixed Plant"]:
            dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                             "OCALC", "Pole loading", RNG.uniform(0.3, 2.5), "Synthetic pole-loading extraction and submission.")

        current += pd.Timedelta(days=int(RNG.integers(1, 5)))
        design_blocks = int(RNG.integers(1, 4))
        for _ in range(design_blocks):
            dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                             "Design", "Design", RNG.uniform(1.0, 8.5), "Synthetic design production and record correction.")
            current += pd.Timedelta(days=int(RNG.integers(0, 3)))
        dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                         "Design", "Design QC", RNG.uniform(0.75, 3.5), "Synthetic design quality-control review completed.")

        # Rework deliberately influences risk distribution
        rework_probability = 0.18 + (0.10 if category == "Mixed Plant" else 0)
        if RNG.random() < rework_probability:
            rework_hours = RNG.uniform(0.5, 7.5)
            dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                             "Design", "Rework - Design", rework_hours, "Synthetic customer or QC corrections implemented.")

        # Permitting
        if category == "Permit Only" or RNG.random() < 0.62:
            current += pd.Timedelta(days=int(RNG.integers(0, 4)))
            for milestone_name, dummy_name, low, high in [
                ("Permitting", "Permit Admin", 0.2, 2.5),
                ("Permitting", "Unscaled Permit", 0.5, 4.5),
                ("Permitting", "Quality Control - Permit", 0.4, 2.5),
            ]:
                if RNG.random() < 0.8:
                    dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                                     milestone_name, dummy_name, RNG.uniform(low, high), "Synthetic permit preparation or submission activity.")

        current += pd.Timedelta(days=int(RNG.integers(1, 5)))
        dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                         "Final Delivery", "Final Delivery", RNG.uniform(0.5, 1.5), "Synthetic final package review and delivery.")
        if RNG.random() < 0.08:
            dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                             "Final Delivery", "Rework - Final Delivery", RNG.uniform(0.5, 3.0), "Synthetic final-delivery correction.")

        # Zero-hour lifecycle records retained intentionally
        for _ in range(int(RNG.integers(1, 4))):
            dwr_id = add_dwr(dwr_rows, wo_num, dwr_id, str(RNG.choice(PSG_TECHS)), "Pearce Services Global", current,
                             "Billing", "Revenue true-up", 0.0, "Synthetic units submitted for revenue true-up.")

        # Billing
        realization = float(np.clip(RNG.normal(0.98, 0.08), 0.75, 1.18))
        final_bill = total_est_revenue * realization
        if status == "Closed":
            pieces = int(RNG.integers(1, 4))
            weights = RNG.dirichlet(np.ones(pieces))
            for piece in weights:
                bill_rows.append({
                    "invoice_id": f"INV-{invoice_id}",
                    "work_order_number": wo_num,
                    "invoice_date": (current + pd.Timedelta(days=int(RNG.integers(0, 15)))).date().isoformat(),
                    "billing_status": "Paid" if RNG.random() < 0.78 else "Issued",
                    "billed_amount": round(final_bill * piece, 2),
                })
                invoice_id += 1
        elif status == "Billing Pending":
            bill_rows.append({
                "invoice_id": f"INV-{invoice_id}",
                "work_order_number": wo_num,
                "invoice_date": current.date().isoformat(),
                "billing_status": "Draft",
                "billed_amount": round(final_bill * RNG.uniform(0.15, 0.55), 2),
            })
            invoice_id += 1
        elif status == "In Progress" and RNG.random() < 0.35:
            bill_rows.append({
                "invoice_id": f"INV-{invoice_id}",
                "work_order_number": wo_num,
                "invoice_date": current.date().isoformat(),
                "billing_status": "Progress Billing",
                "billed_amount": round(final_bill * RNG.uniform(0.10, 0.40), 2),
            })
            invoice_id += 1

        # Other costs
        mileage_amount = travel_hours * RNG.uniform(12, 32)
        cost_rows.append({
            "cost_id": f"COST-{cost_id}", "work_order_number": wo_num,
            "cost_date": current.date().isoformat(), "cost_type": "Mileage/Travel",
            "amount": round(mileage_amount, 2), "description": "Synthetic mileage and travel expense"
        })
        cost_id += 1
        if category == "Permit Only" or RNG.random() < 0.50:
            cost_rows.append({
                "cost_id": f"COST-{cost_id}", "work_order_number": wo_num,
                "cost_date": current.date().isoformat(), "cost_type": "Permit Fee",
                "amount": round(float(RNG.uniform(25, 280)), 2), "description": "Synthetic permit or filing fee"
            })
            cost_id += 1
        if RNG.random() < 0.05:
            cost_rows.append({
                "cost_id": f"COST-{cost_id}", "work_order_number": wo_num,
                "cost_date": current.date().isoformat(), "cost_type": "Subcontractor",
                "amount": round(float(RNG.uniform(150, 900)), 2), "description": "Synthetic subcontractor expense"
            })
            cost_id += 1

    pd.DataFrame(wo_rows).to_csv(output_dir / "dim_work_order.csv", index=False)
    pd.DataFrame(wu_rows).to_csv(output_dir / "fact_work_unit_revenue.csv", index=False)
    pd.DataFrame(dwr_rows).to_csv(output_dir / "fact_dwr_labor.csv", index=False)
    pd.DataFrame(bill_rows).to_csv(output_dir / "fact_billing.csv", index=False)
    pd.DataFrame(cost_rows).to_csv(output_dir / "fact_other_cost.csv", index=False)
    pd.DataFrame([
        {"tech_subsidiary": "Pearce Services Global", "effective_date": "2025-01-01", "hourly_rate": 18.50, "currency": "USD", "rate_type": "Synthetic burdened rate"},
        {"tech_subsidiary": "Pearce Services", "effective_date": "2025-01-01", "hourly_rate": 52.00, "currency": "USD", "rate_type": "Synthetic burdened rate"},
    ]).to_csv(output_dir / "dim_labor_rate.csv", index=False)
    pd.DataFrame([
        {"milestone_order": order, "milestone": milestone, "dummy_unit": dummy}
        for order, milestone, dummy in MILESTONES
    ]).to_csv(output_dir / "dim_milestone.csv", index=False)

    print(f"Generated {n_work_orders} work orders")
    print(f"Work units: {len(wu_rows):,}; DWR rows: {len(dwr_rows):,}; invoices: {len(bill_rows):,}; other costs: {len(cost_rows):,}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic Insite P&L MVP data")
    parser.add_argument("--output", default="data", help="Output data directory")
    parser.add_argument("--work-orders", type=int, default=600, help="Number of synthetic work orders")
    args = parser.parse_args()
    generate(Path(args.output), args.work_orders)
