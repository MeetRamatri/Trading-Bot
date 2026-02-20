# Binance Futures Trading Bot (Testnet)

This is a Python-based command-line trading bot for the Binance Futures Testnet. It allows you to place various types of orders (Market, Limit, and Stop-Limit) directly from your terminal.

## Prerequisites

- Python 3.8+
- A Binance Futures Testnet account and API keys.

## 1. Setting up the Virtual Environment

It is recommended to use a virtual environment to manage dependencies:

```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

## 2. Installing Requirements

With your virtual environment active, install the necessary dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## 3. Configuring the `.env` File for Binance Testnet

Create a file named `.env` in the root directory of the project (you can copy `.env.example` if it exists). Add your Binance Testnet API keys:

```env
API_KEY=your_testnet_api_key_here
SECRET_KEY=your_testnet_api_secret_here
```


## 4. Usage Examples

You can interact with the bot using the `cli.py` script. The bot validates inputs such as the symbol (e.g., BTCUSDT), side (BUY or SELL), quantity (must be > 0), and price (where applicable).

### Market Order
A Market order executes immediately at the current market price.

**Syntax:**
```bash
python cli.py market-order <SYMBOL> <SIDE> <QUANTITY>
```

**Example:** Place a MARKET BUY order for 0.01 BTC on the BTCUSDT pair:
```bash
python cli.py market-order BTCUSDT BUY 0.01
```

### Limit Order
A Limit order is placed on the order book at a specific price and executes when the market price reaches that level.

**Syntax:**
```bash
python cli.py limit-order <SYMBOL> <SIDE> <QUANTITY> <PRICE>
```

**Example:** Place a LIMIT SELL order for 0.05 BTC at a price of 65000:
```bash
python cli.py limit-order BTCUSDT SELL 0.05 65000
```

### Stop-Limit Order
A Stop-Limit order is a conditional order over a set timeframe that executes at a specified limit price after a given stop price has been reached. 
*(Note: Ensure your CLI utility `cli.py` is updated to include the `stop-limit-order` command exposing this underlying bot functionality).*

**Syntax:**
```bash
python cli.py stop-limit-order <SYMBOL> <SIDE> <QUANTITY> <STOP_PRICE> <LIMIT_PRICE>
```

**Example:** Place a STOP-LIMIT BUY order for 0.1 BTC. When the price hits 61000 (stop price), place a limit order to buy at 61500:
```bash
python cli.py stop-limit-order BTCUSDT BUY 0.1 61000 61500
```
