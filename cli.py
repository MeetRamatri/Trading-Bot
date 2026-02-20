import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import validate_symbol, validate_side, validate_quantity, ValidationError
from binance.exceptions import BinanceAPIException, BinanceRequestException

app = typer.Typer(help="Trading Bot Command Line Interface")
console = Console()

def get_order_manager() -> OrderManager:
    try:
        client = BinanceClient()
        return OrderManager(client)
    except Exception as e:
        console.print(Panel(f"[bold red]Failed to initialize Binance Client:[/bold red]\n{e}", title="Error", border_style="red"))
        raise typer.Exit(code=1)

def print_success(title: str, response: dict):
    lines = [
        f"[bold green]Status:[/bold green] {response.get('status', 'UNKNOWN')}",
        f"[bold cyan]Order ID:[/bold cyan] {response.get('orderId', 'N/A')}",
        f"[bold yellow]Average Price:[/bold yellow] {response.get('avgPrice', 'N/A')}"
    ]
    panel = Panel("\n".join(lines), title=f"[bold green]{title} Successful[/bold green]", border_style="green")
    console.print(panel)

def print_error(error_msg: str):
    panel = Panel(f"[bold red]{error_msg}[/bold red]", title="Error Placing Order", border_style="red")
    console.print(panel)

@app.command("market-order")
def market_order(
    symbol: str = typer.Argument(..., help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side (BUY or SELL)"),
    quantity: float = typer.Argument(..., help="Quantity to trade")
):
    """
    Places a MARKET order on Binance Futures Testnet.
    """
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        quantity = validate_quantity(quantity)
    except ValidationError as e:
        console.print(Panel(f"[bold red]Validation Error:[/bold red]\n{e}", title="Invalid Input", border_style="red"))
        raise typer.Exit(code=1)

    manager = get_order_manager()
    
    with console.status(f"Placing MARKET order for {quantity} {symbol} ({side})...", spinner="dots"):
        try:
            response = manager.place_market_order(symbol, side, quantity)
            print_success("MARKET Order", response)
        except (BinanceAPIException, BinanceRequestException) as e:
            print_error(f"API Error:\n{e}")
            raise typer.Exit(code=1)
        except Exception as e:
            print_error(f"Unexpected Error:\n{e}")
            raise typer.Exit(code=1)

@app.command("limit-order")
def limit_order(
    symbol: str = typer.Argument(..., help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side (BUY or SELL)"),
    quantity: float = typer.Argument(..., help="Quantity to trade"),
    price: float = typer.Argument(..., help="Limit price")
):
    """
    Places a LIMIT order on Binance Futures Testnet.
    """
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        quantity = validate_quantity(quantity)
    except ValidationError as e:
        console.print(Panel(f"[bold red]Validation Error:[/bold red]\n{e}", title="Invalid Input", border_style="red"))
        raise typer.Exit(code=1)

    manager = get_order_manager()
    
    with console.status(f"Placing LIMIT order for {quantity} {symbol} ({side}) at {price}...", spinner="dots"):
        try:
            response = manager.place_limit_order(symbol, side, quantity, price)
            print_success("LIMIT Order", response)
        except (BinanceAPIException, BinanceRequestException) as e:
            print_error(f"API Error:\n{e}")
            raise typer.Exit(code=1)
        except Exception as e:
            print_error(f"Unexpected Error:\n{e}")
            raise typer.Exit(code=1)

@app.command("stop-limit-order")
def stop_limit_order(
    symbol: str = typer.Argument(..., help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side (BUY or SELL)"),
    quantity: float = typer.Argument(..., help="Quantity to trade"),
    stop_price: float = typer.Argument(..., help="Stop price to trigger the limit order"),
    price: float = typer.Argument(..., help="Limit price")
):
    """
    Places a STOP-LIMIT order on Binance Futures Testnet.
    """
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        quantity = validate_quantity(quantity)
        # Price and stop_price validation are handled in the order manager / validate_price, but let's just let it pass to manager
    except ValidationError as e:
        console.print(Panel(f"[bold red]Validation Error:[/bold red]\n{e}", title="Invalid Input", border_style="red"))
        raise typer.Exit(code=1)

    manager = get_order_manager()
    
    with console.status(f"Placing STOP-LIMIT order for {quantity} {symbol} ({side}) Trigger: {stop_price} Limit: {price}...", spinner="dots"):
        try:
            response = manager.place_stop_limit_order(symbol, side, quantity, stop_price, price)
            print_success("STOP-LIMIT Order", response)
        except (BinanceAPIException, BinanceRequestException) as e:
            print_error(f"API Error:\n{e}")
            raise typer.Exit(code=1)
        except Exception as e:
            print_error(f"Unexpected Error:\n{e}")
            raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
