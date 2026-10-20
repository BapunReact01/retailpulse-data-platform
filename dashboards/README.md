# RetailPulse - Power BI Dashboard Guide

This directory contains SQL queries for Power BI dashboards connecting to the RetailPulse data warehouse.

## Database Connection

**Database:** retail_dw  
**Host:** localhost  
**Port:** 5433  
**User:** retail_user  
**Password:** (from .env file)

## Available SQL Queries

### 1. Sales Overview (`sales_overview.sql`)
- Total sales by date
- Sales by store
- Sales by product category
- Top 10 products by revenue

### 2. Customer Analytics (`customer_analytics.sql`)
- Customer segmentation
- Monthly active customers
- Top customers by revenue
- Customer geographic distribution

### 3. Product Analytics (`product_analytics.sql`)
- Product performance
- Product category performance
- Price category analysis
- Low margin products (alerts)

## How to Connect Power BI

1. Open Power BI Desktop
2. Click "Get Data" → "Database" → "PostgreSQL"
3. Enter connection details:
   - Server: localhost
   - Database: retail_dw
   - Port: 5433
   - User: retail_user
   - Password: (from .env)
4. Click "Connect"
5. Click "Transform Data" to paste SQL queries
6. Or use "Direct Query" for each SQL file

## Dashboard Ideas

### Sales Dashboard
- Daily sales trend
- Sales by store (map)
- Sales by category (bar chart)
- Top products (table)

### Customer Dashboard
- Customer segments (pie chart)
- Customer retention (line chart)
- Top customers (bar chart)
- Geographic distribution (map)

### Product Dashboard
- Product performance (table)
- Category performance (bar chart)
- Price category analysis (donut chart)
- Low margin alerts (table)

## Notes

- The fact and dimension tables are in Star Schema format
- Use `expiry_date IS NULL` to get current active records
- All monetary values are in local currency
- Dates are in YYYY-MM-DD format