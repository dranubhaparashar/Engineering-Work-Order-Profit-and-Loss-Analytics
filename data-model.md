# Synthetic Data Generation

## Purpose

The generator creates a realistic analytical demonstration without using real company records. It models relationships and variability rather than copying production rows.

## Run the generator

```bash
python scripts/generate_synthetic_data.py --output data --work-orders 600
```

## Reproducibility

The random-number generator uses a fixed seed:

```python
RNG = np.random.default_rng(20260609)
```

With the same code and parameters, output is reproducible.

## Generated behavior

Each work order receives:

- Customer, account, program, category, region, dates, status, and risk thresholds
- One or more sales orders and multiple work-unit lines
- Activity events through applicable lifecycle stages
- Delivery Center and Field Operations hours
- Optional rework, permitting, and final-delivery correction events
- One or more zero-hour revenue-reconciliation events
- Billing events depending on status
- Travel and optional permit or subcontractor costs

## Privacy design

The generator uses invented:

- Work-order, sales-order, activity, invoice, and cost identifiers
- Customer and account names
- Technician labels
- Work-unit codes and prices
- Dates, quantities, hours, and financial values
- Scope descriptions

## Change the dataset size

```bash
python scripts/generate_synthetic_data.py --output data --work-orders 50
python scripts/generate_synthetic_data.py --output data --work-orders 5000
```

Large outputs may require application and warehouse performance tuning.

## Change the patterns

Edit the catalogs and probability distributions near the top of the generator. After changing them, update documentation and tests so users understand the new assumptions.
