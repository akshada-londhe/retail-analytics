# Retail Analytics - Issues & Fixes Report

**Repository:** https://github.com/akshada-londhe/retail-analytics
**Generated:** 2026-07-17
**Tool:** flake8 + pylint + manual code review + test execution

---

## Executive Summary

| Category | Count |
|---|---|
| Critical Bugs | 5 |
| Significant Bugs | 6 |
| UI/UX Issues | 8 |
| Code Quality Issues | 10 |
| Linting Issues (flake8) | 70+ |
| Pylint Warnings | 13 |
| Test Failures | 0 (22/22 pass) |

---

## 1. CRITICAL BUGS (Will cause runtime errors or data corruption)

### BUG-01: Logout redirects to non-existent route `/dashboard`
- **File:** `routes/auth.py:27`
- **Problem:** `return redirect('/dashboard')` - No route is registered at `/dashboard`. The dashboard is at `/`. This causes a **404 error** on every logout.
- **Fix:**
```python
# routes/auth.py:27
return redirect('/')
```

### BUG-02: Upload uses hardcoded `user_id=1` with no user creation
- **File:** `routes/upload.py:38`
- **Problem:** `user_id=1` is hardcoded but no User with `id=1` is ever created. There is no registration route. The `password_hash` field exists but no hashing code exists. This causes a **foreign key constraint violation** on every upload.
- **Fix:**
```python
# Option A: Remove user association from uploads temporarily
upload = Upload(filename=filename, filepath=filepath, rows_count=rows_count, user_id=1)

# Option B: Create a default user on first run (recommended)
# In app.py create_app(), after db.create_all():
from models import User
if not User.query.filter_by(username='admin').first():
    admin = User(username='admin', email='admin@example.com',
                 password_hash='not-hashed-yet')
    db.session.add(admin)
    db.session.commit()
```

### BUG-03: `dashboard.js` race condition - Chart.js loaded dynamically before DOM ready
- **File:** `static/js/dashboard.js:2-9`
- **Problem:** `loadDashboard()` is called on Chart.js `onload` which fires immediately when the script tag is parsed. `document.getElementById(...)` calls inside `loadDashboard()` will fail because DOM elements in `dashboard.html` don't exist yet on non-dashboard pages (login, upload) and may not exist even on the dashboard page depending on script execution order.
- **Impact:** Charts and KPI cards silently fail to render on some page loads.
- **Fix:**
```javascript
// static/js/dashboard.js - wrap everything in DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    const chartScript = document.createElement('script');
    chartScript.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js';
    document.head.appendChild(chartScript);
    chartScript.onload = function() {
        loadDashboard();
    };
});

function loadDashboard() {
    // ... existing fetch code
}
```

### BUG-04: `base.html` loads `dashboard.js` on ALL pages
- **File:** `templates/base.html:31`
- **Problem:** `<script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>` is in `base.html`, so it loads on login, upload, and dashboard pages. On non-dashboard pages, `loadDashboard()` runs and calls `fetch('/api/dashboard')` + renders charts on `<canvas>` elements that don't exist, causing JavaScript errors in the console.
- **Fix:** Move the script include to `dashboard.html` only:
```html
<!-- base.html: remove line 31 -->
<!-- dashboard.html: add at end of content block -->
{% block scripts %}
<script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>
{% endblock %}
```

### BUG-05: `dashboard.js` renders region data into "categoryChart" canvas
- **File:** `static/js/dashboard.js:60`
- **Problem:** The region sales data is fetched from `/api/sales/by-region` but rendered into a canvas with `id="categoryChart"`. The dashboard template (`dashboard.html:50`) names this canvas `categoryChart` but the data is regional, not categorical. The API endpoint `/api/sales/by-region` returns region data, not category data.
- **Impact:** The chart title says "Sales by Region" but the canvas ID suggests categories. Misleading naming. Also, there's no actual category breakdown chart.
- **Fix:** Either rename the canvas to `regionChart` and update the ID references, or add a separate category API endpoint.

---

## 2. SIGNIFICANT BUGS (Functional issues, data problems)

