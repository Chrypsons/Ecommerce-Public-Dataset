import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

#data
all_df = pd.read_csv("Dashboard\\all_data.csv")
datetime_cols = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "shipping_limit_date"]
for column in datetime_cols:
    all_df[column] = pd.to_datetime(all_df[column])

best_products = pd.read_csv("Dashboard\\best_products.csv")
worst_products = pd.read_csv("Dashboard\\worst_products.csv")
customer_by_city = pd.read_csv("Dashboard\\customer_by_city.csv")
customer_by_state = pd.read_csv("Dashboard\\customer_by_state.csv")
monthly_orders = pd.read_csv("Dashboard\\monthly_orders.csv").sort_values(by="order_approved_at")
order_by_order_status = pd.read_csv("Dashboard\\order_by_order_status.csv")
order_reviews_score = pd.read_csv("Dashboard\\order_reviews_score.csv")
rfm_df = pd.read_csv("Dashboard\\rfm_df.csv")

# Helper function
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule="D", on="order_approved_at").agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    return daily_orders_df

def create_sum_spend_df(df):
    sum_spend_df = df.resample(rule="D", on="order_approved_at").agg({
        "payment_value": "sum"
    })
    sum_spend_df = sum_spend_df.reset_index()
    sum_spend_df.rename(columns={
        "payment_value": "total_spend"
    }, inplace=True)
    return sum_spend_df

daily_orders_df = create_daily_orders_df(all_df)
sum_spend_df = create_sum_spend_df(all_df)

st.header("Data Analysis Project: Brazilian E-Commerce Public Dataset")

col1, col2 = st.columns(2)
with col1:
    total_order = daily_orders_df.order_count.sum()
    st.metric("Total Orders", value=total_order)

with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "BRL", locale="pt_BR")
    st.metric("Total Revenue", value=total_revenue)

st.subheader("Sales Performance by Month")
fig, ax = plt.subplots(figsize=(16, 8))
ax.set_facecolor("white")
plt.plot(
    monthly_orders.order_approved_at,
    monthly_orders.order_id,
    marker="o",
    linewidth=3,
    color="darkblue"
)
plt.xticks(rotation=45)

st.pyplot(fig)

st.subheader("Most and Least Ordered Products")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["darkblue", "lightgrey", "lightgrey", "lightgrey", "lightgrey"]

sns.barplot(
    x="order_id",
    y="product_category_name_english",
    data=best_products,
    ax=ax[0],
    palette=colors,
    hue="product_category_name_english"
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_facecolor("white")
ax[0].set_title("Most Ordered Products", fontsize=20)
ax[0].tick_params(axis='y', labelsize=15)

sns.barplot(
    x="order_id",
    y="product_category_name_english",
    data=worst_products,
    ax=ax[1],
    palette=colors,
    hue="product_category_name_english"
)
ax[1].invert_xaxis()
ax[1].set_facecolor("white")
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Least Ordered Products", fontsize=20)
ax[1].tick_params(axis='y', labelsize=15)

st.pyplot(fig)

st.subheader("Customer Demographics")
fig, ax = plt.subplots(figsize=(16, 8))
ax.set_facecolor("white")
colors = ["darkblue", "lightgrey", "lightgrey", "lightgrey", "lightgrey", "lightgrey", "lightgrey", "lightgrey", "lightgrey", "lightgrey"]

sns.barplot(
    y="count",
    x="customer_state",
    data=customer_by_state.head(10),
    palette=colors,
    hue="customer_state"
)
plt.ylabel(None)
plt.xlabel(None)
plt.title("Customer Demographics by State", fontsize=20)
plt.xticks(fontsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_facecolor("white")
sns.barplot(
    y="count",
    x="customer_city",
    data=customer_by_city.head(10),
    palette=colors,
    hue="customer_city"
)
plt.ylabel(None)
plt.xlabel(None)
plt.title("Customer Demographics by City", fontsize=18)
plt.xticks(rotation=45, fontsize=10)

st.pyplot(fig)

st.subheader("Score Review Distribution")
fig, ax = plt.subplots(figsize=(16, 8))
ax.set_facecolor("white")
colors = ["lightgrey", "lightgrey", "lightgrey", "lightgrey", "darkblue"]

sns.barplot(
    y="count",
    x="review_score",
    data=order_reviews_score,
    palette=colors,
    hue="review_score",
    legend=False
)
plt.ylabel(None)
plt.xlabel("Score Review", fontsize=17)
st.pyplot(fig)

st.subheader("Best Customer Based on RFM Parameters")
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["darkblue", "lightgrey", "lightgrey", "lightgrey", "lightgrey"]

sns.barplot(
    y="recency",
    x="customer_id",
    data=rfm_df.sort_values(by="recency", ascending=True).head(),
    palette=colors,
    ax=ax[0],
    hue="customer_id"
)

ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_facecolor("white")
ax[0].set_title("By Recency (days)", fontsize=25)
ax[0].tick_params(axis="x", rotation=90, labelsize=15)

sns.barplot(
    y="frequency",
    x="customer_id",
    data=rfm_df.sort_values(by="frequency", ascending=False).head(),
    palette=colors,
    ax=ax[1],
    hue="customer_id"
)

ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_facecolor("white")
ax[1].set_title("By Frequency", fontsize=25)
ax[1].tick_params(axis="x", rotation=90, labelsize=15)

sns.barplot(
    y="monetary",
    x="customer_id",
    data=rfm_df.sort_values(by="monetary", ascending=False).head(),
    palette=colors,
    ax=ax[2],
    hue="customer_id"
)

ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_facecolor("white")
ax[2].set_title("By Monetary", fontsize=25)
ax[2].tick_params(axis="x", rotation=90, labelsize=15)

st.pyplot(fig)

st.caption("Copyright (C) Chrypson Sidabalok 2024")