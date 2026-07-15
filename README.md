# AI-Powered Revenue Leakage Detection System

### Olist E-commerce Dataset | Python • SQL • XGBoost • Streamlit • Power BI

This repository houses an end-to-end analytics and machine learning solution designed to identify, quantify, and predict **Revenue Leakage** across e-commerce operations. 

Using historical transaction data from **Olist** (100k+ orders in Brazil), the system models leakage signals—such as operational delays, severe customer dissatisfaction, and margin-eroding shipping rates—to advise financial executives (CFO/VP of Operations) on margin recovery opportunities.

---

## 1. Business Problem & Executive Framing
For digital marketplaces, revenue leakage is a silent margin killer. It is often hidden across multiple operational silos (logistics delays, support refunds, credit defaults, or payment defaults).
* **The Core Challenge**: Marketplace platforms like Olist do not have a column labeled "discount loss" or "refund cost". Leakage must be dynamically modeled by combining operational metrics with customer feedback proxies.
* **The Goal**: Calculate exactly where margins are eroding, quantify the recovery value, and deploy an automated predictive firewall that flags high-risk transactions before they incur loss.

---

## 2. System Architecture

```
Raw CSV Datasets (Olist)
  │
  ▼
Python ETL Pipeline (python/etl.py) ──► Joins Orders, Payments, Reviews, Sellers, Categories
  │
  ▼
Feature Engineering (python/transform.py) ──► Computes Leakage Amount, Reasons & Status Indicators
  ├── Export to: data/processed_fact_orders.csv
  │
  ├──► Database Warehouse Load (python/load_to_sql.py) ──► MySQL (Production) / SQLite (Fallback)
  │      └── Analytics Views (sql/analytics_queries.sql)
  │
  ├──► ML Model Pipeline (notebooks/02_modeling.ipynb)
  │      ├── Preprocessing: Pipeline (Scaler + OneHotEncoder)
  │      ├── Classifier: XGBoost (leakage_classifier_pipeline.pkl)
  │      └── Anomaly Detection: Isolation Forest (anomaly_detector.pkl)
  │
  └──► Visualizations & Interface
         ├── Streamlit Control Center (streamlit/app.py) ──► Live KPI Dashboard & AI Predictor Sandbox
         └── Power BI Dashboard ──► Strategic CFO reporting
```

---

## 3. Operations Leakage Proxy Rules

Since ground-truth financial loss isn't explicitly tagged in the raw dataset, the system engineers leakage amounts based on business-validated operational heuristics:

| Operational Signal | Target Metric | Business Rule / Formula | Assumed Leakage Multiplier |
| :--- | :--- | :--- | :--- |
| **Cancelled Orders** | `is_cancelled` | Order status is `canceled` or `unavailable` | **100% of order price** |
| **Late Deliveries + Poor Reviews** | `is_late` & `is_low_review` | Delivered date > Estimated date AND review score ≤ 2 | **70% of order price** (high refund risk) |
| **Freight Margin Erosion** | `freight_ratio` > 0.3 | Shipping costs exceed 30% of item price | **Excess Freight Value** (`freight_ratio` - 0.3) * price |
| **Severe Customer Dislike** | `is_low_review` | Review score is 1 or 2 (without delivery delay) | **20% of order price** (support overhead) |
| **Standard Delivery Delay** | `is_late` | Delivered date > Estimated date | **10% of order price** (retention credits) |

*Note: Overlaps are resolved sequentially in the order of severity listed above to avoid double-counting.*

---

## 4. Database Setup & SQL Analytics

