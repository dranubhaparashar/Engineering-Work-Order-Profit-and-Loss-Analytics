# Snowflake Integration

## Objective

Replace local synthetic CSVs with governed Snowflake tables or views while preserving the logical fields documented in this repository.

## Recommended flow

```mermaid
flowchart LR
    S[Source systems] --> STG[Raw or staging tables]
    STG --> CUR[Curated work-order views]
    CUR --> MART[Work-order profit and loss mart]
    MART --> APP[Streamlit application]
```

## Create the model

Run, after reviewing object names and permissions:

```sql
-- sql/snowflake_schema.sql
-- sql/profit_loss_views.sql
-- sql/quality_checks.sql
```

Use a dedicated database and schema in non-production first.

## Field mapping

Create a mapping document from each enterprise source field to the logical fields in `DATA_DICTIONARY.md`. Confirm:

- Join keys
- Source-of-truth ownership
- Data type and nullability
- Update frequency
- Historical availability
- Revenue status and recognition meaning
- Rate and cost ownership

## Effective-date rate join

The sample SQL joins on delivery organization only. Production logic should select the appropriate effective rate for each activity date. A common pattern is a lateral join ordered by effective date descending with a limit of one.

## Streamlit in Snowflake

For Streamlit in Snowflake:

- Read curated views with Snowpark.
- Grant the app role only required `USAGE` and `SELECT` privileges.
- Keep raw operational tables inaccessible to the app.
- Use caching carefully because data freshness requirements vary.

## External Streamlit

For an application outside Snowflake:

- Use the official connector or Snowpark client.
- Load credentials from a secret manager.
- Use key-pair or federated authentication where supported.
- Use a read-only role and restricted warehouse.
- Enforce network policies and private connectivity where appropriate.

## Data freshness

Choose a refresh approach based on the decision need:

| Use case | Suggested refresh |
|---|---|
| Executive portfolio monitoring | Daily or several times daily |
| Operational margin intervention | Hourly or event-driven |
| Billing reconciliation | Aligned to billing-system refresh |
| Historical reporting | Scheduled batch |

## Validation before release

Reconcile at least:

- Work-order counts
- Work-unit line counts
- Total estimated revenue
- Total billed amount by status
- Total hours by delivery organization
- Total non-labor cost by type
- Work-order-level margin samples
- Orphan and duplicate counts
