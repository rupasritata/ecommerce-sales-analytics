
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="📊",
    layout="wide"
)

DATA_PATH = Path(__file__).parent / "data" / "ecommerce_sales.csv"


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    data["order_date"] = pd.to_datetime(
        data["order_date"], errors="coerce"
    )

    data = data.drop_duplicates(subset=["order_id"])

    for col in ["category", "region", "order_status"]:
        data[col] = data[col].fillna("Unknown")

    numeric_cols = [
        "quantity", "unit_price", "discount_pct",
        "revenue", "cost", "profit"
    ]

    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    return data.dropna(
        subset=["order_date", "revenue", "profit"]
    )


df = load_data()

st.title("📊 E-Commerce Sales Analysis")
st.caption(
    "Interactive Business Intelligence Dashboard | Synthetic Practice Dataset"
)

# SIDEBAR FILTERS
with st.sidebar:
    st.header("Dashboard Filters")

    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()

    date_range = st.date_input(
        "Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    categories = st.multiselect(
        "Category",
        sorted(df["category"].unique()),
        default=sorted(df["category"].unique())
    )

    regions = st.multiselect(
        "Region",
        sorted(df["region"].unique()),
        default=sorted(df["region"].unique())
    )

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    df["order_date"].dt.date.between(start_date, end_date)
    & df["category"].isin(categories)
    & df["region"].isin(regions)
]

delivered = filtered[
    filtered["order_status"] == "Delivered"
]

# KPI CALCULATIONS
total_revenue = delivered["revenue"].sum()
total_profit = delivered["profit"].sum()
order_count = delivered["order_id"].nunique()

aov = (
    total_revenue / order_count
    if order_count else 0
)

return_rate = (
    filtered["order_status"].eq("Returned").mean() * 100
    if len(filtered) else 0
)

# KPI DASHBOARD
st.subheader("Performance Overview")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Delivered Revenue", f"₹{total_revenue:,.0f}")
k2.metric("Total Profit", f"₹{total_profit:,.0f}")
k3.metric("Delivered Orders", f"{order_count:,}")
k4.metric("Average Order Value", f"₹{aov:,.0f}")
k5.metric("Return Rate", f"{return_rate:.1f}%")

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

if delivered.empty:
    st.warning("No delivered orders match these filters.")

