# Retail Analytics Platform - Architecture & Codebase Guide

Welcome to the Retail Analytics Platform. This document is a complete, beginner-friendly guide to understanding the codebase structure, database models, blueprint routes, backend services, frontend scripts, and the dynamic data flows wiring everything together.

---

## 1. System Architecture

The application is structured using the **Model-View-Controller (MVC)** design pattern, backed by a service layer for data cleaning and analytical computation:

```
[Browser Client] <--- AJAX / JSON ---> [Flask Blueprint Controllers]
                                             |              |
                                         (SQLite)      (Data Engine)
                                             v              v
                                        [models.py]    [services / utils]
                                                            |
                                                            v
                                                     [Raw CSV Files]
```

1. **Model**: Defines the database schemas and manages persistence via SQLite ([models.py](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/models.py)).
2. **View**: Renders Jinja2 HTML templates and triggers dynamic client-side fetches ([templates/](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/templates/) & [static/](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/static/)).
3. **Controller**: Handles routing, page rendering, session management, and JSON API payloads ([routes/](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/routes/)).
4. **Service & Utility**: Loads, cleans, transforms, and analyzes raw transaction data ([utils/](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/utils/) & [services/](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/services/)).

---

## 2. Directory & Codebase Layout

```
├── data/
│   └── superstore.csv           # Small 984-byte baseline CSV for tests
├── routes/
│   ├── auth.py                  # Signup, login, logout, and password security
│   ├── api.py                   # Data endpoints (KPIs, monthly sales, top products, RFM)
│   ├── dashboard.py             # Page routes for Dashboard, Customers, and Products
│   ├── reports.py               # Compilation and download of TXT, CSV, and Excel exports
│   └── upload.py                # Dataset uploading, list management, activation, and deletion
├── services/
│   ├── analytics.py             # Calculations for LTV, KPIs, and RFM segment cuts
│   ├── features.py              # Feature engineering (Month, Year, Margins, Discount impacts)
│   └── reports.py               # Compiles summaries and exports files (Excel, CSV)
├── static/
│   ├── css/
│   │   └── style.css            # Custom theme styles (Dark mode, Light mode overrides)
│   └── js/
│       ├── app.js               # Theme state management and navigation hooks
│       └── dashboard.js         # API Ajax fetching, Chart.js mapping, and skeletons toggle
├── templates/
│   ├── base.html                # Sidebar frame and light/dark theme switch
│   ├── landing.html             # Marketing portal index page
│   ├── login.html               # User sign-in card
│   ├── signup.html              # Account signup form
│   ├── dashboard.html           # Main KPIs, trend lines, and category charts
│   ├── customers.html           # Top customer tables and RFM segmentation breakdowns
│   ├── products.html            # Category filtering and product ledger tables
│   ├── reports.html             # Text terminal report previewer and download cards
│   └── upload.html              # Dropzone form and active dataset switcher table
├── utils/
│   ├── auth.py                  # Route protection decorators (@login_required, @api_login_required)
│   ├── cleaner.py               # Removes duplicates/nulls and standardizes header names
│   └── load_data.py             # Safe CSV parsing supporting mixed datetime formats
├── tests/
│   └── test_api.py              # Automated routing and controller integration tests
├── app.py                       # Application bootstrapper
├── models.py                    # SQLite database models
└── config.py                    # Env configuration classes
```

---

## 3. Detailed Component Breakdown

### A. Database Models (`models.py`)
Uses Flask-SQLAlchemy to define three core tables:
1. `User`: Stores credentials (`username`, hashed `password`, `email`) and links to uploads.
2. `Upload`: Stores details of uploaded CSV files (`filename`, absolute `filepath`, `rows_count`, upload timestamp) associated with a user ID.
3. `Report`: Tracks generated exports (future audit log use).

