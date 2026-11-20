-- E-Commerce Sales Analysis SQL Practice
-- Table: sales
-- Business KPIs below use delivered orders unless stated otherwise.

-- 1. Total revenue, profit, and delivered orders
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales
WHERE order_status = 'Delivered';

-- 2. Monthly revenue trend
SELECT
    strftime('%Y-%m', order_date) AS sales_month,
    ROUND(SUM(revenue), 2) AS monthly_revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY strftime('%Y-%m', order_date)
ORDER BY sales_month;

-- 3. Category-wise performance
SELECT
    category,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM sales
WHERE order_status = 'Delivered'
GROUP BY category
ORDER BY revenue DESC;

-- 4. Top 10 products by revenue
SELECT
    product,
    ROUND(SUM(revenue), 2) AS revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY product
ORDER BY revenue DESC
LIMIT 10;

-- 5. Regional performance
SELECT
    region,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    COUNT(DISTINCT order_id) AS orders
FROM sales
WHERE order_status = 'Delivered'
GROUP BY region
ORDER BY revenue DESC;

-- 6. Customer ranking using a window function
WITH customer_summary AS (
    SELECT
        customer_id,
        ROUND(SUM(revenue), 2) AS customer_revenue,
        COUNT(DISTINCT order_id) AS order_count
    FROM sales
    WHERE order_status = 'Delivered'
    GROUP BY customer_id
)
SELECT
    customer_id,
    customer_revenue,
    order_count,
    DENSE_RANK() OVER (ORDER BY customer_revenue DESC) AS customer_rank
FROM customer_summary
ORDER BY customer_rank
LIMIT 10;

-- 7. Order status distribution (all orders)
SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sales), 2) AS percentage
FROM sales
GROUP BY order_status
ORDER BY order_count DESC;

-- 8. Average order value
SELECT
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM sales
WHERE order_status = 'Delivered';
