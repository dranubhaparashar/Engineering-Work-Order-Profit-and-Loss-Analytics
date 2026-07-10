# Security and Privacy

## Public repository boundary

The repository is intended for synthetic data only. Do not commit real operational exports, screenshots, sample customer files, internal table names, credentials, or proprietary rate cards.

## Sensitive information to exclude

- Customer and employee identities
- Email addresses and phone numbers
- Precise sites or coordinates
- Contract terms and rate cards
- Invoice and purchase-order details
- Authentication tokens and connection strings
- Internal architecture diagrams or system names
- Unreleased business rules

## Secrets handling

Use environment variables, a cloud secret manager, or Streamlit secrets for private deployments. `.streamlit/secrets.toml` is ignored by Git.

## Access control

The local demonstration has no login. A real deployment must add authentication and authorization before connecting real data.

## Data minimization

Expose only fields required for the decision. Prefer aggregated views and pseudonymous identifiers. Restrict free-text scope descriptions because they may contain names, addresses, or customer details.

## Repository-history review

Deleting a file in a later commit does not remove it from prior Git history. Before public release, review the full history and rewrite it if sensitive content was ever committed.

## Vulnerability reporting

Follow `SECURITY.md` and avoid posting exploitable details in public issues.
