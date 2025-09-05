import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Generate made-up data ---
np.random.seed(123)
brokers = ["JPM", "MS", "Societe Generale", "Barclays", "UBS"]
regions = ["US", "Europe", "EMEA"]
dates = pd.date_range("2024-01-01", "2024-06-30", freq="B")
n = 1000

data = {
    "Date": np.random.choice(dates, n),
    "Broker": np.random.choice(brokers, n),
    "Region": np.random.choice(regions, n),
    "Quote": np.random.normal(100, 10, n).round(2),
    "Execution": np.random.normal(100, 12, n).round(2),
}
df = pd.DataFrame(data)
df["Slippage"] = (df["Execution"] - df["Quote"]).round(2)

# --- Sidebar filters ---
st.sidebar.header("Filters")
date_range = st.sidebar.slider(
    "Select date range",
    min_value=dates.min().date(),
    max_value=dates.max().date(),
    value=(dates.min().date(), dates.max().date()),
    key="date_slider"
)
region_sel = st.sidebar.multiselect("Select region(s)", regions, default=regions, key="region_multiselect")
broker_sel = st.sidebar.multiselect("Select broker(s)", brokers, default=brokers, key="broker_multiselect")

# --- Filter data ---
mask = (
    (df["Date"].dt.date >= date_range[0])
    & (df["Date"].dt.date <= date_range[1])
    & (df["Region"].isin(region_sel))
    & (df["Broker"].isin(broker_sel))
)
filtered = df[mask]

# --- Slippage estimation ---
st.subheader("Average Slippage per Broker")
slippage_broker = filtered.groupby("Broker")["Slippage"].mean().loc[broker_sel]
st.bar_chart(slippage_broker)

st.subheader("Boxplot of Slippage by Broker")
fig1, ax1 = plt.subplots()
filtered.boxplot(column="Slippage", by="Broker", ax=ax1)
plt.title("Slippage Distribution by Broker")
plt.suptitle("")
plt.xlabel("Broker")
plt.ylabel("Slippage")
st.pyplot(fig1, width='content')

st.subheader("Boxplot of Slippage by Region")
fig2, ax2 = plt.subplots()
filtered.boxplot(column="Slippage", by="Region", ax=ax2)
plt.title("Slippage Distribution by Region")
plt.suptitle("")
plt.xlabel("Region")
plt.ylabel("Slippage")
st.pyplot(fig2, width='content')

st.subheader("Boxplot of Slippage by Month")
filtered["Month"] = filtered["Date"].dt.to_period("M").astype(str)
fig3, ax3 = plt.subplots(figsize=(8, 4))
filtered.boxplot(column="Slippage", by="Month", ax=ax3)
plt.title("Slippage Distribution by Month")
plt.suptitle("")
plt.xlabel("Month")
plt.ylabel("Slippage")
st.pyplot(fig3, width='content')

st.subheader("Raw Data")
st.dataframe(filtered)