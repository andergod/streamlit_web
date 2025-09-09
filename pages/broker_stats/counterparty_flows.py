import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.model import train_model
from src.data_loader import load_data

# --- Generate made-up data ---
np.random.seed(123)
brokers = ["JPM", "MS", "Societe Generale", "Barclays", "UBS"]
asset_type = ["Equity", "Credit", "Rates"]
instrument = ["Inst1", "Inst2", "Inst3", "Inst4"]
side = ['Buy', 'Sell']
dates = pd.date_range("2020-01-01", "2024-06-30", freq="B")
n = 1000

data = {
    "Date": np.random.choice(dates, n),
    "Broker": np.random.choice(brokers, n),
    "Asset_Type": np.random.choice(asset_type, n),
    "Instrument": np.random.choice(instrument, n),
    "Side": np.random.choice(side, n),
    "Quantity": np.random.randint(1, 10, size =n),
    "avgFill":  np.random.randint(95, 105, size=n),
    "samplePrice": np.random.normal(98, 102, n).round(2)
}
df = pd.DataFrame(data)
df["Slippage"] = ((df["avgFill"] - df["samplePrice"])*df["Quantity"]).round(2)

st.title("Counterparty Flows")

# --- Filters inside the main component ---
with st.expander("Filters", expanded=True):
    date_range = st.slider(
        "Select date range",
        min_value=dates.min().date(),
        max_value=dates.max().date(),
        value=(dates.min().date(), dates.max().date()),
        key="date_slider"
    )
    broker_sel = st.multiselect("Select broker(s)", brokers, default=brokers, key="broker_multiselect")
    inst_sel = st.multiselect("Select instrument(s)", instrument, default=instrument, key="instrument_multiselect")
    asset_sel = st.multiselect("Select asset type(s)", asset_type, default=asset_type, key="asset_multiselect")

# --- Filter data ---
mask = (
    (df["Date"].dt.date >= date_range[0])
    & (df["Date"].dt.date <= date_range[1])
    & (df["Broker"].isin(broker_sel))
    & (df["Instrument"].isin(inst_sel))
    & (df["Asset_Type"].isin(asset_sel))
)
filtered = df[mask]

# --- Layout ---
left, right = st.columns([2, 1])

with left:
    st.subheader("Aggregated Table")
    agg_table = filtered.groupby(["Broker", "Instrument", "Side", "Asset_Type"]).agg(
        Trades=("Date", "count"),
        Total_Quantity=("Quantity", "sum"),
        Avg_Slippage=("Slippage", "mean"),
        Total_Slippage=("Slippage", "sum")
    ).round(2)
    st.dataframe(agg_table)

    st.markdown("---")

    # --- Lower section: Graphs with tabs ---
    tab1, tab2, tab3 = st.tabs(["Slippage by Broker", "Slippage by Instrument", "Slippage Over Time"])

    with tab1:
        st.subheader("Slippage by Broker")
        broker_slip = filtered.groupby("Broker")["Slippage"].mean().reset_index()
        fig1 = px.bar(broker_slip, x="Broker", y="Slippage", title="Avg Slippage by Broker")
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.subheader("Slippage by Instrument")
        inst_slip = filtered.groupby("Instrument")["Slippage"].mean().reset_index()
        fig2 = px.bar(inst_slip, x="Instrument", y="Slippage", title="Avg Slippage by Instrument")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Slippage Over Time")
        time_slip = filtered.groupby(filtered["Date"].dt.to_period("M"))["Slippage"].mean().reset_index()
        time_slip["Date"] = time_slip["Date"].astype(str)
        fig3 = px.line(time_slip, x="Date", y="Slippage", title="Avg Slippage Over Time")
        st.plotly_chart(fig3, use_container_width=True)

with right:
    st.subheader("Raw Data")
    st.dataframe(filtered)

    st.subheader("Slippage Distribution (Pie Chart)")
    pie_data = filtered.groupby("Broker")["Slippage"].sum().abs().reset_index()
    fig_pie = px.pie(pie_data, names="Broker", values="Slippage", title="Total Slippage by Broker")
    st.plotly_chart(fig_pie, use_container_width=False)