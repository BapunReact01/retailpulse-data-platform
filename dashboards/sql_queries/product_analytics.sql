-- Product Analytics Dashboard Query
-- Connect to warehouse database (retail_dw, port 5433)

-- Product Performance
SELECT 
    dp.product_name,
    dp.category,
    dp.subcategory,
    dp.brand,
    dp.unit_price,
    dp.cost_price,
    dp.profit_margin_pct,
    dp.is_profitable,
    SUM(fs.quantity) as total_quantity_sold,
    SUM(fs.line_item_total) as total_revenue,
    COUNT(DISTINCT fs.order_id) as order_count
FROM fact_sales fs
JOIN dim_products dp ON fs.product_key = dp.product_key
WHERE dp.expiry_date IS NULL
GROUP BY dp.product_name, dp.category, dp.subcategory, dp.brand, dp.unit_price, dp.cost_price, dp.profit_margin_pct, dp.is_profitable
ORDER BY total_revenue DESC;

-- Product Category Performance
SELECT 
    dp.category,
    COUNT(DISTINCT dp.product_key) as product_count,
    SUM(fs.quantity) as total_quantity_sold,
    SUM(fs.line_item_total) as total_revenue,
    AVG(dp.profit_margin_pct) as avg_profit_margin
FROM fact_sales fs
JOIN dim_products dp ON fs.product_key = dp.product_key
WHERE dp.expiry_date IS NULL
GROUP BY dp.category
ORDER BY total_revenue DESC;

-- Price Category Analysis
SELECT 
    dp.price_category,
    COUNT(DISTINCT dp.product_key) as product_count,
    SUM(fs.quantity) as total_quantity_sold,
    SUM(fs.line_item_total) as total_revenue,
    AVG(fs.unit_price) as avg_price
FROM fact_sales fs
JOIN dim_products dp ON fs.product_key = dp.product_key
WHERE dp.expiry_date IS NULL
GROUP BY dp.price_category
ORDER BY total_revenue DESC;

-- Low Margin Products (Alerts)
SELECT 
    dp.product_name,
    dp.brand,
    dp.profit_margin_pct,
    SUM(fs.line_item_total) as total_revenue
FROM fact_sales fs
JOIN dim_products dp ON fs.product_key = dp.product_key
WHERE dp.expiry_date IS NULL
GROUP BY dp.product_name, dp.brand, dp.profit_margin_pct
HAVING AVG(dp.profit_margin_pct) < 10
ORDER BY dp.profit_margin_pct ASC;