-- Customer Analytics Dashboard Query
-- Connect to warehouse database (retail_dw, port 5433)

-- Customer Segmentation
SELECT 
    dc.customer_segment,
    dc.customer_tier,
    COUNT(DISTINCT dc.customer_key) as customer_count,
    SUM(dc.customer_lifetime_value) as total_clv,
    AVG(dc.days_as_customer) as avg_days_as_customer
FROM dim_customers dc
WHERE dc.expiry_date IS NULL
GROUP BY dc.customer_segment, dc.customer_tier
ORDER BY total_clv DESC;

-- Customer RFM Analysis (from Gold layer if loaded)
-- Monthly Active Customers
SELECT 
    DATE_TRUNC('month', fs.order_date) as month,
    COUNT(DISTINCT fs.customer_key) as active_customers,
    SUM(fs.line_item_total) as monthly_revenue,
    AVG(fs.line_item_total) as avg_monthly_spend
FROM fact_sales fs
JOIN dim_dates dd ON fs.date_key = dd.date_key
GROUP BY DATE_TRUNC('month', fs.order_date)
ORDER BY month DESC;

-- Top Customers by Revenue
SELECT 
    dc.first_name,
    dc.last_name,
    dc.email,
    dc.city,
    SUM(fs.line_item_total) as total_revenue,
    COUNT(DISTINCT fs.order_id) as total_orders,
    AVG(fs.line_item_total) as avg_order_value
FROM fact_sales fs
JOIN dim_customers dc ON fs.customer_key = dc.customer_key
WHERE dc.expiry_date IS NULL
GROUP BY dc.first_name, dc.last_name, dc.email, dc.city
ORDER BY total_revenue DESC
LIMIT 10;

-- Customer Geographic Distribution
SELECT 
    dc.city,
    dc.state,
    COUNT(DISTINCT dc.customer_key) as customer_count,
    SUM(dc.customer_lifetime_value) as total_clv
FROM dim_customers dc
WHERE dc.expiry_date IS NULL
GROUP BY dc.city, dc.state
ORDER BY customer_count DESC;