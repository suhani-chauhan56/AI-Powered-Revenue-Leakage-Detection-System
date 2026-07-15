-- 1. Total leakage by reason
SELECT leakage_reason,
       ROUND(SUM(leakage_amount),2) AS total_leakage,
       COUNT(*) AS affected_orders
FROM fact_orders_leakage
WHERE leakage_reason != 'None'
GROUP BY leakage_reason
ORDER BY total_leakage DESC;

-- 2. Monthly leakage trend with window functions
WITH monthly AS (
    SELECT order_month,
           SUM(leakage_amount) AS monthly_leakage
    FROM fact_orders_leakage
    GROUP BY order_month
)
SELECT order_month,
       ROUND(monthly_leakage, 2) AS monthly_leakage,
       ROUND(SUM(monthly_leakage) OVER (ORDER BY order_month), 2) AS cumulative_leakage,
       ROUND(monthly_leakage - LAG(monthly_leakage) OVER (ORDER BY order_month), 2) AS mom_change
FROM monthly
ORDER BY order_month;

-- 3. Worst sellers (ranked)
SELECT seller_id,
       ROUND(SUM(leakage_amount),2) AS total_leakage,
       COUNT(*) AS orders,
       RANK() OVER (ORDER BY SUM(leakage_amount) DESC) AS leakage_rank
FROM fact_orders_leakage
GROUP BY seller_id
ORDER BY total_leakage DESC
LIMIT 10;

-- 4. Category-level leakage
SELECT product_category_name_english,
       ROUND(SUM(leakage_amount),2) AS total_leakage,
       ROUND(AVG(freight_ratio),3) AS avg_freight_ratio
FROM fact_orders_leakage
GROUP BY product_category_name_english
ORDER BY total_leakage DESC
LIMIT 10;

-- 5. Delivery funnel
SELECT
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END) AS delivered,
    SUM(CASE WHEN is_late THEN 1 ELSE 0 END) AS late_deliveries,
    SUM(CASE WHEN is_cancelled THEN 1 ELSE 0 END) AS cancelled
FROM fact_orders_leakage;
