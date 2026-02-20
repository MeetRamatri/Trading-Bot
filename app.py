import streamlit as st
import os
from dotenv import load_dotenv
from bot.client import BinanceClient
from bot.orders import OrderManager

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Binance Futures Testnet Bot", layout="wide")

# Initialize session state for Binance Client & Balance
if "api_connected" not in st.session_state:
    st.session_state.api_connected = False
if "usdt_balance" not in st.session_state:
    st.session_state.usdt_balance = 0.0

def check_connection():
    """Validates the connection by fetching the account balance."""
    try:
        client = BinanceClient()
        balance = client.get_account_balance()
        if balance is not None:
            st.session_state.usdt_balance = balance
            st.session_state.api_connected = True
            st.success("API Keys are valid. Connected to Binance Testnet!")
        else:
            st.session_state.api_connected = False
            st.error("Failed to retrieve balance. Check API keys.")
    except Exception as e:
        st.session_state.api_connected = False
        st.error(f"Connection error: {e}")

# --- SIDEBAR ---
with st.sidebar:
    st.title("API Status")
    
    st.button("Check Connection", on_click=check_connection, use_container_width=True)
    
    if st.session_state.api_connected:
        st.success("Connected")
        st.metric("USDT Balance", f"${st.session_state.usdt_balance:.2f}")
    else:
        st.warning("Not connected")
        st.markdown("Ensure `.env` contains valid `API_KEY` and `SECRET_KEY`.")

# --- MAIN AREA ---
st.title("Trading Bot Dashboard")
st.markdown("Place orders on the Binance Futures Testnet directly from this interface.")

with st.form("order_entry_form"):
    st.subheader("Order Entry")
    
    col1, col2 = st.columns(2)
    with col1:
        symbol = st.selectbox("Symbol", options=["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"])
        order_type = st.selectbox("Order Type", options=["MARKET", "LIMIT", "STOP_LIMIT"])
    
    with col2:
        side = st.selectbox("Side", options=["BUY", "SELL"])
        quantity = st.number_input("Quantity", min_value=0.001, step=0.001, format="%.3f")
        
    st.markdown("---")
    
    # Conditional fields based on order type
    col3, col4 = st.columns(2)
    with col3:
        price = st.number_input("Limit Price (if LIMIT/STOP_LIMIT)", min_value=0.0, step=1.0, format="%.2f")
    with col4:
        stop_price = st.number_input("Stop Price (if STOP_LIMIT)", min_value=0.0, step=1.0, format="%.2f")
    
    submitted = st.form_submit_button("Submit Order", use_container_width=True)
    
    if submitted:
        if not st.session_state.api_connected:
            st.error("Please connect to the API first using the sidebar.")
        else:
            try:
                client = BinanceClient()
                manager = OrderManager(client)
                
                with st.spinner(f"Placing {order_type} order..."):
                    if order_type == "MARKET":
                        response = manager.place_market_order(symbol, side, quantity)
                    elif order_type == "LIMIT":
                        response = manager.place_limit_order(symbol, side, quantity, price)
                    elif order_type == "STOP_LIMIT":
                        response = manager.place_stop_limit_order(symbol, side, quantity, stop_price, price)
                
                st.success(f"Order Placed Successfully! Order ID: {response.get('orderId')}")
                st.json(response)
                
            except Exception as e:
                st.error(f"Failed to place order: {e}")
