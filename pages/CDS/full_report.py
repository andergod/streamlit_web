import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Generate made-up data ---
np.random.seed(123)
brokers = ["JPM", "MS", "Societe Generale", "Barclays", "UBS"]
instrument = ["Inst1", "Inst2", "Inst3", "Inst4"]
side = ['Buy', 'Sell']
dates = pd.date_range("2020-01-01", "2024-06-30", freq="B")
n = 1000

data = {
    "Date": np.random.choice(dates, n),
    "Broker": np.random.choice(brokers, n),
    "Instrument": np.random.choice(instrument, n),
    "Side": np.random.choice(side, n),
    "Quantity": np.random.randint(1, 10, size =n),
    "avgFill":  np.random.randint(95, 105, size=n),
    "samplePrice": np.random.normal(98, 102, n).round(2)
}
df = pd.DataFrame(data)
df["Slippage"] = ((df["avgFill"] - df["samplePrice"])*df["Quantity"]).round(2)

# --- Sidebar filters ---
st.sidebar.header("Filters")
date_range = st.sidebar.slider(
    "Select date range",
    min_value=dates.min().date(),
    max_value=dates.max().date(),
    value=(dates.min().date(), dates.max().date()),
    key="date_slider"
)
broker_sel = st.sidebar.multiselect("Select broker(s)", brokers, default=brokers, key="broker_multiselect")
inst_sel = st.sidebar.multiselect("Select instrument(s)", instrument, default=instrument, key="instrument_multiselect")

# --- Filter data ---
mask = (
    (df["Date"].dt.date >= date_range[0])
    & (df["Date"].dt.date <= date_range[1])
    & (df["Broker"].isin(broker_sel))
    & (df["Instrument"].isin(inst_sel))
)
filtered = df[mask]

# --- Layout ---
left, right = st.columns([2, 1])

with left:
    st.subheader("Aggregated Table")
    agg_table = filtered.groupby(["Broker", "Instrument", "Side"]).agg(
        Trades=("Date", "count"),
        Total_Quantity=("Quantity", "sum"),
        Avg_Slippage=("Slippage", "mean"),
        Total_Slippage=("Slippage", "sum")
    ).round(2)
    st.dataframe(agg_table)

with right:
    st.subheader("Raw Data")
    st.dataframe(filtered)

st.markdown("---")

# --- Lower section: Graphs with tabs ---
tab1, tab2, tab3 = st.tabs(["Slippage by Broker", "Slippage by Instrument", "Slippage Over Time"])

with tab1:
    st.subheader("Slippage by Broker")
    broker_slip = filtered.groupby("Broker")["Slippage"].sum()
    st.bar_chart(broker_slip)

with tab2:
    st.subheader("Slippage by Instrument")
    inst_slip = filtered.groupby("Instrument")["Slippage"].sum()
    st.bar_chart(inst_slip)

with tab3:
    st.subheader("Slippage Over Time")
    time_slip = filtered.groupby(filtered["Date"].dt.to_period("M"))["Slippage"].sum()
    time_slip.index = time_slip.index.astype(str)
    st.line_chart(time_slip)


