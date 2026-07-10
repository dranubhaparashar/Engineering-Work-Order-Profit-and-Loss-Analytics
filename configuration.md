# Installation

## Supported environments

- Windows 10 or 11
- macOS
- Current Linux distributions
- Python 3.10, 3.11, 3.12, or 3.13

## Windows automated setup

From PowerShell:

```powershell
cd path\to\engineering-workorder-profit-loss-analytics
.\setup_and_run.ps1
```

The script creates `.venv`, installs dependencies, and launches Streamlit.

PowerShell may block local scripts. For the current terminal session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup_and_run.ps1
```

The batch-file alternative is:

```cmd
setup_and_run.bat
```

## Windows manual setup

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## macOS and Linux

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Verify installation

```bash
pytest -q
python -m compileall app.py src scripts tests
```

## Stop the application

Press `Ctrl+C` in the terminal running Streamlit.

## Remove the local environment

Deactivate and delete `.venv`:

```bash
deactivate
```

Then remove the directory using the file manager or terminal.
