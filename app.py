import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

tickers = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN",
    "Meta (META)": "META",
    "Alphabet (GOOGL)": "GOOGL"
}

st.sidebar.title("S&P 500 Tech Titans Pulse")
selected_company = st.sidebar.selectbox("Select a Company", list(tickers.keys()))
ticker_symbol = tickers[selected_company]


st.title(f"{selected_company} – Real-Time Financial Dashboard")

company = yf.Ticker(ticker_symbol)
info = company.info
data = company.history(period="1y")

st.subheader("📊 Key Financial Metrics")

col1, col2 = st.columns(2)

with col1:
    st.metric("Market Cap", f"${round(info.get('marketCap', 0)/1e9, 2)} B")
    st.metric("Trailing P/E", info.get("trailingPE", "N/A"))
    st.metric("Revenue (TTM)", f"${round(info.get('totalRevenue', 0)/1e9, 2)} B")

with col2:
    net_income = info.get("netIncomeToCommon", 0)
    st.metric("Net Income (TTM)", f"${round(net_income/1e9, 2)} B" if net_income else "N/A")
    roe = info.get("returnOnEquity")
    st.metric("Return on Equity", f"{roe:.2%}" if roe else "N/A")
    st.metric("R&D Expense", f"${round(info.get('researchDevelopment', 0)/1e9, 2)} B")

st.subheader("📈 Stock Price - Last 1 Year")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
fig.update_layout(title=f"{ticker_symbol} Stock Price", xaxis_title="Date", yaxis_title="Price (USD)")
st.plotly_chart(fig, use_container_width=True)
try:
    revenue = info['totalRevenue']
    r_and_d = info.get('researchDevelopment', 0)
    capex = info.get('capitalExpenditures', 0)

    r_and_d_pct = (r_and_d / revenue) * 100 if revenue else None

    capex_b = abs(capex) / 1e9 if capex else None

except Exception as e:
    r_and_d_pct = capex_b = None

st.subheader("💡 Innovation & Investment KPIs")
col3, col4 = st.columns(2)

with col3:
    st.metric("R&D as % of Revenue", f"{r_and_d_pct:.2f}%" if r_and_d_pct else "N/A")
    st.metric("CapEx", f"${capex_b:.2f} B" if capex_b else "N/A")

with col4:
    st.metric("EPS (TTM)", info.get("trailingEps", "N/A"))
    st.metric("Operating Margin", f"{info.get('operatingMargins'):.2%}" if info.get("operatingMargins") else "N/A")
