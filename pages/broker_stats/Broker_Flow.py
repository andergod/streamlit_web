import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --- Generate made-up data ---
np.random.seed(42)
banks = ["JPM", "MS", "Societe Generale", "Barclays", "UBS"]
sectors = ["Technology", "Healthcare", "Finance", "Energy", "Consumer"]
dates = pd.date_range("2024-01-01", "2024-12-31", freq="W")
n = len(banks) * len(sectors) * len(dates)

data = {
    "Date": np.tile(dates, len(banks) * len(sectors)),
    "Bank": np.repeat(banks, len(sectors) * len(dates)),
    "Sector": np.tile(np.repeat(sectors, len(dates)), len(banks)),
    "Asset_Class": "Equities",
    "Flow": np.random.randint(1, 101, size=n)
    }

df = pd.DataFrame(data)

# --- Sidebar filters ---
st.sidebar.header("Filters")
timeline = st.sidebar.slider(
    "Select date range",
    min_value=dates.min().date(),
    max_value=dates.max().date(),
    value=(dates.min().date(), dates.max().date()),
    key="timeline_slider"
)
sector = st.sidebar.multiselect("Select sector(s)", sectors, default=sectors, key="sector_multiselect")

# --- Filter data ---
mask = (
    (df["Date"].dt.date >= timeline[0])
    & (df["Date"].dt.date <= timeline[1])
    & (df["Sector"].isin(sector))
    & (df["Asset_Class"] == "Equities")
)
filtered = df[mask]

# --- Dashboard ---
st.subheader("Broker Flow by Bank and Sector")
pivot = (
    filtered.groupby(["Bank", "Sector"])["Flow"]
    .sum()
    .unstack(fill_value=0)
    .loc[banks, sectors]
)
st.dataframe(pivot.style.format("{:.2f}"))
st.bar_chart(pivot)

st.subheader("Broker Flow Over Time (Line Chart)")
line_data = (
    filtered.groupby(["Date", "Bank"])["Flow"]
    .sum()
    .unstack(fill_value=0)
    .loc[:, banks]
)
st.line_chart(line_data)

st.subheader("Total Broker Flow by Bank (Pie Chart)")
pie_data = filtered.groupby("Bank")["Flow"].sum()
fig, ax = plt.subplots(figsize=(4, 4))  
pie_data.plot.pie(autopct="%.1f%%", ylabel="", ax=ax)
st.pyplot(fig, width='content')

st.subheader("Raw Data")
st.dataframe(filtered)