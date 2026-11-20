# E-Commerce Sales Analysis & Business Intelligence

A portfolio-ready Data Analyst project using **Python, Pandas, SQL, and Streamlit**. It analyzes e-commerce transactions and presents business KPIs, sales trends, category performance, regional performance, and customer insights.

> **Dataset note:** `data/ecommerce_sales.csv` is a reproducible, synthetic practice dataset created for this portfolio project. It is not real company or customer data. Do not describe it as real business data in an interview.

## Project objectives
- Clean and validate transaction data.
- Measure revenue, profit, orders, average order value (AOV), and return/cancellation rates.
- Identify top-performing categories, products, and regions.
- Examine monthly sales trends and customer purchasing behavior.
- Communicate findings through an interactive dashboard.

## Tech stack
- Python 3.10+
- Pandas and NumPy
- SQLite and SQL
- Streamlit and Plotly

## Folder structure
```text
ecommerce-sales-analytics/
├── app.py
├── analysis.py
├── generate_data.py
├── requirements.txt
├── README.md
├── data/
│   └── ecommerce_sales.csv
├── sql/
│   └── analysis_queries.sql
└── outputs/
    └── (generated charts and database)
```

## Run locally
1. Install Python 3.10 or later.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```
6. Optional: generate the SQLite database and static charts:
   ```bash
   python analysis.py
   ```

## Dashboard features
- KPI cards for revenue, profit, delivered orders, and average order value.
- Date, category, and region filters.
- Monthly revenue trend.
- Revenue and profit by category.
- Regional sales comparison.
- Top products and customer contribution.

## Key business definitions
- **Revenue:** Sum of net transaction revenue for delivered orders.
- **Profit:** Sum of revenue minus recorded cost for delivered orders.
- **AOV:** Delivered revenue divided by delivered order count.
- **Return rate:** Returned orders divided by all orders.
- **Cancellation rate:** Cancelled orders divided by all orders.

## Data quality approach
The app parses dates, removes duplicate order IDs, handles missing values in key dimensions, and excludes non-delivered orders from sales KPIs while retaining them for order-status analysis.

## Suggested GitHub description
Interactive e-commerce sales analytics dashboard built with Python, Pandas, SQL, and Streamlit. Includes data cleaning, KPI analysis, trend analysis, and business insights using a clearly labelled synthetic dataset.

## Interview explanation (short)
"I built an E-Commerce Sales Analysis dashboard to understand sales and profitability across products, categories, regions, and time. I used Python and Pandas to clean and analyze the data, SQL to perform aggregations and ranking, and Streamlit with Plotly to present interactive KPIs and charts. The project helps identify high-performing categories, regional trends, and areas that may need attention. The included dataset is synthetic, so the project demonstrates the analytical workflow rather than claiming real company findings."

## Before publishing
- Replace the sample dataset with a public dataset if you want to demonstrate analysis on real-world sourced data; cite its source and license.
- Add screenshots of your running dashboard to the repository.
- Be ready to explain the data, metric definitions, SQL queries, and limitations.
