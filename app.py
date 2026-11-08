import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="DataHunterX - Real-time Crypto AI Quantitative Dashboard",
    page_icon="⚡",
    layout="wide"
)

st.title("DataHunterX - Real-time Crypto AI Quantitative Dashboard")
st.markdown("Automated Data Monitoring | Direct Binance API | AI Multi-factor & Reversal Radar")

st.sidebar.markdown("### Join DataHunterX Community")
st.sidebar.markdown("Get real-time automated alerts every minute!")
st.sidebar.button("Join Discord Server", on_click=lambda: st.write("https://discord.gg/QBCbTC"))

def get_crypto_data():
    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if not isinstance(data, (dict, list)):
            st.error(f"API Error: {response.text[:200]}")
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Data update failed: {str(e)}")
        return pd.DataFrame()

df = get_crypto_data()

if not df.empty and 'symbol' in df.columns:
    st.success("Data loaded successfully!")
    
    usdt_df = df[df['symbol'].str.endswith('USDT')].copy()
    
    numeric_cols = ['lastPrice', 'priceChangePercent', 'volume']
    for col in numeric_cols:
        if col in usdt_df.columns:
            usdt_df[col] = pd.to_numeric(usdt_df[col], errors='coerce')
            
    st.subheader("🔥 Binance Futures 24hr Price Change Radar")
    st.dataframe(usdt_df[['symbol', 'lastPrice', 'priceChangePercent', 'volume']].head(20), use_container_width=True)
else:
    st.warning("Failed to fetch Binance data. Please refresh later.")