Database tables are defined in [`sql/schema.sql`](file:///c:/Users/HP/Desktop/leakage%20Detection%20project/sql/schema.sql).

Advanced analytical queries are provided in [`sql/analytics_queries.sql`](file:///c:/Users/HP/Desktop/leakage%20Detection%20project/sql/analytics_queries.sql) to extract immediate summaries:
1. **Gross Leakage Categorization**: Highlights top operational leakage reasons.
2. **Cumulative Financial Trend**: Uses SQL Window functions to calculate Cumulative Margin Loss and Month-over-Month (MoM) change.
3. **High-Risk Seller Ranking**: Employs `RANK() OVER (ORDER BY SUM(leakage_amount) DESC)` to isolate the top 10 sellers responsible for logistics-based leakage.
4. **Product Category Pareto Analysis**: Evaluates freight burden ratios and leakage rates across product classifications.

---

## 5. Machine Learning Layer

The modeling pipeline is detailed in [`notebooks/02_modeling.ipynb`](file:///c:/Users/HP/Desktop/leakage%20Detection%20project/notebooks/02_modeling.ipynb):
* **Preprocessing Pipeline**: Integrates `SimpleImputer`, `StandardScaler` (for numerical metrics: price, freight, installments, delay days), and `OneHotEncoder` (for categoricals: payment type, product category) into a single reusable configuration block.
* **XGBoost Classifier**: Predicts high-risk leakage orders (defined as orders falling in the top 25% of leakage severity). Preprocessing is bundled *inside* the exported classifier pipeline to prevent serve-time training skew.
* **Isolation Forest Anomaly Detector**: Identifies outliers in price, freight ratios, and delay distributions to audit system anomalies.

---

## 6. Power BI CFO Dashboard Configuration

### Setup Instructions
1. Import `data/processed_fact_orders.csv` or connect directly to the MySQL/SQLite database.
2. Load/Create a Date table (`Calendar`) linked to `order_purchase_timestamp`.
3. Set the `Calendar` table as the Date Table.

### DAX Measures
Create the following measures in your Power BI model:

```dax
Total Revenue = SUM(fact_orders_leakage[total_price])

Total Leakage = SUM(fact_orders_leakage[leakage_amount])

Leakage % = DIVIDE([Total Leakage], [Total Revenue], 0)

Recovery Opportunity = [Total Leakage] * 0.5

Late Delivery Rate = 
DIVIDE(
    COUNTROWS(FILTER(fact_orders_leakage, fact_orders_leakage[is_late] = TRUE)),
    COUNTROWS(fact_orders_leakage)
)

MoM Leakage Change = 
VAR CurrentMonth = [Total Leakage]
VAR PrevMonth = CALCULATE([Total Leakage], DATEADD('Calendar'[Date], -1, MONTH))
RETURN DIVIDE(CurrentMonth - PrevMonth, PrevMonth, 0)
```

---

## 7. Streamlit Control Center

The application ([`streamlit/app.py`](file:///c:/Users/HP/Desktop/leakage%20Detection%20project/streamlit/app.py)) provides a dashboard visual interface for executive stakeholder check-ups:
* **Interactive KPIs & Plots**: Plotly charts visualizing trends, Pareto categorizations, and worst-performing sellers.
* **Live Sandbox Simulator**: A dynamic form permitting users to simulate single order data to receive live predictions on margin risk using the trained XGBoost model.

---

## 8. Local Setup & Execution Guide

### Prerequisites
* Python 3.10+
* Virtual Environment utility (`venv`)

### Setup Instructions

1. **Clone and navigate to repository**:
   ```bash
   cd Revenue-Leakage-Detection
   ```

2. **Initialize and activate virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute ETL & Database pipeline**:
   This extracts the raw Olist files, runs feature calculations, and loads records into `data/olist_leakage_db.db` (SQLite) or your configured MySQL server.
   ```bash
   python python/load_to_sql.py
   ```

5. **Train ML Models**:
   Run the Jupyter notebook to export the serializations:
   ```bash
   jupyter nbconvert --to notebook --execute --inplace notebooks/02_modeling.ipynb
   ```

6. **Launch Streamlit Dashboard**:
   ```bash
   streamlit run streamlit/app.py
   ```

---

## 9. Interview Talking Points (Resume Positioning)

If showcasing this project in technical interviews, focus on these engineering decisions to demonstrate professional senior analyst judgment:
* **Handling Missing Ground Truth (Proxy Logic)**: *"Olist didn't have a label for revenue leakage. I defined logical operational proxies—like late deliveries paired with low satisfaction reviews representing refund risks—and parameterized the weights (0.7, 0.2, 0.1 multipliers) so that business stakeholders could easily recalibrate the sensitivity."*
* **Production Pipeline Design**: *"I packaged the categorical encoder and StandardScaler directly inside the Scikit-learn ColumnTransformer and XGBoost pipeline before serialization. This prevents training-serving skew, meaning the Streamlit live predictor accepts raw dataframe inputs directly without duplicate encoding scripts."*
* **Fault-Tolerant ETL**: *"I engineered the load script to dynamically check for MySQL database availability. If the connection fails or credentials aren't provided, it automatically falls back to an SQLite file database, ensuring full system functionality on local staging environments."*
