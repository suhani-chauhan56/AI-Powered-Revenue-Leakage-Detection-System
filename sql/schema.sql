CREATE DATABASE IF NOT EXISTS olist_leakage_db;
USE olist_leakage_db;

CREATE TABLE IF NOT EXISTS fact_orders_leakage (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    seller_id VARCHAR(50),
    product_category_name_english VARCHAR(100),
    order_status VARCHAR(20),
    order_purchase_timestamp DATETIME,
    order_estimated_delivery_date DATETIME,
    order_delivered_customer_date DATETIME,
    total_price DECIMAL(12,2),
    total_freight DECIMAL(12,2),
    review_score INT,
    is_cancelled BOOLEAN,
    is_late BOOLEAN,
    delay_days INT,
    freight_ratio DECIMAL(6,3),
    leakage_amount DECIMAL(12,2),
    leakage_reason VARCHAR(50),
    order_month VARCHAR(10)
);
