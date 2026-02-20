from bot.logging_config import setup_logger
from bot.client import BinanceClient
from bot.validators import validate_symbol, validate_side, validate_quantity, validate_price, ValidationError
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = setup_logger(__name__)

class OrderManager:
    def __init__(self, client: BinanceClient):
        self.client = client.client  # Get raw python-binance client initialized in BinanceClient
        
    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """Places a MARKET order on Binance Futures."""
        try:
            symbol = validate_symbol(symbol)
            side = validate_side(side)
            quantity = validate_quantity(quantity)
        except ValidationError as e:
            logger.error(f"Validation Error before placing MARKET order: {e}")
            raise
            
        logger.info(f"Preparing MARKET order: Symbol={symbol}, Side={side}, Quantity={quantity}")
        try:
            order_params = {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": quantity,
            }
            logger.info(f"Request details: futures_create_order(**{order_params})")
            
            response = self.client.futures_create_order(**order_params)
            
            logger.info(f"Response details: {response}")
            
            return {
                "orderId": response.get("orderId"),
                "status": response.get("status"),
                "avgPrice": response.get("avgPrice") or response.get("price")
            }
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Binance API Error during MARKET order: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during MARKET order: {e}")
            raise

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict:
        """Places a LIMIT order on Binance Futures."""
        try:
            symbol = validate_symbol(symbol)
            side = validate_side(side)
            quantity = validate_quantity(quantity)
        except ValidationError as e:
            logger.error(f"Validation Error before placing LIMIT order: {e}")
            raise
            
        logger.info(f"Preparing LIMIT order: Symbol={symbol}, Side={side}, Quantity={quantity}, Price={price}")
        try:
            order_params = {
                "symbol": symbol,
                "side": side,
                "type": "LIMIT",
                "quantity": quantity,
                "price": price,
                "timeInForce": "GTC",  # Good Till Cancel
            }
            logger.info(f"Request details: futures_create_order(**{order_params})")
            
            response = self.client.futures_create_order(**order_params)
            
            logger.info(f"Response details: {response}")
            
            return {
                "orderId": response.get("orderId"),
                "status": response.get("status"),
                "avgPrice": response.get("avgPrice") or response.get("price")
            }
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Binance API Error during LIMIT order: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during LIMIT order: {e}")
            raise

    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, stop_price: float, price: float) -> dict:
        """Places a STOP_LIMIT order on Binance Futures."""
        try:
            symbol = validate_symbol(symbol)
            side = validate_side(side)
            quantity = validate_quantity(quantity)
            stop_price = validate_price(stop_price, "STOP_LIMIT")
            price = validate_price(price, "STOP_LIMIT")
        except ValidationError as e:
            logger.error(f"Validation Error before placing STOP_LIMIT order: {e}")
            raise
            
        logger.info(f"Preparing STOP_LIMIT order: Symbol={symbol}, Side={side}, Quantity={quantity}, StopPrice={stop_price}, Price={price}")
        try:
            order_params = {
                "symbol": symbol,
                "side": side,
                "type": "STOP",  # In Binance Futures, a STOP_LIMIT order is often just type "STOP" with both stopPrice and price. "STOP" type means STOP_LIMIT.
                "quantity": quantity,
                "stopPrice": stop_price,
                "price": price,
                "timeInForce": "GTC",
            }
            logger.info(f"Request details: futures_create_order(**{order_params})")
            
            response = self.client.futures_create_order(**order_params)
            
            logger.info(f"Response details: {response}")
            
            return {
                "orderId": response.get("orderId"),
                "status": response.get("status"),
                "avgPrice": response.get("avgPrice") or response.get("price")
            }
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Binance API Error during STOP_LIMIT order: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during STOP_LIMIT order: {e}")
            raise