### B. Core Data Pipeline & Utilities
When a CSV file is uploaded, it passes through:
* **Loader ([load_data.py](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/utils/load_data.py))**: Loads the CSV file into a Pandas DataFrame. It parses the date columns using `format='mixed'` and `errors='coerce'` to handle different formats safely.
* **Cleaner ([cleaner.py](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/utils/cleaner.py))**: Standardizes alternative column names (mapping `Customer Name` $\to$ `Customer`, `Product Name` $\to$ `Product`, and `Sub-Category` $\to$ `Sub Category`) to prevent parsing errors. It also drops duplicate rows, removes invalid non-positive sales, and strips trailing whitespaces.
* **Feature Engineering ([features.py](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/services/features.py))**: Adds computed analytical properties to the DataFrame:
  - Calendar periods: Extracts `Year`, `Month`, and `Quarter` from order dates.
  - Financial variables: Adds `Profit Margin %` and `Discount Impact`.
  - Customer values: Calculates `Total Customer Sales` and `Customer Lifetime Value (LTV)`.

### C. Analytics Engine (`services/analytics.py`)
Provides core analytical metrics by querying the processed DataFrame:
* `get_dashboard_kpis()`: Compiles total sales, total profit, total transactions, average order value, and count of unique products/customers.
* `get_customer_metrics()`: Groups records by customer name to compute their individual frequency, order counts, average order values, and total profit.
* `get_product_metrics()`: Groups records by product name to track category, sub-category, total sales, profit, and discount rates.
* `calculate_rfm_segments()`: Evaluates Recency, Frequency, and Monetary parameters for each client, applying Pandas `qcut` logic to rank clients into segment classifications (`Champions`, `Loyal Customers`, `New Customers`, `At Risk`, `Hibernating / Lost`).

### D. Blueprint Route Controllers
* **Main Dashboard Routing ([dashboard.py](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/routes/dashboard.py))**: Serves the primary page layouts. Verifies if the logged-in user has uploaded files (`has_uploads`) and passes this flag to templates to render empty states if needed.
* **API Endpoints ([api.py](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/routes/api.py))**: Exposes secure API paths (`/api/dashboard`, `/api/sales/monthly`, `/api/top-products`, etc.). It retrieves the user's active upload ID from their session, falls back to their latest file, retrieves the processed DataFrame from the cache, and returns the stats as JSON.
* **Reports Compilation ([reports.py](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/routes/reports.py))**: Directs text summary compilation and triggers downloads for Excel spreadsheet tables and raw CSV dumps.
* **Dataset Management ([upload.py](file:///C:/Users/chinm/.gemini/antigravity/worktrees/retail-analytics/finalize-full-app-polish/routes/upload.py))**: Handles new dataset additions, lists previously uploaded datasets, sets active workspace IDs, and deletes records.

---

## 4. Code Wirings & Data Flow

### The Complete Data Lifecycle:
```
1. File Uploaded ---> Saved to uploads/ ---> Database entry created
2. User selects Active Dataset ---> Saved to Session
3. Dashboard Loads ---> API fetches JSON from routes/api.py
4. API reads CSV ---> Standardizes headers ---> Adds columns (cleaner/features)
5. Analytics Engine calculates stats ---> Returns JSON to client
6. static/js/dashboard.js parses JSON ---> Hides shimmers ---> Renders Chart.js
```

### Routing Paths Alignment:
All URLs and blueprint handlers end with trailing slashes (e.g. `/dashboard/`, `/customers/`, `/products/`, `/upload/`, `/reports/`) to avoid redirection or `404 Not Found` errors in Flask.

---

## 5. Summary of Overhaul Fixes (What Changed)

1. **Strict User Workspaces**: Removed the global default fallback dataset for authenticated pages. Dashboards, reports, and charts are derived only from the user's uploaded datasets.
2. **Robust Datetime Parsing**: Modified date processing to use `format='mixed'` and `errors='coerce'`. This allows the application to parse different date formats safely.
3. **Column Standardization**: Implemented column header mapping to automatically standardize column names.
4. **Interactive Dataset Management Table**: Added a management table on `/upload/` that lists files, formats row counts, tracks the active dataset, and allows users to activate or delete uploads.
5. **No-flicker CSS Shimmers**: Added the `.d-none { display: none !important; }` class to resolve shimmer skeleton flickering and overlapping.
6. **Responsive Chart Layouts**: Wrapped canvas elements in a `.chart-container` and enabled `maintainAspectRatio: false` to ensure charts scale correctly without vertical overflows.
7. **Premium Cosmic Dark Mode & Rich Light Mode Styles**: Upgraded dark mode to a premium cosmic dark theme and light mode to a clear, high-contrast grid outline theme.
