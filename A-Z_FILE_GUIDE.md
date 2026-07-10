# Architecture

## 1. Purpose

Engineering Work Order Profit and Loss Analytics is a layered analytical application that combines work-order master data, work-unit revenue, labor activity, billing, labor rates, and other costs into a single work-order financial and lifecycle summary.

The public repository runs on synthetic CSV files. The same logical model can be implemented over governed Snowflake views or another analytical warehouse.

## 2. System context

```mermaid
flowchart TB
    U[Operations and Finance User]
    APP[Streamlit Analytics Application]
    CSV[Synthetic CSV Data]
    WH[Enterprise Data Warehouse]
    EXPORT[Filtered CSV Export]

    U -->|filters, selections, rate scenarios| APP
    APP -->|charts, tables, KPIs, risk reasons| U
    CSV -->|prototype mode| APP
    WH -.->|production mode through governed views| APP
    APP --> EXPORT
```

## 3. Logical layers

```mermaid
flowchart LR
    subgraph Sources
        WO[Work Order Master]
        WU[Work Units and Sales Orders]
        AR[Activity and Labor Reports]
        BL[Billing Events]
        OC[Other Costs]
        LR[Labor Rates]
    end

    subgraph Ingestion
        DL[src/data_loader.py]
        DQ[Schema and Data-Quality Validation]
    end

    subgraph Analytics
        REV[Revenue Aggregation]
        LAB[Labor Cost Aggregation]
        COST[Other Cost Aggregation]
        FIN[Profit and Loss Metrics]
        RISK[Rules-Based Risk Classification]
    end

    subgraph Presentation
        PORT[Portfolio Overview]
        DETAIL[Work Order Detail]
        LIFE[Lifecycle and Labor]
        SCEN[Rate Scenario]
        QUAL[Data Quality]
    end

    WO --> DL
    WU --> DL
    AR --> DL
    BL --> DL
    OC --> DL
    LR --> DL
    DL --> DQ
    DQ --> REV
    DQ --> LAB
    DQ --> COST
    REV --> FIN
    LAB --> FIN
    COST --> FIN
    FIN --> RISK
    RISK --> PORT
    RISK --> DETAIL
    RISK --> LIFE
    RISK --> SCEN
    DQ --> QUAL
```

## 4. Runtime sequence

```mermaid
sequenceDiagram
    participant User
    participant Streamlit as app.py
    participant Loader as src/data_loader.py
    participant Metrics as src/metrics.py
    participant Files as data/*.csv

    User->>Streamlit: Open application
    Streamlit->>Loader: load_data(DATA_DIR)
    Loader->>Files: Read required CSV files
    Files-->>Loader: DataFrames
    Loader-->>Streamlit: Dataset dictionary
    Streamlit->>Metrics: build_work_order_summary(...)
    Metrics-->>Streamlit: One row per work order
    User->>Streamlit: Apply filters or rate scenario
    Streamlit->>Metrics: recalculate_with_rates(...)
    Metrics-->>Streamlit: Scenario metrics
    Streamlit-->>User: KPIs, charts, tables, and export
```

## 5. Data model

The model follows a small analytical star pattern:

- `dim_work_order` is the central work-order dimension.
- `fact_work_unit_revenue` contains sales-order work-unit lines.
- `fact_activity_labor` contains activity and labor events.
- `fact_billing` contains invoices and progress billing.
- `fact_other_cost` contains non-labor expenses.
- `dim_labor_rate` maps a delivery organization to an effective hourly rate.
- `dim_milestone` standardizes lifecycle order and activity labels.

```mermaid
erDiagram
    DIM_WORK_ORDER ||--o{ FACT_WORK_UNIT_REVENUE : has
    DIM_WORK_ORDER ||--o{ FACT_ACTIVITY_LABOR : records
    DIM_WORK_ORDER ||--o{ FACT_BILLING : receives
    DIM_WORK_ORDER ||--o{ FACT_OTHER_COST : incurs
    DIM_LABOR_RATE ||--o{ FACT_ACTIVITY_LABOR : prices
    DIM_MILESTONE ||--o{ FACT_ACTIVITY_LABOR : classifies

    DIM_WORK_ORDER {
        string work_order_number PK
        string customer
        string account
        string budgeted_program
        string job_category
        string bid_region
        date intake_date
        string status
        decimal target_margin_pct
    }

    FACT_WORK_UNIT_REVENUE {
        string work_order_number FK
        string sales_order_number
        string sales_order_line
        string work_unit_name
        decimal work_unit_qty
        decimal item_rate
    }

    FACT_ACTIVITY_LABOR {
        string work_order_number FK
        string activity_report_id
        string technician
        string delivery_organization
        date activity_date
        string milestone
        string activity_type
        decimal labor_hours
    }
```

## 6. Component responsibilities

| Component | Responsibility |
|---|---|
| `app.py` | User interface, filtering, visualization, downloads, and scenario inputs |
| `src/data_loader.py` | Required-file checks, CSV parsing, and date conversion |
| `src/metrics.py` | Revenue, cost, margin, lifecycle, and risk calculations |
| `scripts/generate_synthetic_data.py` | Deterministic generation of synthetic dimensions and facts |
| `sql/*.sql` | Snowflake physical model, analytical views, and quality checks |
| `tests/` | Regression checks for grain, metrics, and scenario behavior |

## 7. Caching and performance

The application uses `st.cache_data` for source frames and the derived work-order summary. This prevents repeated file reads and metric recomputation during normal widget interactions.

For larger datasets:

- Push aggregation into Snowflake.
- Load only required columns and filtered date ranges.
- Materialize the work-order summary view.
- Add warehouse clustering or partitioning on activity date and work-order number.
- Paginate or sample detailed tables in the UI.

## 8. Security architecture

The public mode has no authentication and uses synthetic files. A real deployment should add:

- Identity provider authentication
- Role-based access control
- Row-level or account-level security
- Network restrictions and private connectivity
- Secrets management
- Audit logging
- Data retention and masking policies
- Separate development, test, and production environments

## 9. Production deployment patterns

### Pattern A: Streamlit in Snowflake

Use Snowpark DataFrames or SQL views and grant the application role access only to curated analytical views.

### Pattern B: External Streamlit application

Use a service account, private connectivity, encrypted secrets, and a read-only warehouse role.

### Pattern C: Scheduled extracts

Export governed summary files to controlled object storage and refresh the application on a schedule. This is simpler but less real-time.

## 10. Key architectural decisions

1. **One-row-per-work-order summary:** simplifies dashboard filtering and portfolio KPIs.
2. **Facts remain separate:** preserves auditability and drill-down.
3. **Rates are data, not constants:** supports scenario analysis and effective-date extensions.
4. **Zero-hour events are retained:** they can represent lifecycle transitions even when they have no labor cost.
5. **Risk reasons are explicit:** users can see why a work order was classified as high or medium risk.
6. **Synthetic data is generated in code:** the demonstration is reproducible and safe for public sharing.