else:

    # MONTHLY REVENUE TREND
    st.divider()
    st.subheader("📈 Monthly Revenue Analysis")

    left, right = st.columns(2)

    with left:

        monthly = delivered.assign(
            month=delivered["order_date"].dt.to_period("M").astype(str)
        ).groupby(
            "month", as_index=False
        )["revenue"].sum()

        fig = px.line(
            monthly,
            x="month",
            y="revenue",
            markers=True,
            title="Monthly Revenue Trend"
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate=(
                "Month: %{x}<br>"
                "Revenue: ₹%{y:,.0f}<extra></extra>"
            )
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Revenue (₹)",
            yaxis_tickprefix="₹",
            yaxis_tickformat=",.0f",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

    # CATEGORY ANALYSIS
    with right:

        category_sales = delivered.groupby(
            "category", as_index=False
        )["revenue"].sum().sort_values(
            "revenue", ascending=False
        )

        fig = px.bar(
            category_sales,
            x="category",
            y="revenue",
            color="category",
            text_auto=",.2s",
            title="Revenue by Product Category"
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "Category: %{x}<br>"
                "Revenue: ₹%{y:,.0f}<extra></extra>"
            )
        )

        fig.update_layout(
            xaxis_title="Product Category",
            yaxis_title="Revenue (₹)",
            yaxis_tickprefix="₹",
            yaxis_tickformat=",.0f",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    # REGIONAL AND PRODUCT ANALYSIS
    st.divider()
    st.subheader("🌍 Regional & Product Performance")

    left, right = st.columns(2)

    with left:

        regional = delivered.groupby(
            "region", as_index=False
        ).agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum")
        )

        regional_long = regional.melt(
            id_vars="region",
            value_vars=["revenue", "profit"],
            var_name="metric",
            value_name="amount"
        )

        fig = px.bar(
            regional_long,
            x="region",
            y="amount",
            color="metric",
            barmode="group",
            text_auto=",.2s",
            title="Revenue and Profit by Region"
        )

        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Amount (₹)",
            yaxis_tickprefix="₹",
            yaxis_tickformat=",.0f"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        top_products = delivered.groupby(
            "product", as_index=False
        )["revenue"].sum().nlargest(
            10, "revenue"
        ).sort_values("revenue")

        fig = px.bar(
            top_products,
            x="revenue",
            y="product",
            orientation="h",
            text_auto=",.2s",
            title="Top 10 Products by Revenue"
        )

        fig.update_layout(
            xaxis_title="Revenue (₹)",
            yaxis_title="Product",
            xaxis_tickprefix="₹",
            xaxis_tickformat=",.0f"
        )

        st.plotly_chart(fig, use_container_width=True)

    # BUSINESS INSIGHTS
    st.divider()
    st.subheader("💡 Business Insights")

    category_insights = delivered.groupby(
        "category", as_index=False
    ).agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    ).sort_values("revenue", ascending=False)

    region_insights = delivered.groupby(
        "region", as_index=False
    ).agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    ).sort_values("revenue", ascending=False)

    product_insights = delivered.groupby(
        "product", as_index=False
    )["revenue"].sum().sort_values(
        "revenue", ascending=False
    )

    best_category = category_insights.iloc[0]
    best_region = region_insights.iloc[0]
    best_product = product_insights.iloc[0]

    profit_margin = (
        total_profit / total_revenue * 100
        if total_revenue else 0
    )

    category_share = (
        best_category["revenue"] / total_revenue * 100
        if total_revenue else 0
    )

    region_share = (
        best_region["revenue"] / total_revenue * 100
        if total_revenue else 0
    )

    c1, c2 = st.columns(2)

    with c1:
        st.success(
            f"🏆 Top Category: {best_category['category']}"
        )
        st.write(
            f"Revenue: ₹{best_category['revenue']:,.0f}"
        )
        st.write(
            f"Contribution: {category_share:.1f}%"
        )

        st.info(
            f"🌍 Best Region: {best_region['region']}"
        )
        st.write(
            f"Revenue: ₹{best_region['revenue']:,.0f}"
        )
        st.write(
            f"Contribution: {region_share:.1f}%"
        )

    with c2:
        st.success(
            f"⭐ Top Product: {best_product['product']}"
        )
        st.write(
            f"Revenue: ₹{best_product['revenue']:,.0f}"
        )

        st.info(
            f"📊 Overall Profit Margin: {profit_margin:.2f}%"
        )

    st.caption(
        "Business insights are calculated dynamically using the "
        "selected filters and synthetic practice data."
    )

# ORDER STATUS
st.divider()
st.subheader("📦 Order Status Breakdown")

status_counts = (
    filtered["order_status"]
    .value_counts()
    .rename_axis("status")
    .reset_index(name="orders")
)

fig = px.pie(
    status_counts,
    names="status",
    values="orders",
    hole=0.45,
    title="Order Status Distribution"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(fig, use_container_width=True)

# CUSTOMER ANALYSIS
st.subheader("👥 Customer Contribution")

customer_sales = delivered.groupby(
    "customer_id", as_index=False
).agg(
    orders=("order_id", "nunique"),
    revenue=("revenue", "sum"),
    profit=("profit", "sum")
).sort_values(
    "revenue", ascending=False
)

st.dataframe(
    customer_sales.head(10),
    use_container_width=True,
    hide_index=True
)

# TRANSACTION DATA
with st.expander("View Filtered Transaction Data"):

    st.dataframe(
        filtered.sort_values(
            "order_date", ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Filtered CSV",
        filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_ecommerce_sales.csv",
        mime="text/csv"
    )

# DATA DISCLAIMER
st.info(
    "Dataset Disclaimer: This project uses simulated e-commerce "
    "data for educational and portfolio purposes. All insights "
    "and business metrics are based on sample transactions."
)
