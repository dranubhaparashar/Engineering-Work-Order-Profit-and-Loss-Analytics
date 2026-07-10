# Deployment

## Local demonstration

The default deployment is local Streamlit over synthetic CSV files.

```bash
streamlit run app.py
```

## Streamlit Community Cloud

A public demonstration can be deployed from GitHub because the repository contains synthetic data only. Set the main file to `app.py` and confirm that no secrets or proprietary content exist in the complete Git history.

## Streamlit in Snowflake

Use this option when the data already resides in Snowflake and access must remain within Snowflake governance. Replace CSV loading with Snowpark queries against curated views.

## Container deployment

A container can run the application behind an authenticated reverse proxy. A production container should:

- Use a non-root user
- Pin dependencies
- Run vulnerability scans
- Expose only the Streamlit port internally
- Use a health check
- Load secrets at runtime

## Production checklist

- Written authorization to use the data
- Authentication and role-based access control
- HTTPS
- Centralized secrets management
- Read-only data access
- Audit logs
- Backup and recovery plan
- Monitoring and alerting
- Defined refresh service level
- Financial validation and sign-off
- Privacy and retention review

## Public-repository checklist

- Only synthetic data
- No real system names or screenshots
- No customer, employee, location, rate-card, or contract information
- No credentials in files or Git history
- Generic repository description
- Security and license files present
