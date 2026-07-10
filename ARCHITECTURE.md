# Frequently Asked Questions

## What does profit and loss mean here?

It compares forecast revenue with accumulated labor and other costs for each work order.

## Is this an accounting system?

No. It is an analytical prototype and does not replace an enterprise resource planning, billing, or accounting platform.

## Is the dataset real?

No. Every record and identifier in the repository is synthetic.

## Why retain zero-hour records?

Some lifecycle events represent status or revenue-reconciliation activity without labor hours. Keeping them preserves the timeline.

## Why use the greater of estimated and billed revenue?

It is a demonstration forecast assumption. A real organization must define its own revenue-recognition and forecasting rules.

## Can one work order have multiple sales orders?

Yes. The data model explicitly supports a one-to-many relationship.

## Can the project connect to Snowflake?

Yes. The repository includes Snowflake table and view definitions and a mapping guide. The default public application reads synthetic CSV files.

## Can I publish the repository publicly?

The included version is designed for public demonstration, but review every file and the complete Git history before publication.

## Can I replace the synthetic data with real data?

Only in a private, authorized environment with appropriate security, privacy, governance, and financial validation.
