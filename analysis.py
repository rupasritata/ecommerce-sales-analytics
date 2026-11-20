from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "ecommerce_sales.csv"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["order_date"])
df = df.drop_duplicates(subset=["order_id"])
df = df.dropna(subset=["order_date", "revenue", "profit"])
df["category"] = df["category"].fillna("Unknown")
df["region"] = df["region"].fillna("Unknown")

# Business sales KPIs use delivered orders only.
delivered = df[df["order_status"] == "Delivered"].copy()
revenue = delivered["revenue"].sum()
profit = delivered["profit"].sum()
orders = delivered["order_id"].nunique()
aov = revenue / orders if orders else 0

print("E-COMMERCE SALES SUMMARY")
print(f"Delivered revenue : ₹{revenue:,.2f}")
print(f"Delivered profit  : ₹{profit:,.2f}")
print(f"Delivered orders  : {orders:,}")
print(f"Average order value: ₹{aov:,.2f}")
print(f"Return rate       : {(df['order_status'].eq('Returned').mean()*100):.2f}%")

# Save a SQLite database for SQL practice.
db_path = OUTPUTS / "ecommerce_sales.db"
with sqlite3.connect(db_path) as conn:
    df.to_sql("sales", conn, if_exists="replace", index=False)
    query = """
        SELECT category,
               ROUND(SUM(revenue), 2) AS revenue,
               ROUND(SUM(profit), 2) AS profit,
               COUNT(DISTINCT order_id) AS orders
        FROM sales
        WHERE order_status = 'Delivered'
        GROUP BY category
        ORDER BY revenue DESC;
    """
    print("\\nCATEGORY PERFORMANCE")
    print(pd.read_sql_query(query, conn).to_string(index=False))

# Save a monthly revenue chart.
monthly = delivered.assign(month=delivered["order_date"].dt.to_period("M").astype(str))
monthly = monthly.groupby("month", as_index=False)["revenue"].sum()
plt.figure(figsize=(11, 5))
plt.plot(monthly["month"], monthly["revenue"], marker="o")
plt.title("Monthly Delivered Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig(OUTPUTS / "monthly_revenue.png", dpi=150)
plt.close()

print(f"\\nCreated SQLite database: {db_path}")
print(f"Created chart: {OUTPUTS / 'monthly_revenue.png'}")