### BUG-06: Every API endpoint reloads and re-processes the same CSV
- **File:** `routes/api.py:14,27,41,55`
- **Problem:** Each of the 4 API endpoints independently calls `load_dataset()` -> `clean_data()` -> `engineer_features()`. The dashboard page calls 3 of these endpoints, meaning the CSV is loaded and processed **3 times** per page load.
- **Fix:** Cache the processed DataFrame or load once and pass to all endpoints:
```python
# Use Flask's g object or a module-level cache
from flask import g

def get_processed_df():
    if 'df' not in g:
        g.df = engineer_features(clean_data(load_dataset('data/superstore.csv')))
    return g.df
```

### BUG-07: Upload data is saved but never used by the dashboard
- **File:** `routes/api.py:14` vs `routes/upload.py:30`
- **Problem:** Uploaded files are saved to `uploads/` and logged in the database, but all API endpoints hardcode `'data/superstore.csv'`. Users upload data that can never be analyzed.
- **Fix:** Add an endpoint to select which upload to analyze, or use the latest upload.

### BUG-08: Config side effects at import time
- **File:** `config.py:18-19`
- **Problem:** `os.makedirs()` calls execute at class definition time (import time). Directories are created even during testing, linting, or when the module is just imported.
- **Fix:** Move to `create_app()` or use `@app.before_first_request`:
```python
# In app.py create_app():
import os
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)
```

### BUG-09: `Config.UPLOAD_FOLDER` used directly instead of app config
- **File:** `routes/upload.py:30`
- **Problem:** `filepath = os.path.join(Config.UPLOAD_FOLDER, filename)` uses the base `Config` class attribute, not the app's resolved config. If `UPLOAD_FOLDER` is overridden in `DevelopmentConfig` or `ProductionConfig`, it will be ignored.
- **Fix:**
```python
from flask import current_app
filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
```

### BUG-10: `services/reports.py` functions are dead code
- **File:** `services/reports.py` (entire file)
- **Problem:** `generate_csv_report()`, `generate_excel_report()`, and `generate_summary_report()` are defined but never called from any route or service. No route exposes report generation.
- **Fix:** Add routes to expose these or remove the file.

### BUG-11: Unused dependencies in requirements.txt
- **File:** `requirements.txt:7,10`
- **Problem:** `matplotlib==3.7.1` and `reportlab==4.0.4` are listed but never imported anywhere in the codebase. `numpy==1.24.3` is only used transitively by pandas.
- **Fix:** Remove unused dependencies:
```
# Remove these lines:
matplotlib==3.7.1
reportlab==4.0.4
# numpy is transitive, keep only if needed
```

---

## 3. UI/UX ISSUES

### UI-01: No responsive grid on small screens
- **File:** `templates/dashboard.html:11,19,27,35`
- **Problem:** KPI cards use `col-md-3` which collapses to full-width on mobile but doesn't handle tablet well. Charts use `col-md-6` without responsive sizing.
- **Fix:** Use `col-sm-6 col-md-3` for cards and add `canvas` responsive styling.

### UI-02: Charts have no fixed height
- **File:** `templates/dashboard.html:47,50`
- **Problem:** `<canvas>` elements have no height set. On some screens they render at 0px height or overflow.
- **Fix:** Add CSS:
```css
canvas {
    max-height: 400px;
    width: 100% !important;
}
```

### UI-03: No loading states
- **File:** `static/js/dashboard.js`
- **Problem:** No loading spinner or skeleton UI while API calls are in progress. KPI cards show `$0` until data loads.
- **Fix:** Add a loading spinner and hide content until data arrives.

### UI-04: No error handling in JavaScript fetch calls
- **File:** `static/js/dashboard.js:13-24,27-53,56-86`
- **Problem:** No `.catch()` handlers on any `fetch()` calls. If the API returns an error (500), the error JSON is silently ignored. If the network fails, no feedback is shown.
- **Fix:** Add `.catch()` with user-visible error messages.

### UI-05: Login page has no link back to dashboard
- **File:** `templates/login.html`
- **Problem:** Once on the login page, there's no way to navigate to the dashboard without logging in (no "Continue as guest" option).
- **Fix:** Add a link to `/` or show read-only dashboard for unauthenticated users.

