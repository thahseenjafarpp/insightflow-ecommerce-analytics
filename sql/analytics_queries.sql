-- =========================================================
-- InsightFlow - E-Commerce SQL Analytics
-- =========================================================


-- 1. Total number of orders
SELECT COUNT(*) AS total_orders
FROM orders;


-- 2. Total number of customers
SELECT COUNT(*) AS total_customers
FROM customers;


-- 3. Orders by status
SELECT
    order_status,
    COUNT(*) AS order_count
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;


-- 4. Total sales revenue
SELECT
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items;


-- 5. Total freight revenue
SELECT
    ROUND(SUM(freight_value), 2) AS total_freight
FROM order_items;


-- 6. Average order value
SELECT
    ROUND(SUM(price) / COUNT(DISTINCT order_id), 2)
        AS average_order_value
FROM order_items;


-- 7. Revenue by product category
SELECT
    p.product_category_name,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY revenue DESC;


-- 8. Top 10 products by revenue
SELECT
    oi.product_id,
    ROUND(SUM(oi.price), 2) AS revenue
FROM order_items oi
GROUP BY oi.product_id
ORDER BY revenue DESC
LIMIT 10;


-- 9. Orders by customer state
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY total_orders DESC;


-- 10. Revenue by customer state
SELECT
    c.customer_state,
    ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY revenue DESC;


-- 11. Monthly order trend
SELECT
    purchase_year,
    purchase_month,
    COUNT(*) AS total_orders
FROM orders
GROUP BY purchase_year, purchase_month
ORDER BY purchase_year, purchase_month;


-- 12. Delivered vs non-delivered orders
SELECT
    CASE
        WHEN order_status = 'delivered'
            THEN 'Delivered'
        ELSE 'Not Delivered'
    END AS delivery_group,
    COUNT(*) AS order_count
FROM orders
GROUP BY delivery_group;


-- 13. Average delivery time
SELECT
    ROUND(AVG(delivery_time_days), 2)
        AS average_delivery_days
FROM orders
WHERE delivery_time_days IS NOT NULL;


-- 14. Top sellers by revenue
SELECT
    seller_id,
    ROUND(SUM(price), 2) AS revenue
FROM order_items
GROUP BY seller_id
ORDER BY revenue DESC
LIMIT 10;


-- 15. Payment type distribution
SELECT
    payment_type,
    COUNT(*) AS payment_count,
    ROUND(SUM(payment_value), 2) AS total_payment
FROM payments
GROUP BY payment_type
ORDER BY total_payment DESC;


-- =========================================================
-- ADVANCED SQL ANALYTICS
-- =========================================================


-- 16. Top 5 product categories by revenue using a CTE
WITH category_revenue AS (
    SELECT
        p.product_category_name,
        SUM(oi.price) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_category_name
)
SELECT
    product_category_name,
    ROUND(revenue, 2) AS revenue
FROM category_revenue
ORDER BY revenue DESC
LIMIT 5;


-- 17. Customers with more than one order
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS order_count
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
HAVING COUNT(DISTINCT o.order_id) > 1
ORDER BY order_count DESC
LIMIT 10;


-- 18. Products earning more than the average product revenue
SELECT
    product_id,
    ROUND(SUM(price), 2) AS product_revenue
FROM order_items
GROUP BY product_id
HAVING SUM(price) > (
    SELECT AVG(product_revenue)
    FROM (
        SELECT SUM(price) AS product_revenue
        FROM order_items
        GROUP BY product_id
    ) AS product_totals
)
ORDER BY product_revenue DESC
LIMIT 10;


-- 19. Monthly revenue using a CTE
WITH monthly_revenue AS (
    SELECT
        o.purchase_year,
        o.purchase_month,
        SUM(oi.price) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.purchase_year,
        o.purchase_month
)
SELECT
    purchase_year,
    purchase_month,
    ROUND(revenue, 2) AS revenue
FROM monthly_revenue
ORDER BY purchase_year, purchase_month;


-- 20. Rank sellers by revenue using a window function
WITH seller_revenue AS (
    SELECT
        seller_id,
        SUM(price) AS revenue
    FROM order_items
    GROUP BY seller_id
)
SELECT
    seller_id,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM seller_revenue
ORDER BY revenue_rank
LIMIT 10;


-- 21. Rank categories by revenue within the dataset
WITH category_revenue AS (
    SELECT
        p.product_category_name,
        SUM(oi.price) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_category_name
)
SELECT
    product_category_name,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (ORDER BY revenue DESC) AS category_rank
FROM category_revenue
ORDER BY category_rank;


-- 22. Average order value by customer state
SELECT
    c.customer_state,
    ROUND(
        SUM(oi.price) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY average_order_value DESC
LIMIT 10;


-- 23. Orders that took longer than the average delivery time
SELECT
    order_id,
    customer_id,
    ROUND(delivery_time_days, 2) AS delivery_time_days
FROM orders
WHERE delivery_time_days > (
    SELECT AVG(delivery_time_days)
    FROM orders
    WHERE delivery_time_days IS NOT NULL
)
ORDER BY delivery_time_days DESC
LIMIT 10;


-- 24. Customer order frequency classification
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
)
SELECT
    customer_unique_id,
    order_count,
    CASE
        WHEN order_count = 1 THEN 'One-time customer'
        WHEN order_count BETWEEN 2 AND 3 THEN 'Repeat customer'
        ELSE 'Frequent customer'
    END AS customer_segment
FROM customer_orders
ORDER BY order_count DESC
LIMIT 20;


-- 25. Revenue contribution percentage by category
WITH category_revenue AS (
    SELECT
        p.product_category_name,
        SUM(oi.price) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.product_category_name
)
SELECT
    product_category_name,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        100 * revenue / SUM(revenue) OVER (),
        2
    ) AS revenue_percentage
FROM category_revenue
ORDER BY revenue DESC;



-- =========================================================
-- KEY BUSINESS INSIGHTS
-- =========================================================

-- 1. Total orders and customers
-- 99K+ orders and customers were analyzed across the dataset.

-- 2. Order fulfillment
-- Delivered orders represent the dominant share of total orders.

-- 3. Revenue performance
-- Total product revenue exceeds 13.5M based on order-item prices.

-- 4. Delivery performance
-- Average delivery time is approximately 12.56 days.

-- 5. Regional performance
-- Sao Paulo (SP) leads both order volume and revenue among customer states.

-- 6. Category performance
-- Beauty & Health is the leading product category by revenue.

-- 7. Payment behavior
-- Credit card is the dominant payment method by transaction volume and payment value.

-- 8. Customer behavior
-- Customer segmentation identifies one-time, repeat, and frequent customers.

-- 9. Seller performance
-- Seller rankings highlight the highest-revenue sellers for performance comparison.

-- 10. Revenue concentration
-- Category revenue contribution percentages identify the categories
-- responsible for the largest shares of overall product revenue.