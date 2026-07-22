# Smart Retail Analytics Platform

A retail analytics web application built with **Flask**, **Pandas**, **NumPy**, **SQLite** and **Chart.js**. Upload sales CSV files, explore interactive dashboards, and generate reports (summary, CSV, Excel).

## Features

* User registration and login (session-based auth)
* CSV sales data upload, stored per user in SQLite
* Interactive dashboard with KPI cards (sales, profit, order value, orders)
* Charts: monthly sales trend, sales by region, sales by category, profit
* Per-dataset selection on the dashboard
* Report export: summary (TXT), CSV, and Excel
* REST API for all analytics endpoints

## Technology Stack

* Python 3.10+
* Flask
* Flask-SQLAlchemy / SQLAlchemy
* SQLite
* Pandas
* NumPy
* Chart.js (frontend charts)
* Bootstrap 5 (UI)
* OpenPyXL (Excel export)

## Project Structure

```text
retail-analytics/
├── app.py                 # Application factory
├── config.py              # Configuration (dev, test, prod)
├── models.py              # SQLAlchemy models (User, Upload, Report)
├── requirements.txt
├── README.md
├── database.db            # SQLite DB (auto-created)
├── uploads/               # Uploaded CSV files
├── reports/               # Generated reports
├── data/                  # Default superstore dataset
├── routes/
│   ├── landing.py         # Landing page (/)
│   ├── auth.py            # Sign up, login, logout
│   ├── dashboard.py       # Dashboard (/dashboard)
│   ├── upload.py          # Upload (/upload)
│   ├── api.py             # Analytics API (/api)
│   └── reports.py         # Reports (/reports)
├── services/              # Analytics & report generation
├── utils/                 # Validators, data loading, cleaning
├── static/                # CSS and JS
├── templates/             # Jinja2 templates
└── tests/                 # Pytest test suite
```

## Workflow

1. Visit the **landing page** (`/`) and click **Get Started**.
2. **Sign up** for an account (or **Sign In** with the default admin).
3. Open the **Dashboard** (`/dashboard`) and upload your first CSV.
4. View KPIs and charts, then download **Reports**.

## Prerequisites

* Python 3.10 or newer
* `pip` and (optionally) `venv`

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd retail-analytics
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment variables

The app uses a `SECRET_KEY` for sessions. Set it (or rely on the dev fallback):

```bash
# Windows (PowerShell)
$env:SECRET_KEY = "your-strong-secret-key"

# macOS / Linux
export SECRET_KEY="your-strong-secret-key"
```

### 6. Run the application

```bash
python app.py
```

The SQLite database (`database.db`) and the `uploads/` / `reports/` folders are created automatically on first run.

### 7. Default admin credentials

A default admin user is created on first run:

```
username: admin
password: admin
```

Visit <http://127.0.0.1:5000> in your browser.

## Database

The database is auto-created on first run via `db.create_all()`.

### Schema

* **users** — `id`, `username` (unique), `email` (unique), `password_hash`, `created_at`
* **uploads** — `id`, `filename`, `filepath`, `user_id` (FK), `rows_count`, `uploaded_at`
* **reports** — `id`, `upload_id` (FK), `report_type`, `filepath`, `created_at`

### Reset the database

Stop the app and delete the database file:

```bash
rm database.db        # macOS / Linux
del database.db       # Windows
```

It will be recreated on the next run (including the default admin user).

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Landing page |
| GET | `/signup` | Sign up page |
| POST | `/signup` | Create account + auto login |
| GET/POST | `/login` | Login |
| GET | `/logout` | Logout |
| GET | `/dashboard/` | Dashboard (requires login) |
| GET/POST | `/upload` | Upload page (requires login) |
| GET | `/api/uploads` | List uploads |
| GET | `/api/dashboard?upload_id=` | Dashboard KPIs |
| GET | `/api/sales/monthly?upload_id=` | Monthly sales |
| GET | `/api/top-products?n=&upload_id=` | Top products |
| GET | `/api/sales/by-region?upload_id=` | Sales by region |
| GET | `/api/sales/by-category?upload_id=` | Sales by category |
| GET | `/reports/summary` | Download summary report |
| GET | `/reports/csv` | Download CSV export |
| GET | `/reports/excel` | Download Excel export |

## Testing

Run the test suite with:

```bash
pytest
```

Run linting with:

```bash
flake8
```

## License

This project is developed for educational and learning purposes.
