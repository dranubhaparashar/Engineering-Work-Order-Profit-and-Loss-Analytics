# Contributing

## Before contributing

- Keep all examples and test data synthetic.
- Do not include confidential company, customer, employee, or production information.
- Open an issue for large design changes before implementing them.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

## Pull requests

A pull request should:

- Explain the problem and approach.
- Include tests for changed calculations.
- Update relevant documentation and the data dictionary.
- Pass `pytest -q` and Python compilation.
- Avoid unrelated formatting changes.
- Confirm that no confidential data or credentials were added.

## Issues

Use the included bug and feature templates. Provide reproducible steps and synthetic examples only.

## Code style

Use readable names, type hints, small reusable functions, and explicit null handling. Keep financial logic in `src/metrics.py` rather than embedding it in dashboard presentation code.
