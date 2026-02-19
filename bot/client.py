import logging
import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BinanceClient:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("SECRET_KEY")

        if not self.api_key or not self.api_secret:
            logger.error("API_KEY or SECRET_KEY not found in environment variables.")
            raise ValueError("API_KEY and SECRET_KEY must be set in .env file.")

        try:
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            logger.info("Binance Futures Testnet Client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Binance Client: {e}")
            raise

    def fetch_symbol_price(self, symbol):
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.info(f"Current price for {symbol}: {price}")
            return price
        except BinanceAPIException as e:
            logger.error(f"Binance API Exception fetching price for {symbol}: {e}")
            return None
        except BinanceRequestException as e:
            logger.error(f"Binance Request Exception fetching price for {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching price for {symbol}: {e}")
            return None

    def get_account_balance(self):
        try:
            account = self.client.futures_account_balance()
            usdt_balance = next((item for item in account if item["asset"] == "USDT"), None)
            
            if usdt_balance:
                balance = float(usdt_balance['balance'])
                logger.info(f"Account Balance (USDT): {balance}")
                return balance
            else:
                 logger.info("USDT balance not found or account is empty.")
                 return account

        except BinanceAPIException as e:
            logger.error(f"Binance API Exception fetching balance: {e}")
            return None
        except BinanceRequestException as e:
            logger.error(f"Binance Request Exception fetching balance: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching balance: {e}")
            return None

if __name__ == "__main__":
    try:
        bc = BinanceClient()
        price = bc.fetch_symbol_price("BTCUSDT")
        print(f"Test Price fetch: {price}")
        balance = bc.get_account_balance()
        print(f"Test Balance fetch: {balance}")
    except Exception as e:
        print(f"Verification failed: {e}")
