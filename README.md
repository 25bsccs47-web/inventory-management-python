# Inventory Management (CSV + Tkinter)

This project stores inventory in a local CSV file (`inventory.csv`) and provides a simple Tkinter GUI to add, update, delete, and view items.

Running locally

1. (Optional) Create and activate a virtual environment.

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows (cmd):

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

2. Run the app (no extra packages required):

```bash
python app.py
```

Files changed

- `app.py` — replaced with a CSV-backed Tkinter GUI that reads/writes `inventory.csv`.

Notes

- The CSV file `inventory.csv` will be created automatically when you run the app.
- If you prefer the old CLI/sqlite version, let me know and I can restore it or provide a migration.

Web version (run on localhost)

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Start the server:

```bash
python web_app.py
```

Open your browser at http://127.0.0.1:5000 to use the web UI.