### UI-06: Upload page has no navigation feedback after upload
- **File:** `templates/upload.html`
- **Problem:** After successful upload, the page just shows a green alert. No link to view the uploaded data or dashboard.
- **Fix:** Add a "View Dashboard" link in the success message.

### UI-07: No dark mode or theme toggle
- **File:** `static/css/style.css`
- **Problem:** Only light theme is supported. The `#f8f9fa` background and Bootstrap defaults are fixed.
- **Fix:** Add CSS custom properties and a theme toggle.

### UI-08: Navbar doesn't highlight active page
- **File:** `templates/base.html:19-20`
- **Problem:** All nav links look the same. No `active` class is applied to the current page's link.
- **Fix:** Use Jinja2 blocks or JS to add `active` class to current nav item.

---

## 4. CODE QUALITY ISSUES

### CQ-01: Hardcoded credentials
- **File:** `routes/auth.py:14`
- **Problem:** `if username == 'admin' and password == 'admin'` - Hardcoded credentials with no hashing.
- **Fix:** Use environment variables and `werkzeug.security.check_password_hash()`.

### CQ-02: No session-based auth enforcement
- **Files:** All routes
- **Problem:** No route checks `session.get('user')`. Dashboard, upload, and API are publicly accessible. Login is purely decorative.
- **Fix:** Add `@login_required` decorator or check session in each route.

### CQ-03: `datetime.utcnow` deprecation
- **File:** `models.py:15,29,42`
- **Problem:** `datetime.utcnow` is deprecated in Python 3.12+.
- **Fix:** Use `datetime.now(timezone.utc)`.

### CQ-04: Missing docstrings
- **Files:** `utils/cleaner.py` functions, `services/reports.py` functions
- **Problem:** Several functions lack docstrings.
- **Fix:** Add docstrings to all public functions.

### CQ-05: `sys.path` manipulation in test conftest
- **File:** `tests/conftest.py:5`
- **Problem:** `sys.path.insert(0, str(project_root))` is a hack. Should use proper package installation.
- **Fix:** Add `setup.py` or `pyproject.toml` with `pip install -e .`.

### CQ-06: Broad exception catching
- **Files:** `routes/api.py:19,32,47,61`, `routes/upload.py:43`
- **Problem:** `except Exception as e` catches everything including `KeyboardInterrupt`, `SystemExit`.
- **Fix:** Catch specific exceptions or use `except (ValueError, FileNotFoundError) as e`.

### CQ-07: No CORS configuration
- **File:** `app.py`
- **Problem:** No CORS headers configured. If the API is consumed by external clients, requests will be blocked.
- **Fix:** Add `flask-cors` or manual CORS headers.

### CQ-08: `SECRET_KEY` fallback is insecure
- **File:** `config.py:8`
- **Problem:** `SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-prod"` - The fallback is a static string that would be committed to source control.
- **Fix:** Raise an error in production if `SECRET_KEY` is not set.

### CQ-09: Missing `.env.example`
- **File:** Project root
- **Problem:** No `.env.example` file to document required environment variables.
- **Fix:** Create `.env.example` with `SECRET_KEY=your-secret-key`.

### CQ-10: No database migrations
- **Files:** `models.py`, `app.py`
- **Problem:** Uses `db.create_all()` which doesn't handle schema changes. No Alembic/Flask-Migrate setup.
- **Fix:** Add Flask-Migrate for database migrations.

---

## 5. LINTING ISSUES (flake8)

### Unused Imports (F401)
| File | Import |
|---|---|
| `routes/upload.py:1` | `flask.jsonify` |
| `routes/upload.py:3` | `werkzeug.utils.secure_filename` |
| `services/analytics.py:1` | `pandas as pd` |
| `services/reports.py:1` | `os` |
| `services/reports.py:2` | `csv` |
| `services/reports.py:3` | `pandas as pd` |
| `utils/validators.py:1` | `os` |
| `tests/test_loader.py:5` | `pathlib.Path` |

### Whitespace Issues (W291-W293)
- **70+ instances** of trailing whitespace (W291), blank lines with whitespace (W293), and missing newlines at end of file (W292) across all files.
- **Affected files:** Every single `.py` file in the project.

