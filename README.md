# Smart Retail Analytics Platform

A production-style retail analytics platform built with **Flask**, **Pandas**, **NumPy**, **Matplotlib**, and **SQLite**. This project enables retail businesses to upload sales data, analyze business performance, generate reports, and visualize key metrics through an interactive dashboard.

## Features

* Sales data upload and processing
* Retail performance analytics
* Interactive dashboard
* Sales and profit visualization
* Inventory insights
* Report generation (PDF & Excel)
* SQLite database integration
* REST API using Flask

## Technology Stack

* Python 3.11+
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* Pandas
* NumPy
* Matplotlib
* SQLite
* ReportLab
* OpenPyXL

## Project Structure

```text
Retail Analytics/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── database.db
├── uploads/
├── reports/
├── templates/
├── static/
├── models/
├── routes/
├── services/
├── data/
├── notebooks/
└── venv/
```

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd Retail-Analytics
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

### 5. Run the application

```bash
python app.py
```

### 6. Open in your browser

```
http://127.0.0.1:5000
```

## Current API

### Home

**GET /**

Response:

```json
{
  "message": "Retail Analytics API",
  "status": "Running"
}
```

## Future Modules

* Customer Analytics
* Product Analytics
* Sales Forecasting
* Inventory Management
* Profit Analysis
* Report Generation
* Data Export
* Admin Dashboard

## Author

Akshada Londhe

## License

This project is developed for educational and learning purposes.
