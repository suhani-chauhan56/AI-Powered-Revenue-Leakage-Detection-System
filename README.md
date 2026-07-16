# AI-Powered Revenue Leakage Detection System

<p align="center">
  <a href="https://ai-powered-revenue-leakage-detection-system-99a3w4dnwjjmzzwwkp.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/Live%20Demo-Open%20Streamlit%20App-00C853?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo">
  </a>
  <a href="https://github.com/suhani-chauhan56/AI-Powered-Revenue-Leakage-Detection-System" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-Source%20Code-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/ML-XGBoost%20%2B%20Scikit--Learn-1f77b4?style=for-the-badge" alt="ML Stack">
</p>

<p align="center">
  <b>End-to-end analytics and machine learning project for identifying, quantifying, and predicting revenue leakage in e-commerce operations.</b>
</p>

<p align="center">
  <span style="color:#0ea5e9"><b>Python</b></span> •
  <span style="color:#22c55e"><b>SQL</b></span> •
  <span style="color:#f97316"><b>XGBoost</b></span> •
  <span style="color:#38bdf8"><b>Streamlit</b></span> •
  <span style="color:#8b5cf6"><b>Power BI</b></span>
</p>

---

## Live Demo

<div style="padding:16px; border-left:5px solid #00C853; background:#f8fafc; border-radius:10px;">

Try the deployed dashboard here:

**[Open the Streamlit app](https://ai-powered-revenue-leakage-detection-system-99a3w4dnwjjmzzwwkp.streamlit.app/)**

</div>

---

## What This Project Does

This project turns raw Olist marketplace data into a business-ready leakage intelligence workflow.

- It builds a clean order-level fact table from multiple raw CSV sources.
- It engineers operational proxy signals for leakage such as late delivery, low reviews, freight burden, and cancellations.
- It loads the engineered data into SQL for reporting and analysis.
- It trains a classification model to flag high-risk orders.
- It delivers an interactive Streamlit dashboard for executives and analysts.

---

## Why This Matters

Revenue leakage is often hidden in operational data rather than labeled directly.

This project helps answer practical business questions like:

- Which orders are most likely to create margin loss?
- Which sellers or categories deserve operational attention?
- How much leakage is recoverable if the team intervenes early?
- Where should finance and operations focus first?

---

## Dataset Overview

The project uses the public **Olist e-commerce dataset**, which contains transactional data for a large Brazilian marketplace.

### Raw sources included

- `data/olist_orders_dataset.csv`
- `data/olist_order_items_dataset.csv`
- `data/olist_order_payments_dataset.csv`
- `data/olist_order_reviews_dataset.csv`
- `data/olist_products_dataset.csv`
- `data/olist_customers_dataset.csv`
- `data/olist_sellers_dataset.csv`
- `data/product_category_name_translation.csv`
- `data/olist_geolocation_dataset.csv`

### Processed output

- `data/processed_fact_orders.csv`
- `data/olist_leakage_db.db`

### Processed dataset shape

- **Rows:** 99,441 orders
- **Columns:** 35 engineered fields

### Important engineered fields

- `is_cancelled`
- `is_late`
- `delay_days`
- `is_low_review`
- `freight_ratio`
- `is_high_freight_burden`
- `is_payment_issue`
- `leakage_amount`
- `leakage_reason`
- `order_month`

---

## Key Outcomes

On the included processed dataset, the pipeline surfaces these outcomes:

- **Gross leakage:** about **R$ 1.17M**
- **Orders with non-zero leakage:** **45,857**
- **Largest leakage driver:** **High Freight Burden**
- **Strongest customer-friction signals:** late delivery and low review combinations
- **Model usage:** the Streamlit app can score a transaction in real time

---

## Key Insights

- 🚚 **Freight burden is the biggest margin leak.** Shipping costs above the price threshold create the highest concentration of loss.
- ⏱️ **Delivery delays are not just an operations issue.** They correlate with poor customer experience and financial leakage.
- ⭐ **Low review scores are a useful proxy for after-sale risk.** They help identify refund and support pressure.
- 🧾 **Cancellations are the cleanest leakage signal.** These are typically the most expensive and easiest to explain to stakeholders.
- 🏷️ **A small number of categories and sellers drive a disproportionate share of leakage.** This is ideal for targeted remediation.

---

## Business Impact

This project can help a finance or operations team:

- prioritize recovery opportunities instead of reviewing every order manually
- quantify margin loss in financial terms
- identify sellers that need SLA review
- spot product categories with costly freight patterns
- create an early-warning system for risky transactions
- support CFO-level reporting with a simple and repeatable leakage framework

In a real company, the same logic could be used to:

- reduce refunds and credits
- improve shipping policy
- improve seller scorecards
- focus operations reviews on the highest-risk transactions

---

## System Architecture

```text
Raw Olist CSV files
  ↓
ETL pipeline (`python/etl.py`)
  ↓
Feature engineering (`python/transform.py`)
  ↓
Processed fact table (`data/processed_fact_orders.csv`)
  ↓
SQL warehouse load (`python/load_to_sql.py`)
  ↓
Analytics queries (`sql/analytics_queries.sql`)
  ↓
Model training (`notebooks/02_modeling.ipynb`)
  ↓
Streamlit dashboard (`streamlit/app.py`)
```

---

## Core Files

- [`python/etl.py`](python/etl.py) builds the order-level fact table.
- [`python/transform.py`](python/transform.py) engineers leakage signals and the leakage amount.
- [`python/load_to_sql.py`](python/load_to_sql.py) exports the data and loads it into MySQL or SQLite.
- [`sql/schema.sql`](sql/schema.sql) defines the warehouse schema.
- [`sql/analytics_queries.sql`](sql/analytics_queries.sql) contains reporting queries.
- [`notebooks/01_eda.ipynb`](notebooks/01_eda.ipynb) explores the dataset and validates patterns.
- [`notebooks/02_modeling.ipynb`](notebooks/02_modeling.ipynb) trains the classifier and anomaly detector.
- [`streamlit/app.py`](streamlit/app.py) hosts the interactive dashboard.

---

## Streamlit Dashboard

The dashboard now includes:

- executive KPIs
- leakage-by-reason charts
- monthly leakage trends
- category and seller drilldowns
- a live risk simulator
- business impact summaries

### What the simulator shows

- predicted leakage risk
- gauge visualization
- estimated transaction impact
- recommended mitigation steps

---

## How To Run

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### Deployment note

For Streamlit Community Cloud, use Python 3.12 in the app settings. This repo also includes
[`runtime.txt`](runtime.txt) as a version hint, but the Streamlit Cloud Python selector is the
authoritative setting.

The runtime requirements are intentionally minimal so the dashboard can deploy cleanly:

- `streamlit`
- `pandas`
- `numpy`
- `plotly`
- `scikit-learn`
- `xgboost`

Optional database packages for local ETL loading:

- `SQLAlchemy`
- `PyMySQL`

If you only want to deploy the Streamlit dashboard, you do not need the optional database packages.

### 3. Run the ETL step

```powershell
python python/etl.py
```

**Output:** builds the joined fact table and prints the final shape.

### 4. Run feature engineering

```powershell
python python/transform.py
```

**Output:** creates leakage flags, leakage amount, and leakage reasons.

### 5. Run the full load pipeline

```powershell
python python/load_to_sql.py
```

**Output:** exports `data/processed_fact_orders.csv` and loads the table into SQL.

### 6. Run the prediction smoke test

```powershell
python test_predictions.py
```

**Output:** prints leakage stats and model prediction probabilities.

### 7. Launch the dashboard

```powershell
streamlit run streamlit/app.py
```

**Output:** opens the interactive revenue leakage control center in your browser.

### 8. Run the notebooks

```powershell
jupyter notebook
```

Open:

- `notebooks/01_eda.ipynb`
- `notebooks/02_modeling.ipynb`

---

## Expected Outputs

### `python/etl.py`

- joins raw Olist tables
- prints the fact table shape

### `python/transform.py`

- creates leakage labels
- prints total leakage calculated

### `python/load_to_sql.py`

- exports the processed file
- loads data into MySQL if configured
- falls back to SQLite if MySQL is unavailable

### `test_predictions.py`

- inspects the leakage distribution
- prints target counts
- tests the saved model on low-risk and high-risk samples

### `streamlit/app.py`

- shows dashboard KPIs
- renders leakage charts
- displays prediction risk and mitigation guidance

---

## Machine Learning Layer

The modeling notebook builds:

- a preprocessing pipeline with imputation, scaling, and one-hot encoding
- an `XGBClassifier` for high-leakage classification
- an `IsolationForest` model for anomaly detection

### Feature set

Numeric:

- `total_price`
- `total_freight`
- `freight_ratio`
- `installments`
- `delay_days`

Categorical:

- `payment_type`
- `product_category_name_english`

---

## SQL Analytics

The SQL layer includes queries for:

- leakage by root cause
- monthly leakage trend
- seller ranking
- category-level leakage
- delivery funnel analysis

Use these queries to power a BI dashboard or ad hoc reporting.

---