### Indentation Issues (E128)
- `services/features.py:34-35` - continuation line under-indented
- `tests/test_features.py:49` - continuation line under-indented

### Blank Line Issues (E302, E303)
- `config.py:5` - Expected 2 blank lines before class definition
- `app.py:34,38` - Too many blank lines
- `routes/auth.py:14` - Too many blank lines
- `utils/load_data.py:10` - Too many blank lines

---

## 6. PYLINT WARNINGS

| File | Line | Warning |
|---|---|---|
| `app.py` | 8 | W0621: Redefining name 'app' from outer scope |
| `routes/api.py` | 19,32,47,61 | W0718: Catching too general exception |
| `routes/upload.py` | 43 | W0718: Catching too general exception |
| `services/reports.py` | 21 | W1514: Using open without explicitly specifying encoding |
| `utils/load_data.py` | 30 | W0707: Consider explicitly re-raising using `from e` |

**Pylint Score: 9.55/10**

---

## 7. TEST RESULTS

```
22 passed in 8.13s
```

All tests pass, but coverage is incomplete:
- No tests for `services/reports.py`
- No tests for `utils/validators.py`
- No tests for template rendering
- No tests for authentication flow
- No tests for file upload flow
- `test_cleaner.py` has an unused `sample_df` fixture

---

## 8. RECOMMENDED FIX PRIORITY

### Phase 1 - Critical (fix immediately)
1. Fix logout redirect (`/dashboard` -> `/`) - BUG-01
2. Fix `user_id=1` foreign key issue - BUG-02
3. Fix `dashboard.js` race condition - BUG-03
4. Move `dashboard.js` out of `base.html` - BUG-04
5. Fix chart canvas naming confusion - BUG-05

### Phase 2 - Important (fix soon)
6. Cache processed DataFrame in API - BUG-06
7. Connect uploaded data to dashboard - BUG-07
8. Move `os.makedirs` out of config import time - BUG-08
9. Use `current_app.config` in upload route - BUG-09
10. Add error handling to JavaScript - UI-04

### Phase 3 - Quality improvements
11. Remove unused imports (8 files)
12. Fix all whitespace issues
13. Add missing newlines at end of file
14. Remove unused dependencies from requirements.txt
15. Add auth enforcement to routes
16. Add loading states to dashboard
17. Add responsive chart sizing
18. Add `.env.example`

---

## 9. FILE-BY-FILE ISSUE INDEX

| File | Issues |
|---|---|
| `app.py` | E303, W291, W292, W0621 |
| `config.py` | E302, W292, side effects at import |
| `models.py` | W293 (x5), W292, deprecated `utcnow` |
| `routes/api.py` | F401, W293 (x2), W292, W0718 (x4), no caching |
| `routes/auth.py` | W293 (x3), E303, W292, hardcoded creds, wrong redirect |
| `routes/dashboard.py` | W292 |
| `routes/upload.py` | F401 (x2), W293 (x6), W292, hardcoded user_id, Config misuse |
| `services/analytics.py` | F401, W292 |
| `services/features.py` | W293 (x3), W291, E128 (x2), W292 |
| `services/reports.py` | F401 (x3), W293 (x8), W292, W1514, dead code |
| `utils/cleaner.py` | W293 (x6), W292 |
| `utils/load_data.py` | W293, E303, W292, W0707 |
| `utils/validators.py` | F401, W293 (x4), W292 |
| `tests/conftest.py` | W292, sys.path hack |
| `tests/test_analytics.py` | W292 |
| `tests/test_api.py` | W292 |
| `tests/test_cleaner.py` | W292, unused fixture |
| `tests/test_features.py` | W291 (x2), E128, W292 |
| `tests/test_loader.py` | F401, W293 (x2), W292 |
| `templates/base.html` | dashboard.js loaded on all pages |
| `templates/dashboard.html` | No chart height, misleading canvas ID |
| `static/js/dashboard.js` | Race condition, no error handling, no loading states |
| `static/css/style.css` | No chart sizing, no responsive breakpoints |
| `requirements.txt` | Unused deps: matplotlib, reportlab |
