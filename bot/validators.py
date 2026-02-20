import re
from typing import Union

class ValidationError(ValueError):
    pass

def validate_symbol(symbol: str) -> str:
    if not isinstance(symbol, str):
        raise ValidationError(f"Symbol must be a string, got {type(symbol).__name__}.")
    
    symbol = symbol.upper().strip()
    if not re.match(r"^[A-Z0-9]+$", symbol):
        raise ValidationError(f"Symbol must contain only alphanumeric characters: '{symbol}'.")
    
    return symbol

def validate_side(side: str) -> str:
    if not isinstance(side, str):
        raise ValidationError(f"Side must be a string, got {type(side).__name__}.")
    
    side = side.upper().strip()
    if side not in {"BUY", "SELL"}:
        raise ValidationError(f"Side must be 'BUY' or 'SELL', got '{side}'.")
    
    return side

def validate_order_type(order_type: str) -> str:
    valid_types = {
        "LIMIT", "MARKET", "STOP", "STOP_MARKET", "STOP_LIMIT",
        "TAKE_PROFIT", "TAKE_PROFIT_MARKET", "TRAILING_STOP_MARKET"
    }
    
    if not isinstance(order_type, str):
        raise ValidationError(f"Order type must be a string, got {type(order_type).__name__}.")
    
    order_type = order_type.upper().strip()
    if order_type not in valid_types:
        raise ValidationError(f"Invalid order type: '{order_type}'. Must be one of {valid_types}.")
    
    return order_type

def validate_quantity(quantity: Union[int, float, str]) -> float:
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Quantity must be a numeric value, got {type(quantity).__name__}.")
    
    if qty <= 0:
        raise ValidationError(f"Quantity must be a positive number greater than 0, got {qty}.")
    
    return qty

def validate_price(price: Union[int, float, str, None], order_type: str) -> Union[float, None]:
    if order_type in {"LIMIT", "STOP_LIMIT"}:
        if price is None:
            raise ValidationError(f"Price must be provided for order type '{order_type}'.")
            
    if price is not None:
        try:
            p = float(price)
        except (ValueError, TypeError):
            raise ValidationError(f"Price must be a numeric value, got {type(price).__name__}.")
            
        if p <= 0:
            raise ValidationError(f"Price must be a positive number greater than 0, got {p}.")
            
        return p
        
    return None

def would_trigger_immediately(stop_price: float, current_price: float, side: str) -> bool:
    side = side.upper().strip()
    if side == "BUY" and current_price >= stop_price:
        return True
    elif side == "SELL" and current_price <= stop_price:
        return True
    return False
