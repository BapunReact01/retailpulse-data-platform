-- Sales Overview Dashboard Query
-- Connect to warehouse database (retail_dw, port 5433)

-- Total Sales by Date
SELECT 
    DATE_TRUNC('day', fs.order_date) as date,
    SUM(fs.line_item_total) as total_sales,
    COUNT(DISTINCT fs.order_id) as total_orders,
    COUNT(DISTINCT fs.customer_key) as unique_customers,
    AVG(fs.line_item_total) as avg_order_value
FROM fact_sales fs
JOIN dim_dates dd ON fs.date_key = dd.date_key
GROUP BY DATE_TRUNC('day', fs.order_date)
ORDER BY date DESC;

-- Sales by Store
SELECT 
    ds.store_name,
    ds.city,
    SUM(fs.line_item_total) as total_sales,
    COUNT(DISTINCT fs.order_id) as total_orders,
    COUNT(DISTINCT fs.customer_key) as unique_customers
FROM fact_sales fs
JOIN dim_stores ds ON fs.store_key = ds.store_key
GROUP BY ds.store_name, ds.city
ORDER BY total_sales DESC;

-- Sales by Product Category
SELECT 
    dp.category,
    dp.subcategory,
    SUM(fs.quantity) as total_quantity_sold,
    SUM(fs.line_item_total) as total_revenue,
    AVG(fs.unit_price) as avg_price
FROM fact_sales fs
JOIN dim_products dp ON fs.product_key = dp.product_key
GROUP BY dp.category, dp.subcategory
ORDER BY total_revenue DESC;

-- Top 10 Products by Revenue
SELECT 
    dp.product_name,
    dp.brand,
    SUM(fs.line_item_total) as total_revenue,
    SUM(fs.quantity) as total_quantity_sold,
    COUNT(DISTINCT fs.order_id) as order_count
FROM fact_sales fs
JOIN dim_products dp ON fs.product_key = dp.product_key
GROUP BY dp.product_name, dp.brand
ORDER BY total_revenue DESC
LIMIT 10;