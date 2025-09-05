import streamlit as st
from src.data_loader import load_data

st.write("Welcome to the new dealing dashboard! Use the sidebar or the buttons below to navigate to different sections.")

st.header("Sections Overview")

st.markdown("""
### 📈 Broker Stats
- **Broker Flow:** Analyze equity flows by broker and sector, with interactive filters for timeline and sector.
- **Winning Trades:** Review top-performing trades and broker performance.

### 💹 CDS
- **Best Brokers:** Explore slippage and execution quality by broker and region for CDS.
- **Quotes:** View and analyze CDS quote data across regions and brokers.
""")

st.header("Quick Navigation")

col1, col2 = st.columns(2)

with col1:
    st.markdown("[🔄 Broker Flow](./broker_flow)")
    st.markdown("[🏆 Winning Trades](./winning_trades)")

with col2:
    st.markdown("[🌟 Best Brokers (CDS)](./best_brokers)")
    st.markdown("[💬 Quotes (CDS)](./quotes)")