import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Nova Financial Analytics Platform",
    page_icon="📊",
    layout="wide"
)

customers = pd.read_csv("data/nova_financial_customers.csv")
plan_summary = pd.read_csv("data/plan_summary.csv")
country_summary = pd.read_csv("data/country_summary.csv")

st.sidebar.title("Dashboard Filters")

st.sidebar.markdown("---")

st.sidebar.markdown(
"""
### About

Explore customer behaviour across different markets and subscription plans.

Use the filters below to interact with the dashboard.
"""
)

st.sidebar.markdown("---")

selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=sorted(customers["country"].unique()),
    default=sorted(customers["country"].unique())
)

selected_plans = st.sidebar.multiselect(
    "Select subscription plans",
    options=sorted(customers["plan"].unique()),
    default=sorted(customers["plan"].unique())
)

customers = customers[
    (customers["country"].isin(selected_countries)) &
    (customers["plan"].isin(selected_plans))
]

plan_summary = customers.groupby("plan").agg(
    customers=("customer_id", "count"),
    revenue=("monthly_revenue", "sum"),
    avg_revenue=("monthly_revenue", "mean"),
    churn_rate=("churned", "mean")
).reset_index()

plan_summary["churn_rate"] = plan_summary["churn_rate"] * 100

country_summary = customers.groupby("country").agg(
    customers=("customer_id", "count"),
    revenue=("monthly_revenue", "sum"),
    avg_revenue=("monthly_revenue", "mean"),
    churn_rate=("churned", "mean"),
    failed_payments=("failed_payments", "sum")
).reset_index()

country_summary["churn_rate"] = country_summary["churn_rate"] * 100
st.title("📊 Nova Financial Analytics Platform")

st.caption(
    "Business Intelligence Dashboard | Python • Pandas • Plotly • Streamlit"
)

st.write(
    """
Interactive analytics platform for a simulated global digital financial services company.
The dashboard enables exploration of customer behaviour, revenue drivers,
operational performance and strategic business insights.
"""
)

total_customers = len(customers)
total_revenue = customers["monthly_revenue"].sum()
avg_revenue = customers["monthly_revenue"].mean()
churn_rate = customers["churned"].mean() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

col2.metric(
    "💰 Monthly Revenue",
    f"£{total_revenue:,.0f}"
)

col3.metric(
    "📈 Revenue / Customer",
    f"£{avg_revenue:.2f}"
)

col4.metric(
    "⚠️ Churn Rate",
    f"{churn_rate:.1f}%"
)

st.divider()

st.header("📈 Revenue Analytics")
st.subheader("Revenue by Subscription Plan")
fig_plan = px.bar(
    plan_summary,
    x="plan",
    y="revenue",
    text_auto=True,
    title="Monthly Revenue by Plan"
)

st.plotly_chart(fig_plan, use_container_width=True)

st.header("🌍 Geographic Performance")
st.subheader("Revenue by Country")
fig_country = px.bar(
    country_summary.sort_values("revenue", ascending=False),
    x="country",
    y="revenue",
    text_auto=True,
    title="Monthly Revenue by Country"
)
st.plotly_chart(fig_country, use_container_width=True)

segment_summary = pd.read_csv("data/segment_summary.csv")

st.header("👥 Customer Segmentation")

fig_segment = px.bar(
    segment_summary,
    x="age_group",
    y="revenue",
    color="age_group",
    title="Revenue by Age Group",
    text_auto=True
)

st.plotly_chart(fig_segment, use_container_width=True)

st.header("Customer Retention")
st.subheader("Churn by Subscription Plan")
churn_by_plan = customers.groupby("plan")["churned"].mean().reset_index()
churn_by_plan["churn_rate"] = churn_by_plan["churned"] * 100

fig_churn = px.bar(
    churn_by_plan,
    x="plan",
    y="churn_rate",
    text_auto=".1f",
    title="Churn Rate by Plan (%)"
)
st.plotly_chart(fig_churn, use_container_width=True)

st.divider()

st.divider()

st.header("📋 Executive Summary")

top_plan = plan_summary.sort_values("revenue", ascending=False).iloc[0]
highest_arpu_country = country_summary.sort_values("avg_revenue", ascending=False).iloc[0]
highest_churn_plan = churn_by_plan.sort_values("churn_rate", ascending=False).iloc[0]
highest_failed_country = country_summary.sort_values("failed_payments", ascending=False).iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.success(
        f"""
### 💰 Revenue

**Top Subscription:** {top_plan['plan']}

Monthly Revenue

**£{top_plan['revenue']:,.0f}**
"""
    )

    st.info(
        f"""
### 🌍 Highest Value Market

**{highest_arpu_country['country']}**

Average Revenue per Customer

**£{highest_arpu_country['avg_revenue']:.2f}**
"""
    )

with col2:

    st.warning(
        f"""
### ⚠ Highest Churn

**{highest_churn_plan['plan']}**

Churn Rate

**{highest_churn_plan['churn_rate']:.1f}%**
"""
    )

    st.error(
        f"""
### 🚨 Operational Risk

**{highest_failed_country['country']}**

Failed Payments

**{highest_failed_country['failed_payments']:,.0f}**
"""
    )

st.divider()

st.header("🎯 Strategic Recommendations")

st.markdown(f"""
### Immediate Actions

- Increase conversion towards **{top_plan['plan']}**, the highest revenue subscription.

- Investigate why **{highest_churn_plan['plan']}** customers leave more frequently.

- Reduce payment failures within **{highest_failed_country['country']}**.

- Study customer behaviour in **{highest_arpu_country['country']}** to replicate success in other markets.
""")
st.divider()

st.header("📊 Scenario Simulator")

st.write(
    "Estimate how changes in paid-plan conversion and churn could affect monthly revenue."
)

conversion_uplift = st.slider(
    "Paid-plan conversion uplift (%)",
    min_value=0,
    max_value=20,
    value=5
)

churn_reduction = st.slider(
    "Churn reduction (%)",
    min_value=0,
    max_value=20,
    value=5
)

paid_revenue = customers[customers["is_paid_plan"]]["monthly_revenue"].mean()
basic_revenue = customers[~customers["is_paid_plan"]]["monthly_revenue"].mean()

extra_paid_users = total_customers * (conversion_uplift / 100)
estimated_extra_revenue = extra_paid_users * (paid_revenue - basic_revenue)

retained_users = total_customers * (churn_rate / 100) * (churn_reduction / 100)
estimated_retention_revenue = retained_users * avg_revenue

estimated_new_revenue = total_revenue + estimated_extra_revenue + estimated_retention_revenue

col1, col2, col3 = st.columns(3)

col1.metric("Current Monthly Revenue", f"£{total_revenue:,.0f}")
col2.metric("Estimated Monthly Revenue", f"£{estimated_new_revenue:,.0f}")
col3.metric("Potential Monthly Uplift", f"£{estimated_new_revenue - total_revenue:,.0f}")

st.markdown(
    f"""
### Scenario Interpretation

If paid-plan conversion increases by **{conversion_uplift}%** and churn is reduced by **{churn_reduction}%**, estimated monthly revenue could rise by approximately **£{estimated_new_revenue - total_revenue:,.0f}**.
"""
)