-- RetailPulse Data Warehouse - Star Schema
-- This script creates dimension and fact tables for the data warehouse

-- ============================================
-- DIMENSION TABLES
-- ============================================

-- Dimension: Customers
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50) DEFAULT 'India',
    postal_code VARCHAR(20),
    registration_date DATE NOT NULL,
    customer_segment VARCHAR(20) CHECK (customer_segment IN ('premium', 'regular', 'new')),
    customer_tier VARCHAR(20) CHECK (customer_tier IN ('gold', 'silver', 'bronze')),
    loyalty_score INTEGER,
    days_as_customer INTEGER,
    customer_lifetime_value DECIMAL(15, 2),
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    expiry_date DATE
);

CREATE INDEX idx_dim_customers_id ON dim_customers(customer_id);
CREATE INDEX idx_dim_customers_segment ON dim_customers(customer_segment);
CREATE INDEX idx_dim_customers_tier ON dim_customers(customer_tier);

-- Dimension: Products
CREATE TABLE IF NOT EXISTS dim_products (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL UNIQUE,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),
    brand VARCHAR(100),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0),
    cost_price DECIMAL(10, 2) NOT NULL CHECK (cost_price > 0),
    launch_date DATE,
    is_active BOOLEAN DEFAULT true,
    price_category VARCHAR(20),
    profit_margin_pct DECIMAL(10, 2),
    is_profitable BOOLEAN,
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    expiry_date DATE
);

CREATE INDEX idx_dim_products_id ON dim_products(product_id);
CREATE INDEX idx_dim_products_category ON dim_products(category);
CREATE INDEX idx_dim_products_brand ON dim_products(brand);

-- Dimension: Stores
CREATE TABLE IF NOT EXISTS dim_stores (
    store_key SERIAL PRIMARY KEY,
    store_id VARCHAR(20) NOT NULL UNIQUE,
    store_name VARCHAR(200) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50),
    country VARCHAR(50) DEFAULT 'India',
    store_type VARCHAR(20) CHECK (store_type IN ('flagship', 'regular', 'online')),
    opening_date DATE,
    manager_name VARCHAR(100),
    store_size_sqft INTEGER,
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    expiry_date DATE
);

CREATE INDEX idx_dim_stores_id ON dim_stores(store_id);
CREATE INDEX idx_dim_stores_city ON dim_stores(city);
CREATE INDEX idx_stores_type ON dim_stores(store_type);

-- Dimension: Dates
CREATE TABLE IF NOT EXISTS dim_dates (
    date_key INTEGER PRIMARY KEY,
    date_value DATE NOT NULL UNIQUE,
    day_of_week INTEGER,
    day_of_month INTEGER,
    day_of_year INTEGER,
    week_of_year INTEGER,
    month INTEGER,
    quarter INTEGER,
    year INTEGER,
    is_holiday BOOLEAN DEFAULT false,
    is_weekend BOOLEAN DEFAULT false,
    month_name VARCHAR(20),
    day_name VARCHAR(20)
);

CREATE INDEX idx_dim_dates_value ON dim_dates(date_value);
CREATE INDEX idx_dim_dates_year_month ON dim_dates(year, month);

-- ============================================
-- FACT TABLES
-- ============================================

-- Fact: Sales
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key SERIAL PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    customer_key INTEGER NOT NULL REFERENCES dim_customers(customer_key),
    product_key INTEGER NOT NULL REFERENCES dim_products(product_key),
    store_key INTEGER NOT NULL REFERENCES dim_stores(store_key),
    date_key INTEGER NOT NULL REFERENCES dim_dates(date_key),
    line_item_id VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0,
    line_item_total DECIMAL(12, 2) NOT NULL,
    effective_price DECIMAL(10, 2),
    total_amount DECIMAL(12, 2) NOT NULL,
    order_value_category VARCHAR(20),
    payment_method VARCHAR(20),
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50) DEFAULT 'silver_sales'
);

CREATE INDEX idx_fact_sales_order ON fact_sales(order_id);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_store ON fact_sales(store_key);
CREATE INDEX idx_fact_sales_date ON fact_sales(date_key);

-- Fact: Returns
CREATE TABLE IF NOT EXISTS fact_returns (
    return_key SERIAL PRIMARY KEY,
    return_id VARCHAR(20) NOT NULL,
    customer_key INTEGER NOT NULL REFERENCES dim_customers(customer_key),
    product_key INTEGER NOT NULL REFERENCES dim_products(product_key),
    store_key INTEGER NOT NULL REFERENCES dim_stores(store_key),
    date_key INTEGER NOT NULL REFERENCES dim_dates(date_key),
    return_date DATE NOT NULL,
    reason VARCHAR(50),
    refund_amount DECIMAL(12, 2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('approved', 'pending', 'rejected')),
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50) DEFAULT 'raw_returns'
);

CREATE INDEX idx_fact_returns_id ON fact_returns(return_id);
CREATE INDEX idx_fact_returns_customer ON fact_returns(customer_key);
CREATE INDEX idx_fact_returns_product ON fact_returns(product_key);
CREATE INDEX idx_fact_returns_date ON fact_returns(date_key);